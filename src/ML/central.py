import json
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from keras.models import clone_model
import tensorflow as tf
import tensorflow_addons as tfa
from enum import Enum
from sklearn.metrics import cohen_kappa_score
import time

import ml
import common as cm


class DATASET(Enum):
    MNIST = 1
    FASHION = 2
    CIFAR10 = 3
    CASA = 4


DATA_FOLDER = f"{cm.PROJECT_PATH}/data"


def central_train(ds_type: DATASET, epoch: int):
    if ds_type == DATASET.MNIST:
        ds = "mnist"
        model = ml.create_init_model_mnist()
        num_classes = 10
    elif ds_type == DATASET.FASHION:
        ds = "fashion"
        model = ml.create_init_model_fashion()
        num_classes = 10
    elif ds_type == DATASET.CIFAR10:
        ds = "cifar10"
        model = ml.create_init_model_cifar10()
        num_classes = 10
    elif ds_type == DATASET.CASA:
        ds = "casa"
        model = ml.create_init_model_casa()
        num_classes = 10

    print(model.summary())
    data_common_path = f"{cm.PROJECT_PATH}/client"

    METRICSs = [
        'accuracy',
        tfa.metrics.F1Score(num_classes=num_classes, average='macro'),
        tf.keras.metrics.AUC()
    ]

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    X_trains = []
    X_tests = []
    y_trains = []
    y_tests = []
    for c in range(1, 4):  # Client number
        with open(f"{data_common_path}/client{c}/data/local/{ds}/x_train.pickle", 'rb') as f:
            X_trains.append(pickle.load(f))
        with open(f"{data_common_path}/client{c}/data/local/{ds}/x_test.pickle", 'rb') as f:
            X_tests.append(pickle.load(f))
        with open(f"{data_common_path}/client{c}/data/local/{ds}/y_train.pickle", 'rb') as f:
            y_trains.append(pickle.load(f))
        with open(f"{data_common_path}/client{c}/data/local/{ds}/y_test.pickle", 'rb') as f:
            y_tests.append(pickle.load(f))

    X_train = np.vstack(X_trains)
    X_test = np.vstack(X_tests)
    y_train = np.vstack(y_trains)
    y_test = np.vstack(y_tests)

    start = time.time()

    history = model.fit(
        X_train,
        y_train,
        epochs=epoch,
        validation_data=(X_test, y_test),
        verbose=1  # progress bar
    )

    # Evaluate the model
    score = model.evaluate(X_test, y_test, verbose=0)
    # Get class labels
    class_true = np.argmax(y_test, axis=-1)
    class_labels = np.argmax(model.predict(X_test), axis=-1)

    score = {
        "acc": score[1],
        "f1": score[2],
        "auc": score[3],
        "kappa": cohen_kappa_score(class_true, class_labels),
        "time": time.time() - start
    }
    print(ds)
    print(history.history["val_accuracy"])
    print(history.history["val_f1_score"])

    with open(f"{cm.PROJECT_PATH}/result/local/{ds}/central.json", 'w') as fp:
        json.dump(score, fp)

    return score


if __name__ == "__main__":
    # central

    epoch = 200
    central_train(DATASET.MNIST, epoch)
    central_train(DATASET.FASHION, epoch)
    central_train(DATASET.CIFAR10, epoch)
