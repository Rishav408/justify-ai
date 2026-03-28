from src.scoring.risk_scorer import RiskScorer


def test_risk_scorer_combines_signals():
    scorer = RiskScorer()
    lex = [{"term": "kill", "severity": "high", "count": 1}]
    causal = [{"cause": "x", "effect": "y"}]
    bias = {"overall": 40}
    result = scorer.score(lex, causal, bias)
    assert 0 <= result["score"] <= 100
    assert result["breakdown"]["lexical"] > 0
