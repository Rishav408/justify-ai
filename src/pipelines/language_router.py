"""
Language Router
===============
Routes incoming text to the appropriate language pipeline based on detection.
"""

from src.utils.language_detection import detect_language
from src.pipelines.english_pipeline import run_english_pipeline
from src.pipelines.hindi_pipeline import run_hindi_pipeline


def route_language(text: str) -> dict:
    """
    Detect language and route to the correct pipeline.

    Supports:
    - English  → English NLP pipeline
    - Hindi    → Hindi NLP pipeline  (indic-bert embeddings + Hindi modules)
    - Hinglish → Hindi pipeline (with a flag)
    """
    lang = detect_language(text)

    if lang == "english":
        return run_english_pipeline(text)

    elif lang == "hindi":
        return run_hindi_pipeline(text)

    elif lang == "hinglish":
        # For code-mixed text, run through Hindi pipeline and flag it
        result = run_hindi_pipeline(text)
        result["language"] = "hinglish"
        result["note"] = "Code-mixed Hindi-English text detected. Analysis used Hindi pipeline."
        return result

    else:
        return {
            "error": "Language not supported",
            "detected": lang,
            "supported": ["english", "hindi", "hinglish"],
        }
