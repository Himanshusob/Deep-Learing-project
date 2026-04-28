import cv2, os
# from ela import convert_to_ela_pil
from src.ela import convert_to_ela_pil


def process_and_save_ela(src_dir, dst_dir, size=(128,128), quality=90):
    os.makedirs(dst_dir, exist_ok=True)
    for cls in os.listdir(src_dir):
        class_src = os.path.join(src_dir, cls)
        if not os.path.isdir(class_src):
            continue
        class_dst = os.path.join(dst_dir, cls)
        os.makedirs(class_dst, exist_ok=True)

        for fname in os.listdir(class_src):
            src_path = os.path.join(class_src, fname)
            try:
                ela_arr = convert_to_ela_pil(src_path, quality=quality)
                ela_resized = cv2.resize(ela_arr, size)
                dst_path = os.path.join(class_dst, os.path.splitext(fname)[0] + ".jpg")
                cv2.imwrite(dst_path, cv2.cvtColor(ela_resized, cv2.COLOR_RGB2BGR))
            except Exception as e:
                print("Skipping", src_path, "err:", e)
