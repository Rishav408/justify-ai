CAUSAL_WORDS = [
    "because",
    "therefore",
    "thus",
    "hence",
    "due",
    "causes",
    "leads",
    "means",
    "since",
    "consequently",
    "so"
]

def extract_causality(tokens):
    detected = []
    for word in tokens:
        if word.lower() in CAUSAL_WORDS:
            detected.append(word)
    return detected
