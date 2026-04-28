# src/clone_detect.py
import cv2
import numpy as np

def detect_clone_matches(image_path, min_matches=10):
    """
    Simple copy-move style detection using ORB keypoints + BFMatcher.
    Returns number_of_good_matches (int) and an image with matches drawn (optional).
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return 0, None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ORB detector
        orb = cv2.ORB_create(2000)
        kp, des = orb.detectAndCompute(gray, None)
        if des is None or len(kp) < 10:
            return 0, None
        # BFMatcher with Hamming
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        matches = bf.knnMatch(des, des, k=2)
        # We must filter out trivial matches (a point matched with itself) and duplicates.
        good = []
        for m,n in matches:
            # ignore match to itself (same index)
            if m.trainIdx == m.queryIdx:
                continue
            if m.distance < 0.75 * n.distance:
                # ensure spatial distance between keypoints large enough (to avoid neighbor matches)
                p1 = kp[m.queryIdx].pt
                p2 = kp[m.trainIdx].pt
                dx = p1[0]-p2[0]; dy = p1[1]-p2[1]
                if (dx*dx + dy*dy) > 25:  # at least 5px apart
                    good.append((m, kp[m.queryIdx], kp[m.trainIdx]))
        n_good = len(good)
        # optional draw first 50 matches
        match_img = None
        try:
            if n_good > 0:
                draw_matches = min(50, n_good)
                # create dummy matches list for drawMatches
                mlist = [g[0] for g in good[:draw_matches]]
                match_img = cv2.drawMatches(img, kp, img, kp, mlist, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        except Exception:
            match_img = None
        return n_good, match_img
    except Exception:
        return 0, None
