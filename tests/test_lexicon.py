from src.lexicon.lexicon_matcher import LexiconMatcher


def test_lexicon_matcher_english_basic():
    matcher = LexiconMatcher()
    hits = matcher.match("I hate them and want to kill them.", "english")
    terms = {h["term"] for h in hits}
    assert "hate" in terms
    assert "kill" in terms
