"""
Hindi Lexicon Detector
======================
Detects influence-related Hindi words using the Hindi lexicon file.
"""

import json
from pathlib import Path

LEXICON_PATH = Path("data/lexicons/lexicon_hi.json")


def load_hindi_lexicon():
    with open(LEXICON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_lexicon = load_hindi_lexicon()


def detect_hindi_lexicon(tokens: list[str]) -> list[dict]:
    """
    Detect lexicon hits from Hindi tokens.

    Returns a list of dicts: [{"word": ..., "category": ...}, ...]
    """
    detected = []
    for token in tokens:
        if token in _lexicon:
            detected.append({"word": token, "category": _lexicon[token]})
    return detected
