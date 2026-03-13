def generate_explanation(lexicon_hits, causality_hits, bias_hits, risk):
    explanation = []

    if lexicon_hits:
        explanation.append(
            f"Influence-related terms detected: {', '.join(lexicon_hits)}."
        )

    if causality_hits:
        explanation.append(
            f"Causal reasoning indicators found: {', '.join(causality_hits)}."
        )

    if bias_hits:
        explanation.append(
            f"Absolute or biased language detected: {', '.join(bias_hits)}."
        )

    explanation.append(
        f"Overall risk level assessed as {risk['risk_level']}."
    )

    return " ".join(explanation)
