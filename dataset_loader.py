import os, numpy as np, cv2
from sklearn.model_selection import train_test_split

def load_dataset(ela_dir, size=(128,128)):
    X, y = [], []
    classes = sorted(os.listdir(ela_dir))
    class_map = {}

    for idx, cls in enumerate(classes):
        class_map[idx] = cls
        cls_path = os.path.join(ela_dir, cls)

        for f in os.listdir(cls_path):
            p = os.path.join(cls_path, f)
            try:
                img = cv2.imread(p)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, size)
                X.append(img)
                y.append(idx)
            except:
                pass

    X = np.array(X, dtype=np.float32) / 255.0
    y = np.array(y)

    return X, y, class_map


def get_splits(X, y, test_size=0.2, val_size=0.1):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size+val_size, stratify=y)
    rel_val = val_size / (test_size + val_size)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=1-rel_val, stratify=y_temp)
    return X_train, X_val, X_test, y_train, y_val, y_test
