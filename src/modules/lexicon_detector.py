import json
from pathlib import Path

LEXICON_PATH = Path("data/lexicons/lexicon_en.json")

def load_lexicon():
    with open(LEXICON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

lexicon = load_lexicon()

def detect_lexicon(tokens):
    detected = []
    for token in tokens:
        if token.lower() in lexicon:
            detected.append(token)
    return detected