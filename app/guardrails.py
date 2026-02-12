def check_guardrail(scores, threshold=2.0):
    # L2 distance: lower is better
    return float(scores[0]) < threshold


def confidence_score(score):
    score = float(score)

    # convert L2 distance to confidence
    conf = 1 / (1 + score)
    return round(conf * 100, 2)
