

import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from src.ela import convert_to_ela_pil
from src.exif import extract_exif_summary
from src.clone_detect import detect_clone_matches
from src.noise import local_noise_variance_map
from src.score import *

from src.localize import detect_forgery_regions
from src.explain import explain_result


def analyze_image_full(model_path, image_path):

    results = {}

    ela_arr = convert_to_ela_pil(image_path)

    ela_gray = cv2.cvtColor(ela_arr, cv2.COLOR_RGB2GRAY).astype(np.float32)
    ela_var = float(ela_gray.var())

    results['ela_arr'] = ela_arr
    results['ela_variance'] = ela_var

    exif = extract_exif_summary(image_path)
    results['exif'] = exif

    n_matches, clone_vis = detect_clone_matches(image_path)

    results['clone_matches'] = n_matches
    results['clone_vis'] = clone_vis

    noise_vis, mean_var = local_noise_variance_map(image_path)

    results['noise_vis'] = noise_vis
    results['noise_mean_var'] = mean_var

    pred_label = None
    pred_prob = None

    if os.path.exists(model_path):

        model = load_model(model_path)

        x = cv2.resize(ela_arr,(128,128)).astype("float32")/255.0
        x = np.expand_dims(x,axis=0)

        p = float(model.predict(x)[0][0])

        pred_prob = p
        pred_label = "fake" if p > 0.5 else "real"

    results['model_label'] = pred_label
    results['model_prob'] = pred_prob

    ela_score = score_from_ela_variance(ela_var)
    exif_score = score_from_exif(exif)
    clone_score = score_from_clone_matches(n_matches)
    noise_score = score_from_noise(mean_var)

    final_score = weighted_authenticity(
        ela_score,
        exif_score,
        clone_score,
        noise_score
    )

    results['scores'] = {
        "ela":ela_score,
        "exif":exif_score,
        "clone":clone_score,
        "noise":noise_score,
        "final":final_score
    }

    orig = cv2.imread(image_path)
    orig = cv2.cvtColor(orig,cv2.COLOR_BGR2RGB)

    localized_img,boxes = detect_forgery_regions(orig,ela_arr)

    results["localization"] = localized_img
    results["boxes"] = boxes

    explanation = explain_result(
        pred_label,
        results["scores"],
        ela_var,
        n_matches,
        mean_var
    )

    results["explanation"] = explanation

    return results

