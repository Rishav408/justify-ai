import json
import re
from pathlib import Path


class LexiconMatcher:
    def __init__(self):
        self._cache = {}

    def _lexicon_path(self, language: str) -> Path:
        base = Path(__file__).parent / "lexicons"
        return base / f"{language}.json"

    def _load_lexicon(self, language: str) -> list[dict]:
        if language in self._cache:
            return self._cache[language]
        path = self._lexicon_path(language)
        if not path.exists():
            self._cache[language] = []
            return self._cache[language]
        # Use utf-8-sig to tolerate BOMs from Windows/Excel exports.
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        # Ensure consistent structure
        normalized = []
        for entry in data:
            term = str(entry.get("term", "")).strip()
            if not term:
                continue
            normalized.append({
                "term": term,
                "severity": entry.get("severity", "low")
            })
        self._cache[language] = normalized
        return normalized

    def _is_latin_term(self, term: str) -> bool:
        return all(ord(ch) < 128 for ch in term)

    def _find_spans(self, text: str, term: str) -> list[list[int]]:
        spans = []
        lowered = text.lower()
        term_lower = term.lower()

        # For simple Latin words, use word boundaries.
        if self._is_latin_term(term_lower) and re.match(r"^[a-z0-9_\- ]+$", term_lower):
            if " " in term_lower:
                pattern = re.escape(term_lower)
            else:
                pattern = r"\b" + re.escape(term_lower) + r"\b"
            for m in re.finditer(pattern, lowered):
                spans.append([m.start(), m.end()])
            return spans

        # For non-Latin scripts or mixed tokens, use substring matches.
        start = 0
        while True:
            idx = lowered.find(term_lower, start)
            if idx == -1:
                break
            spans.append([idx, idx + len(term_lower)])
            start = idx + len(term_lower)
        return spans

    def match(self, text: str, language: str) -> list[dict]:
        lexicon = self._load_lexicon(language)
        if not text or not lexicon:
            return []

        hits = []
        for entry in lexicon:
            term = entry["term"]
            spans = self._find_spans(text, term)
            if spans:
                hits.append({
                    "term": term,
                    "severity": entry.get("severity", "low"),
                    "count": len(spans),
                    "spans": spans
                })
        return hits


if __name__ == "__main__":
    matcher = LexiconMatcher()
    sample = "I hate this. They should be expelled. नफरत फैलाना बंद करो।"
    print(matcher.match(sample, "english"))
    print(matcher.match(sample, "hindi"))
