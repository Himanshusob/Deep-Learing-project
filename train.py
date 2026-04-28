import os
import matplotlib.pyplot as plt
import tensorflow as tf
# from dataset_loader import load_dataset, get_splits
from src.dataset_loader import load_dataset, get_splits

# from model import build_cnn
from src.model import build_cnn


def train(ela_dir, epochs=10, batch_size=16):
    X, y, class_map = load_dataset(ela_dir)
    X_train, X_val, X_test, y_train, y_val, y_test = get_splits(X, y)

    model = build_cnn(input_shape=X.shape[1:])
    model.summary()

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(X_val, y_val))

    os.makedirs("checkpoints", exist_ok=True)
    model.save("checkpoints/final_model.h5")

    loss, acc = model.evaluate(X_test, y_test)
    print("Test Accuracy:", acc)

    return model
