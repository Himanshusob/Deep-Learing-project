

def score_from_ela_variance(ela_variance):

    v = ela_variance

    if v < 50:
        return 95

    elif v < 150:
        return 80

    elif v < 400:
        return 60

    elif v < 800:
        return 40

    else:
        return 20

def score_from_exif(exif_summary):
    """
    If EXIF exists -> slightly higher trust. If missing, neutral.
    Return 0-100 (higher = more trust).
    """
    if not exif_summary:
        return 50.0
    # if camera model exists -> 80, else 60
    if "Model" in exif_summary or "Make" in exif_summary:
        return 85.0
    return 65.0

def score_from_clone_matches(n_matches):
    """
    If many clone matches -> low trust. We'll convert matches -> score (higher matches -> lower score).
    """
    if n_matches <= 0:
        return 100.0
    # For 0..200 matches map -> 100..0
    m = float(min(200, n_matches))
    score = (1.0 - (m / 200.0)) * 100.0
    return max(0.0, min(100.0, score))

# def score_from_noise(mean_local_variance):
#     """
#     Higher mean variance maybe indicates natural noise -> more trustworthy.
#     We'll map mean variance [0..300] to [0..100].
#     """
#     v = max(0.0, min(300.0, mean_local_variance))
#     return (v / 300.0) * 100.0

def score_from_noise(v):

    if v < 50:
        return 20

    elif v < 150:
        return 40

    elif v < 300:
        return 60

    elif v < 600:
        return 80

    else:
        return 95

def weighted_authenticity(ela_s, exif_s, clone_s, noise_s, weights=None):
    """
    Combine scores into final authenticity score (0..100)
    By default weights: ELA 30%, EXIF 10%, Clone 40%, Noise 20%
    """
    if weights is None:
        weights = {'ela':0.30, 'exif':0.10, 'clone':0.40, 'noise':0.20}
    final = (ela_s * weights['ela'] +
             exif_s * weights['exif'] +
             clone_s * weights['clone'] +
             noise_s * weights['noise'])
    return float(max(0.0, min(100.0, final)))
