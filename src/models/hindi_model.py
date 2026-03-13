"""
Hindi Model Loader
==================
Loads the ai4bharat/indic-bert model and tokenizer from HuggingFace.
Provides a function to encode Hindi text into embeddings.
"""

from transformers import AutoTokenizer, AutoModel
import torch
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = "ai4bharat/IndicBERTv2-MLM-only"

# ── Lazy-load model & tokenizer (downloaded on first call) ───────────────────
_tokenizer = None
_model = None


def _load_model():
    """Load model and tokenizer lazily to avoid startup delay."""
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        logger.info(f"Loading Hindi model: {MODEL_NAME} ...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModel.from_pretrained(MODEL_NAME)
        _model.eval()  # set to evaluation mode
        logger.info("Hindi model loaded successfully.")


def encode_hindi(text: str) -> torch.Tensor:
    """
    Convert Hindi text → embedding vector (mean-pooled last hidden state).

    Parameters
    ----------
    text : str
        Input Hindi text.

    Returns
    -------
    torch.Tensor
        Shape [1, hidden_dim] embedding vector.
    """
    _load_model()

    inputs = _tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = _model(**inputs)

    # Mean-pool the last hidden states across the sequence dimension
    embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings


def get_token_embeddings(text: str):
    """
    Return per-token embeddings along with the decoded tokens.
    Useful for token-level analysis later (e.g., attention visualisation).

    Returns
    -------
    dict  {"tokens": list[str], "embeddings": torch.Tensor}
    """
    _load_model()

    inputs = _tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = _model(**inputs)

    token_ids = inputs["input_ids"][0].tolist()
    tokens = _tokenizer.convert_ids_to_tokens(token_ids)
    token_embeds = outputs.last_hidden_state[0]  # shape [seq_len, hidden_dim]

    return {"tokens": tokens, "embeddings": token_embeds}
