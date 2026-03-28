import re


class BiasAuditor:
    """
    Lightweight bias auditor using lexicon co-occurrence.
    Detects demographic group mentions + negative attribute words in same sentence.
    Returns metrics and evidence hits.
    """
    def __init__(self):
        self._groups = {
            "english": {
                "gender": ["women", "woman", "female", "men", "man", "male", "girls", "boys"],
                "religion": ["muslim", "hindu", "christian", "jew", "sikh", "buddhist"],
                "ethnicity": ["black", "white", "brown", "asian", "latino", "tribal"],
                "nationality": ["immigrant", "foreigner", "outsider", "refugee", "migrant"],
                "caste": ["caste", "dalit", "upper caste", "lower caste"],
                "political": ["party", "government", "leftist", "rightist"],
                "language": ["english speakers", "hindi speakers", "marathi speakers"],
            },
            "hindi": {
                "gender": ["महिला", "औरत", "लड़की", "पुरुष", "आदमी", "लड़का"],
                "religion": ["मुस्लिम", "हिंदू", "ईसाई", "सिख", "बौद्ध"],
                "ethnicity": ["जाति", "जनजाति", "नस्ल"],
                "nationality": ["विदेशी", "प्रवासी", "शरणार्थी"],
                "caste": ["दलित", "ऊंची जाति", "नीची जाति"],
                "political": ["पार्टी", "सरकार", "नेता"],
                "language": ["हिंदी", "मराठी", "भोजपुरी", "मारवाड़ी"],
            },
        }

        self._negatives = {
            "english": [
                "criminal", "violent", "dirty", "filthy", "lazy", "stupid",
                "terrorist", "thief", "rapist", "parasite", "invader",
                "illegal", "uneducated", "backward", "disgusting",
                "dangerous", "disease", "vermin"
            ],
            "hindi": [
                "अपराधी", "हिंसक", "गंदा", "आलसी", "बेवकूफ",
                "आतंकवादी", "चोर", "बलात्कारी", "परजीवी",
                "अवैध", "अनपढ़", "पिछड़ा", "खतरनाक", "बीमारी"
            ],
        }

    def _split_sentences(self, text: str) -> list[str]:
        if not text:
            return []
        parts = re.split(r"[.!?।]+", text)
        return [p.strip() for p in parts if p.strip()]

    def _match_terms(self, sentence: str, terms: list[str], is_english: bool) -> list[str]:
        hits = []
        lowered = sentence.lower() if is_english else sentence
        for term in terms:
            t = term.lower() if is_english else term
            if is_english:
                pattern = r"\b" + re.escape(t) + r"\b"
                if re.search(pattern, lowered):
                    hits.append(term)
            else:
                if t in lowered:
                    hits.append(term)
        return hits

    def analyze(self, text: str, language: str) -> dict:
        lang = language if language in self._groups else "english"
        groups = self._groups.get(lang, {})
        negatives = self._negatives.get(lang, self._negatives["english"])
        is_english = lang == "english"

        hits = []
        counts = {k: 0 for k in groups.keys()}
        for sentence in self._split_sentences(text):
            neg_hits = self._match_terms(sentence, negatives, is_english)
            if not neg_hits:
                continue
            for dim, terms in groups.items():
                grp_hits = self._match_terms(sentence, terms, is_english)
                if not grp_hits:
                    continue
                counts[dim] += len(grp_hits)
                hits.append({
                    "dimension": dim,
                    "groups": grp_hits,
                    "negatives": neg_hits,
                    "sentence": sentence
                })

        metrics = {}
        total = 0
        for dim, cnt in counts.items():
            score = min(100, cnt * 20)
            metrics[dim] = score
            total += score

        metrics["overall"] = min(100, total // max(1, len(counts)))

        return {
            "metrics": metrics,
            "hits": hits
        }


if __name__ == "__main__":
    auditor = BiasAuditor()
    sample = "Immigrants are dirty and criminal. Women are lazy."
    print(auditor.analyze(sample, "english"))
