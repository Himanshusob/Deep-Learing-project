# src/exif.py
from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif_summary(image_path):
    """
    Return dict summary of basic EXIF fields (camera, datetime, software).
    If no EXIF found -> return empty dict.
    """
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return {}
        summary = {}
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            # Keep only useful small set
            if tag in ("Make","Model","DateTime","Software","Artist","Copyright"):
                summary[tag] = str(value)
        return summary
    except Exception:
        return {}
