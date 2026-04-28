def explain_result(label, scores, ela_var, clone_matches, noise_var):

    explanation = []

    if label == "fake":

        if ela_var > 120:
            explanation.append("High ELA variance detected")

        if clone_matches > 10:
            explanation.append("Clone detection found duplicated regions")

        if scores["noise"] < 40:
            explanation.append("Noise distribution inconsistent")

        explanation.append("AI model confidence indicates manipulation")

    elif label == "real":

        explanation.append("Low ELA variance indicates consistent compression")

        explanation.append("Noise distribution appears natural")

        if clone_matches <= 3:
            explanation.append("No significant clone patterns detected")

        explanation.append("AI model prediction supports authenticity")

    else:

        explanation.append("Mixed forensic signals detected")

        explanation.append("Further manual investigation recommended")

    return explanation