def check_guardrail(scores, threshold=1.2):

    score = float(scores[0])  # convert here

    if score > threshold:
        return False
    return True


def confidence_score(score):

    score = float(score)  # convert here

    conf = 1 / (1 + score)
    return round(conf * 100, 2)
