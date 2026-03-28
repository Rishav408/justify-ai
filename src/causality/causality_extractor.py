import re


class CausalityExtractor:
    """
    Lightweight rule-based causal relation extractor.
    Returns relations as dicts: {cause, effect, relation, confidence, sentence}
    """
    def __init__(self):
        self._patterns = {
            "english": [
                # cause because effect
                (r"(?P<effect>.+?)\s+because\s+(?P<cause>.+)", "because", 0.85),
                # effect due to cause
                (r"(?P<effect>.+?)\s+due to\s+(?P<cause>.+)", "due_to", 0.82),
                (r"(?P<effect>.+?)\s+as a result of\s+(?P<cause>.+)", "result_of", 0.82),
                # cause leads to effect
                (r"(?P<cause>.+?)\s+leads to\s+(?P<effect>.+)", "leads_to", 0.78),
                (r"(?P<cause>.+?)\s+results in\s+(?P<effect>.+)", "results_in", 0.78),
                (r"(?P<cause>.+?)\s+causes\s+(?P<effect>.+)", "causes", 0.8),
                (r"(?P<cause>.+?)\s+triggers\s+(?P<effect>.+)", "triggers", 0.75),
            ],
            "hindi": [
                # because/ कारण
                (r"(?P<effect>.+?)\s+क्योंकि\s+(?P<cause>.+)", "क्योंकि", 0.85),
                (r"(?P<effect>.+?)\s+इसके कारण\s+(?P<cause>.+)", "कारण", 0.8),
                (r"(?P<cause>.+?)\s+के कारण\s+(?P<effect>.+)", "के_कारण", 0.8),
                (r"(?P<cause>.+?)\s+से\s+(?P<effect>.+)", "से", 0.72),
                (r"(?P<cause>.+?)\s+की वजह से\s+(?P<effect>.+)", "वजह_से", 0.82),
                (r"(?P<cause>.+?)\s+से\s+.*?होता है\s*(?P<effect>.+)?", "से", 0.7),
            ],
            "marathi": [
                (r"(?P<effect>.+?)\s+कारण\s+(?P<cause>.+)", "कारण", 0.8),
                (r"(?P<cause>.+?)\s+मुळे\s+(?P<effect>.+)", "मुळे", 0.82),
                (r"(?P<cause>.+?)\s+मुळेच\s+(?P<effect>.+)", "मुळेच", 0.82),
            ],
            "bhojpuri": [
                (r"(?P<effect>.+?)\s+काहे कि\s+(?P<cause>.+)", "काहे_कि", 0.78),
                (r"(?P<cause>.+?)\s+से\s+(?P<effect>.+)", "से", 0.7),
                (r"(?P<cause>.+?)\s+के कारण\s+(?P<effect>.+)", "के_कारण", 0.78),
            ],
            "marwari": [
                (r"(?P<effect>.+?)\s+कुणकि\s+(?P<cause>.+)", "कुणकि", 0.78),
                (r"(?P<cause>.+?)\s+र कारण\s+(?P<effect>.+)", "र_कारण", 0.78),
                (r"(?P<cause>.+?)\s+सू\s+(?P<effect>.+)", "सू", 0.7),
            ],
        }

    def _split_sentences(self, text: str) -> list[str]:
        if not text:
            return []
        # Split on common sentence delimiters including Devanagari danda.
        parts = re.split(r"[.!?।]+", text)
        return [p.strip() for p in parts if p.strip()]

    def _clean_fragment(self, frag: str) -> str:
        frag = re.sub(r"\s+", " ", frag or "").strip()
        # Trim leading/trailing quotes or punctuation
        return frag.strip(" \"'“”‘’(),;:-")

    def extract_relations(self, text: str, language: str) -> list[dict]:
        patterns = self._patterns.get(language, self._patterns["english"])
        relations = []
        for sentence in self._split_sentences(text):
            lowered = sentence.lower() if language == "english" else sentence
            for pattern, rel, conf in patterns:
                m = re.match(pattern, lowered, flags=re.IGNORECASE) if language == "english" else re.match(pattern, sentence)
                if not m:
                    continue
                cause = self._clean_fragment(m.groupdict().get("cause", ""))
                effect = self._clean_fragment(m.groupdict().get("effect", ""))
                if not cause or not effect:
                    continue
                relations.append({
                    "cause": cause,
                    "effect": effect,
                    "relation": rel,
                    "confidence": conf,
                    "sentence": sentence
                })
        return relations


if __name__ == "__main__":
    extractor = CausalityExtractor()
    sample = "Violence increases because hateful speech spreads. Immigration leads to job loss."
    print(extractor.extract_relations(sample, "english"))
