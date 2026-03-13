def calculate_risk(lexicon_hits, causality_hits, bias_hits):
    score = 0
    score += len(lexicon_hits) * 2
    score += len(causality_hits)
    score += len(bias_hits)

    if score < 3:
        level = "low"
    elif score < 6:
        level = "medium"
    else:
        level = "high"

    confidence = min(1.0, score / 10)

    return {
        "score": score,
        "risk_level": level,
        "confidence": confidence
    }
