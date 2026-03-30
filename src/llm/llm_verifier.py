"""
Phase 8: AI/LLM Verification Layer for Justify-AI
Uses LangChain + Google Gemini to review and verify pipeline output.
"""

import os
import json
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Lazy imports — only loaded when actually used
_langchain_available = None


def _check_langchain():
    """Check if LangChain + Gemini packages are importable."""
    global _langchain_available
    if _langchain_available is not None:
        return _langchain_available
    try:
        from langchain_ollama import ChatOllama  # noqa: F401
        from langchain_core.prompts import ChatPromptTemplate  # noqa: F401
        _langchain_available = True
    except ImportError:
        _langchain_available = False
        logger.warning("LangChain / langchain-ollama not installed. AI review disabled.")
    return _langchain_available


SYSTEM_PROMPT = """You are an AI moderator for Justify-AI. 
Review the provided JSON output from our multilingual hate speech detection pipeline. 
Return ONLY valid JSON formatted precisely according to the requested rules structure.

## Response Format
You MUST respond with ONLY a valid JSON object (no markdown fencing, no extra text). Use this exact structure:
{{
  "agrees_with_classification": true or false,
  "suggested_label": "hate" or "offensive" or "non_hate" or "health_issue",
  "confidence_in_model_output": "high" or "medium" or "low"
}}
"""

USER_PROMPT_TEMPLATE = """Review the following raw JSON output from the Justify-AI pipeline:
```json
{json_payload}
```
Please provide your structural verification review as a strict JSON object responding to the rules defined."""


class LLMVerifier:
    """
    Verifies pipeline outputs using Google Gemini via LangChain.
    Gracefully returns None if API key is missing or packages unavailable.
    """

    def __init__(self):
        self._chain = None
        self._initialized = False

    def _ensure_initialized(self) -> bool:
        """Lazy initialization — only sets up LLM chain on first call."""
        if self._initialized:
            return self._chain is not None

        self._initialized = True

        # Load .env if python-dotenv is available
        try:
            from dotenv import load_dotenv
            # Search for .env in project root (2 levels up from this file)
            env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
            load_dotenv(os.path.abspath(env_path))
        except ImportError:
            pass

        if not _check_langchain():
            return False

        try:
            from langchain_ollama import ChatOllama
            from langchain_core.prompts import ChatPromptTemplate

            model_name = os.environ.get("OLLAMA_MODEL", "qwen3.5:2b").strip()
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").strip()

            llm = ChatOllama(
                model=model_name,
                base_url=base_url,
                temperature=0.3,
                format="json"
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                ("human", USER_PROMPT_TEMPLATE),
            ])

            self._chain = prompt | llm
            logger.info(f"LLM Verifier initialized with Local AI model: {model_name} at {base_url}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize LLM Verifier: {e}")
            self._chain = None
            return False

    def _parse_response(self, raw_text: str) -> Optional[dict]:
        """Parse LLM response text into a structured dict."""
        text = raw_text.strip()

        # Strip markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line (```)
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            logger.warning(f"LLM returned non-JSON response: {text[:200]}")
            # Attempt to extract JSON from the text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    parsed = json.loads(text[start:end])
                except json.JSONDecodeError:
                    return None
            else:
                return None

        # Validate required keys
        required_keys = [
            "agrees_with_classification",
            "suggested_label",
            "confidence_in_model_output"
        ]
        for key in required_keys:
            if key not in parsed:
                logger.warning(f"LLM response missing key: {key}")
                parsed.setdefault(key, None)

        return parsed

    def verify(self, analysis_result: dict) -> Optional[dict]:
        """
        Verify a pipeline analysis result using Gemini.
        Retries up to 3 times with exponential backoff on rate-limit errors.

        Args:
            analysis_result: The full API response dict from the /api/analyze endpoint.

        Returns:
            A structured verification dict, or None if verification is unavailable.
        """
        if not self._ensure_initialized():
            return None

        # Build prompt variables once
        try:
            # We construct a minimized JSON payload string to save thousands of tokens
            minimal_payload = {
                "text": analysis_result.get("text", ""),
                "assigned_label": analysis_result.get("hate_speech_label", "unknown")
            }
            payload_str = json.dumps(minimal_payload, ensure_ascii=False)
            prompt_vars = {
                "json_payload": payload_str
            }
        except Exception as e:
            logger.error(f"Failed to build prompt variables: {e}")
            return None

        # Retry logic for local LLM (e.g., if Ollama is temporarily busy or rejecting)
        max_retries = 2
        base_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                response = self._chain.invoke(prompt_vars)

                # Extract text from the LangChain response
                raw_text = response.content if hasattr(response, "content") else str(response)

                result = self._parse_response(raw_text)
                if result is None:
                    logger.warning("Failed to parse LLM verification response.")
                    return None

                return result

            except Exception as e:
                error_str = str(e).lower()
                is_connection_error = any(kw in error_str for kw in [
                    "connection refused", "connect", "timeout", "not found"
                ])

                if is_connection_error:
                    logger.warning(
                        "Could not connect to Ollama. "
                        "Ensure Ollama is running (`ollama serve`) and the model is downloaded."
                    )
                    return None
                elif attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # 2s, 4s
                    logger.warning(
                        f"Local LLM error hit (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"LLM verification failed: {e}")
                    return None

        return None

    @property
    def is_available(self) -> bool:
        """Check if the verifier is configured and ready."""
        return self._ensure_initialized()


if __name__ == "__main__":
    # Quick smoke test
    verifier = LLMVerifier()
    print(f"Available: {verifier.is_available}")

    if verifier.is_available:
        sample_result = {
            "text": "These immigrants are ruining our country. They should be deported.",
            "hate_speech_label": "hate"
        }
        review = verifier.verify(sample_result)
        print(json.dumps(review, indent=2, ensure_ascii=False))
    else:
        print("Verifier not available (Langchain packages not installed).")
