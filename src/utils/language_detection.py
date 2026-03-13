"""
Language Detection Utility
==========================
Detects whether the input text is Hindi, English, or an unsupported language.
Also provides code-mixing detection for Hindi-English hybrid text.
"""

from langdetect import detect, DetectorFactory
import re

# Make langdetect deterministic
DetectorFactory.seed = 0

# Devanagari Unicode range
_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
_LATIN_RE = re.compile(r"[a-zA-Z]")


def detect_language(text: str) -> str:
    """
    Detect the language of the given text.

    Returns
    -------
    str
        One of: "hindi", "english", "hinglish" (code-mixed), or "unknown".
    """
    if not text or not text.strip():
        return "unknown"

    try:
        # Check for code-mixing first
        has_devanagari = bool(_DEVANAGARI_RE.search(text))
        has_latin = bool(_LATIN_RE.search(text))

        if has_devanagari and has_latin:
            return "hinglish"

        lang = detect(text)

        if lang == "hi":
            return "hindi"
        elif lang == "en":
            return "english"
        # langdetect sometimes confuses Hindi with Marathi / Nepali
        elif lang in ("mr", "ne"):
            return "hindi"
        else:
            return "unknown"

    except Exception:
        # Fallback: check for Devanagari characters
        if has_devanagari:
            return "hindi"
        return "unknown"


def get_language_confidence(text: str) -> dict:
    """
    Return detection probabilities for all considered languages.
    Useful for debugging or displaying confidence to the user.
    """
    from langdetect import detect_langs

    try:
        results = detect_langs(text)
        return {str(r.lang): round(r.prob, 4) for r in results}
    except Exception:
        return {}
