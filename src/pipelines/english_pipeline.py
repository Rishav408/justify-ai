import spacy
from src.modules.preprocessing import clean_text
from src.modules.lexicon_detector import detect_lexicon
from src.modules.causality_extractor import extract_causality
from src.modules.bias_detector import detect_bias
from src.modules.risk_scorer import calculate_risk
from src.modules.explanation_generator import generate_explanation

nlp = spacy.load("en_core_web_sm")

def run_english_pipeline(text):

    cleaned = clean_text(text)

    doc = nlp(cleaned)

    # Note: doc returns spacy tokens. We use token.text down to simple list for our simplistic modules
    tokens = [token.text for token in doc]
    lemmas = [token.lemma_ for token in doc]
    sentences = [sent.text for sent in doc.sents]
    
    # Keeping POS tags if they were needed, otherwise not explicitly required in new mock
    # pos = [(token.text, token.pos_) for token in doc]

    lexicon_hits = detect_lexicon(lemmas)
    causality_hits = extract_causality(lemmas)
    bias_hits = detect_bias(lemmas)

    risk = calculate_risk(
        lexicon_hits,
        causality_hits,
        bias_hits
    )

    explanation = generate_explanation(
        lexicon_hits,
        causality_hits,
        bias_hits,
        risk
    )

    return {
        "language": "english",
        "tokens": tokens,
        "sentences": sentences,
        "lexicon_hits": lexicon_hits,
        "causality_hits": causality_hits,
        "bias_hits": bias_hits,
        "risk": risk,
        "explanation": explanation
    }