# src/noise.py
import cv2
import numpy as np

def local_noise_variance_map(image_path, block_size=16):
    """
    Compute local variance (noise) heatmap by splitting image into blocks.
    Returns heatmap (as uint8 image) and mean local variance value (float).
    """
    img = cv2.imread(image_path)
    if img is None:
        return None, 0.0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape
    # pad to multiple of block_size
    pad_h = (block_size - (h % block_size)) % block_size
    pad_w = (block_size - (w % block_size)) % block_size
    gray_p = np.pad(gray, ((0,pad_h),(0,pad_w)), mode='reflect')
    H, W = gray_p.shape
    heat = np.zeros((H//block_size, W//block_size), dtype=np.float32)
    for i in range(0, H, block_size):
        for j in range(0, W, block_size):
            block = gray_p[i:i+block_size, j:j+block_size]
            heat[i//block_size, j//block_size] = np.var(block)
    # normalize heat to 0-255 for display
    hmin, hmax = heat.min(), heat.max()
    if hmax - hmin > 0:
        norm = (heat - hmin) / (hmax - hmin)
    else:
        norm = heat - hmin
    heat_img = (cv2.resize(norm, (w, h)) * 255).astype('uint8')
    # apply color map for visualization
    heat_color = cv2.applyColorMap(heat_img, cv2.COLORMAP_JET)
    mean_var = float(heat.mean())
    return heat_color, mean_var
