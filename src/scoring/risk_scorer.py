class RiskScorer:
    """
    Combine lexical + causal + bias signals into a single risk score (0-100).
    This is a lightweight baseline; weights can be tuned per language later.
    """
    def __init__(self):
        self.weights = {
            "lexical": 0.45,
            "causal": 0.30,
            "bias": 0.25
        }

        # Severity mapping for lexicon hits
        self.lex_severity = {
            "low": 10,
            "medium": 25,
            "high": 40,
            "critical": 55
        }

    def score_lexical(self, lexicon_hits: list[dict]) -> int:
        total = 0
        for hit in lexicon_hits or []:
            sev = str(hit.get("severity", "low")).lower()
            count = int(hit.get("count", 1))
            total += self.lex_severity.get(sev, 10) * count
        return min(100, total)

    def score_causal(self, causality_relations: list[dict]) -> int:
        # Simple: each causal relation adds intensity
        count = len(causality_relations or [])
        return min(100, count * 30)

    def score_bias(self, bias_metrics: dict) -> int:
        if not bias_metrics:
            return 0
        # Use overall if present, else mean of dimensions
        if "overall" in bias_metrics:
            try:
                return int(bias_metrics.get("overall", 0))
            except Exception:
                return 0
        values = [v for v in bias_metrics.values() if isinstance(v, (int, float))]
        if not values:
            return 0
        return int(sum(values) / len(values))

    def _risk_level(self, score: int) -> str:
        if score < 25:
            return "low"
        if score < 50:
            return "medium"
        if score < 75:
            return "high"
        return "critical"

    def score(self, lexicon_hits: list[dict], causality_relations: list[dict], bias_metrics: dict) -> dict:
        lex = self.score_lexical(lexicon_hits)
        causal = self.score_causal(causality_relations)
        bias = self.score_bias(bias_metrics)

        final = int(
            (lex * self.weights["lexical"]) +
            (causal * self.weights["causal"]) +
            (bias * self.weights["bias"])
        )
        final = max(0, min(100, final))

        return {
            "score": final,
            "level": self._risk_level(final),
            "breakdown": {
                "lexical": lex,
                "causal": causal,
                "bias": bias
            }
        }


if __name__ == "__main__":
    scorer = RiskScorer()
    print(scorer.score(
        [{"term": "kill", "severity": "high", "count": 1}],
        [{"cause": "x", "effect": "y"}],
        {"overall": 40}
    ))
