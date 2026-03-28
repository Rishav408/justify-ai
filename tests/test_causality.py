from src.causality.causality_extractor import CausalityExtractor


def test_causality_extraction_english():
    extractor = CausalityExtractor()
    text = "Violence increases because hateful speech spreads. Immigration leads to job loss."
    relations = extractor.extract_relations(text, "english")
    assert len(relations) >= 2
    assert any(r["relation"] == "because" for r in relations)
