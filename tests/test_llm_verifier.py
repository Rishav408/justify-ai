"""Tests for the LLM Verifier module."""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.llm.llm_verifier import LLMVerifier, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class TestLLMVerifierInit:
    """Test that the verifier initializes safely in all conditions."""

    def test_init_without_error(self):
        """LLMVerifier should instantiate without raising."""
        verifier = LLMVerifier()
        assert verifier is not None
        assert verifier._chain is None
        assert verifier._initialized is False

    def test_verify_returns_none_without_langchain(self):
        """Without langchain packages, verify() should return None gracefully."""
        from unittest.mock import patch
        with patch('src.llm.llm_verifier._check_langchain', return_value=False):
            verifier = LLMVerifier()
            result = verifier.verify({"text": "test", "language": "english"})
            assert result is None

    def test_is_available_false_without_langchain(self):
        """is_available should return False when packages are missing."""
        from unittest.mock import patch
        with patch('src.llm.llm_verifier._check_langchain', return_value=False):
            verifier = LLMVerifier()
            assert verifier.is_available is False


class TestSystemPrompt:
    """Test that the system prompt contains essential context."""

    def test_prompt_mentions_json_response(self):
        assert "agrees_with_classification" in SYSTEM_PROMPT
        assert "suggested_label" in SYSTEM_PROMPT


class TestUserPromptTemplate:
    """Test that the user prompt template has all required placeholders."""

    def test_all_placeholders_present(self):
        expected_vars = ["json_payload"]
        for var in expected_vars:
            assert f"{{{var}}}" in USER_PROMPT_TEMPLATE, f"Missing placeholder: {var}"


class TestResponseParsing:
    """Test the response parsing logic."""

    def test_parse_valid_json(self):
        verifier = LLMVerifier()
        raw = json.dumps({
            "agrees_with_classification": True,
            "suggested_label": "hate",
            "confidence_in_model_output": "high"
        })
        result = verifier._parse_response(raw)
        assert result is not None
        assert result["agrees_with_classification"] is True
        assert result["suggested_label"] == "hate"

    def test_parse_json_with_markdown_fences(self):
        verifier = LLMVerifier()
        raw = '```json\n{"agrees_with_classification": false, "suggested_label": "non_hate", "confidence_in_model_output": "low"}\n```'
        result = verifier._parse_response(raw)
        assert result is not None
        assert result["agrees_with_classification"] is False

    def test_parse_invalid_json_returns_none(self):
        verifier = LLMVerifier()
        result = verifier._parse_response("This is not JSON at all")
        assert result is None

    def test_parse_json_embedded_in_text(self):
        verifier = LLMVerifier()
        raw = 'Here is my review: {"agrees_with_classification": true, "suggested_label": "hate", "confidence_in_model_output": "high"} end.'
        result = verifier._parse_response(raw)
        assert result is not None
        assert result["agrees_with_classification"] is True

    def test_missing_keys_get_defaults(self):
        verifier = LLMVerifier()
        raw = json.dumps({"agrees_with_classification": True})
        result = verifier._parse_response(raw)
        assert result is not None
        assert result.get("suggested_label") is None



if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
