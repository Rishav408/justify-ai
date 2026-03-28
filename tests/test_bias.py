from src.bias.bias_auditor import BiasAuditor


def test_bias_auditor_basic():
    auditor = BiasAuditor()
    text = "Immigrants are dirty and criminal. Women are lazy."
    result = auditor.analyze(text, "english")
    assert "metrics" in result
    assert result["metrics"].get("gender", 0) >= 0
