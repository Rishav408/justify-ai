"""
Hindi Causality Extractor
=========================
Detects causal / justification markers in Hindi text.
These words signal that the speaker is providing a *reason* for a claim.
"""

# ── Hindi causal / justification markers ─────────────────────────────────────
HINDI_CAUSAL_WORDS = [
    # Core causal connectors
    "क्योंकि",       # because
    "इसलिए",        # therefore
    "इसीलिए",       # that is why
    "अतः",          # hence (formal)
    "चूँकि",         # since / because (formal)
    "चूंकि",         # since / because (alt spelling)
    "फलस्वरूप",     # consequently
    "परिणामस्वरूप",  # as a result
    "इस कारण",      # for this reason
    "इस वजह से",    # because of this
    "की वजह से",    # because of
    "के कारण",      # due to
    "जिससे",        # so that / which led to
    "ताकि",         # so that
    "लिहाज़ा",       # therefore (Urdu-loan, common)
    "नतीजतन",       # consequently (Urdu-loan)
    "तो",           # so / then
    "इसका मतलब",    # this means
    "इसका अर्थ",    # this means (formal)
    "जब",           # when (temporal-causal)
    "अगर",          # if (conditional-causal)
    "यदि",          # if (formal)
    "तभी",          # only then
    "वरना",         # otherwise
    "क्योंकि यह",   # because this
]


def extract_hindi_causality(tokens: list[str]) -> list[str]:
    """
    Detect causal markers from Hindi tokens.
    Also checks for multi-word markers by re-joining tokens.
    """
    detected = []

    # Single-token matches
    for token in tokens:
        if token in HINDI_CAUSAL_WORDS:
            detected.append(token)

    # Multi-token phrase matches (bigrams / trigrams)
    text = " ".join(tokens)
    multi_word_markers = [
        m for m in HINDI_CAUSAL_WORDS if " " in m
    ]
    for marker in multi_word_markers:
        if marker in text and marker not in detected:
            detected.append(marker)

    return detected
