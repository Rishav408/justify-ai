"""
Hindi Bias Detector
===================
Detects absolute, sweeping, or biased language markers in Hindi text.
"""

HINDI_BIAS_WORDS = [
    # Absolute quantifiers
    "हमेशा",        # always
    "कभी नहीं",     # never
    "सबको",         # everyone (accusative)
    "सभी",          # all / everyone
    "कोई नहीं",     # nobody
    "हर",           # every
    "हर एक",        # each and every
    "पूरा",         # entire / whole
    "पूरी",         # entire (fem.)
    "पूरे",         # entire (pl.)
    "सिर्फ",        # only
    "केवल",         # only (formal)
    "बिलकुल",       # absolutely
    "निश्चित",       # certainly
    "जरूर",         # surely
    "बेशक",         # undoubtedly
    "एकमात्र",      # sole / only
    "सारा",         # all (masc.)
    "सारी",         # all (fem.)
    "सारे",         # all (pl.)

    # Intensifiers that signal bias
    "बहुत",         # very / too much
    "अत्यंत",       # extremely
    "बिल्कुल",      # absolutely (alt)
    "पूर्ण रूप से",  # completely
    "सदैव",         # always (formal)
    "कदापि",        # ever / never (formal)
]


def detect_hindi_bias(tokens: list[str]) -> list[str]:
    """
    Detect biased / absolute language markers in Hindi tokens.
    Also checks for multi-word markers.
    """
    bias_hits = []

    for token in tokens:
        if token in HINDI_BIAS_WORDS:
            bias_hits.append(token)

    # Multi-word phrase matches
    text = " ".join(tokens)
    multi_word_markers = [m for m in HINDI_BIAS_WORDS if " " in m]
    for marker in multi_word_markers:
        if marker in text and marker not in bias_hits:
            bias_hits.append(marker)

    return bias_hits
