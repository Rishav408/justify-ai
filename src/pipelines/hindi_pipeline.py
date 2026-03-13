"""
Hindi NLP Pipeline
==================
Full analysis pipeline for Hindi text — mirrors the English pipeline.

Steps:
1. Preprocess & tokenize Hindi text
2. Generate embeddings via indic-bert (optional, for advanced features)
3. Detect lexicon hits (influence-related words)
4. Extract causal / justification markers
5. Detect bias / absolute language
6. Calculate risk score
7. Generate explanation
"""

from src.modules.hindi_preprocessing import clean_hindi_text, tokenize_hindi
from src.modules.hindi_lexicon_detector import detect_hindi_lexicon
from src.modules.hindi_causality_extractor import extract_hindi_causality
from src.modules.hindi_bias_detector import detect_hindi_bias
from src.modules.risk_scorer import calculate_risk
from src.modules.explanation_generator import generate_explanation

import logging

logger = logging.getLogger(__name__)

# ── Optional: import model for embedding (loaded lazily) ─────────────────────
_model_available = False
try:
    from src.models.hindi_model import encode_hindi
    _model_available = True
except ImportError:
    logger.warning(
        "Hindi model (ai4bharat/indic-bert) not available. "
        "Embeddings will be skipped. Install: pip install transformers torch sentencepiece"
    )


def run_hindi_pipeline(text: str) -> dict:
    """
    Run the complete Hindi analysis pipeline.

    Parameters
    ----------
    text : str
        Raw Hindi input text.

    Returns
    -------
    dict
        Analysis results including tokens, hits, risk, and explanation.
    """
    # 1 ── Clean & tokenize
    cleaned = clean_hindi_text(text)
    tokens = tokenize_hindi(text)

    import re
    sentences = [s.strip() for s in re.split(r'[.!?।]+', cleaned) if s.strip()]
    if not sentences:
        sentences = [cleaned]

    # 2 ── Embedding (optional — only if model is installed)
    embedding_shape = None
    if _model_available:
        try:
            embedding = encode_hindi(cleaned)
            embedding_shape = str(list(embedding.shape))
        except Exception as e:
            logger.error(f"Hindi embedding failed: {e}")
            embedding_shape = "error"

    # 3 ── Lexicon detection
    lexicon_results = detect_hindi_lexicon(tokens)
    lexicon_words = [hit["word"] for hit in lexicon_results]

    # 4 ── Causality extraction
    causality_hits = extract_hindi_causality(tokens)

    # 5 ── Bias detection
    bias_hits = detect_hindi_bias(tokens)

    # 6 ── Risk scoring (re-uses the shared scorer)
    risk = calculate_risk(lexicon_words, causality_hits, bias_hits)

    # 7 ── Explanation (re-uses the shared generator)
    explanation = generate_explanation(lexicon_words, causality_hits, bias_hits, risk)

    return {
        "language": "hindi",
        "cleaned_text": cleaned,
        "tokens": tokens,
        "sentences": sentences,
        "lexicon_hits": lexicon_words,
        "causality_hits": causality_hits,
        "bias_hits": bias_hits,
        "risk": risk,
        "explanation": explanation,
        "embedding_shape": embedding_shape,
    }
