from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os

def convert_to_ela_pil(image_path, quality=90, enhance_factor=40):
    original = Image.open(image_path).convert('RGB')
    temp_path = image_path + ".temp.jpg"
    original.save(temp_path, 'JPEG', quality=quality)

    compressed = Image.open(temp_path)
    ela_image = ImageChops.difference(original, compressed)

    enhancer = ImageEnhance.Brightness(ela_image)
    ela_image = enhancer.enhance(enhance_factor)

    try:
        os.remove(temp_path)
    except:
        pass

    return np.array(ela_image)
