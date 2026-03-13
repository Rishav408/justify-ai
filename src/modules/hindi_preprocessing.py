"""
Hindi Preprocessing
===================
Text cleaning functions for Hindi / Devanagari text.
Preserves Devanagari characters while stripping unwanted noise.
"""

import re


def clean_hindi_text(text: str) -> str:
    """
    Clean Hindi text while preserving Devanagari script.

    Steps:
    1. Strip leading/trailing whitespace
    2. Remove URLs
    3. Remove HTML tags
    4. Keep Devanagari characters (\\u0900-\\u097F), digits, whitespace,
       and basic Latin letters (for code-mixed text)
    5. Collapse multiple spaces
    """
    text = text.strip()

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Keep Devanagari (U+0900–U+097F), Latin letters, digits, whitespace
    text = re.sub(r"[^\u0900-\u097F\w\s]", "", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_hindi(text: str) -> list[str]:
    """
    Simple whitespace tokenizer for Hindi.
    (Hindi words are space-separated, unlike scripts like Thai/Chinese.)
    """
    cleaned = clean_hindi_text(text)
    return cleaned.split()
