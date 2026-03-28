import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.lexicon.lexicon_matcher import LexiconMatcher


def test_lexicon_matcher_english_basic():
    matcher = LexiconMatcher()
    hits = matcher.match("I hate them and want to kill them.", "english")
    terms = {h["term"] for h in hits}
    assert "hate" in terms
    assert "kill" in terms
