BIAS_WORDS = [
    "always",
    "never",
    "everyone",
    "nobody",
    "obviously"
]

def detect_bias(tokens):
    bias_hits = []
    for word in tokens:
        if word.lower() in BIAS_WORDS:
            bias_hits.append(word)
    return bias_hits
