import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.bias.bias_auditor import BiasAuditor


def test_bias_auditor_basic():
    auditor = BiasAuditor()
    text = "Immigrants are dirty and criminal. Women are lazy."
    result = auditor.analyze(text, "english")
    assert "metrics" in result
    assert result["metrics"].get("gender", 0) >= 0
