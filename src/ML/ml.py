"""
Specialized to Diabetes datasets.
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from os.path import isfile, join
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, BatchNormalization, Dropout, LSTM
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Activation
from enum import Enum
from typing import Tuple
from sklearn.metrics import cohen_kappa_score
import pandas as pd
import pickle
import tensorflow as tf
import tensorflow_addons as tfa
import numpy as np

import common as cm


MODEL_NAME = f"{cm.PROJECT_PATH}/src/ML/{cm.CFG['DATA']}.keras"
num_classes = 47 if cm.CFG["DATA"] == "emnist" else 10
METRICSs = [
    'accuracy',
    tfa.metrics.F1Score(num_classes=num_classes, average='macro'),
    tf.keras.metrics.AUC()
]


class ModelType(Enum):
    INIT = 1
    GLOBAL = 2


cfg = {
    'VGG11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'VGG19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}


def read_all_datasets(client_name) -> Tuple[pd.DataFrame, ...]:
    common_path = f"{cm.PROJECT_PATH}/client/{client_name}/data/local"
    if cm.CFG["DATA"] == "diabetes":
        X_train = pd.read_csv(f"{common_path}/diabetes/x_train.csv", index_col=False, header=None)
        X_test = pd.read_csv(f"{common_path}/diabetes/x_test.csv", index_col=False, header=None)
        y_train = pd.read_csv(f"{common_path}/diabetes/y_train.csv", index_col=False, header=None)
        y_test = pd.read_csv(f"{common_path}/diabetes/y_test.csv", index_col=False, header=None)
    else:
        dataset = cm.CFG["DATA"]
        with open(f"{common_path}/{dataset}/x_train.pickle", 'rb') as f:
            X_train = pickle.load(f)
        with open(f"{common_path}/{dataset}/x_test.pickle", 'rb') as f:
            X_test = pickle.load(f)
        with open(f"{common_path}/{dataset}/y_train.pickle", 'rb') as f:
            y_train = pickle.load(f)
        with open(f"{common_path}/{dataset}/y_test.pickle", 'rb') as f:
            y_test = pickle.load(f)

    return X_train, X_test, y_train, y_test


def create_init_model_diabetes():
    """
    This must be done on Sharemind.
    """
    # create a neural network
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def create_init_model_mnist():
    """
    This must be done on Sharemind.
    """
    # create a neural network
    # model = Sequential()
    # model.add(Flatten(input_shape=(28, 28)))
    # model.add(Dense(128, activation='relu'))
    # model.add(Dense(10, activation='softmax'))

    # CNN
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),)
    model.add(MaxPooling2D((2, 2)),)
    model.add(Conv2D(64, (3, 3), activation="relu"),)
    model.add(MaxPooling2D((2, 2)),)
    model.add(Conv2D(64, (3, 3), activation="relu"),)
    model.add(Flatten(),)
    model.add(Dense(64, activation="relu"),)
    model.add(Dense(10, activation="softmax"))

    # compile the keras model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def create_init_model_emnist():
    """
    This must be done on Sharemind.
    """
    # create a neural network
    # CNN
    # Input Layer
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))

    # Second Convolutional Layer
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))

    # Third Convolutional Layer
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))

    # Flatten Layer
    model.add(Flatten())

    # Fully Connected Layer
    model.add(Dense(128, activation="relu"))
    model.add(BatchNormalization())

    # Output Layer
    model.add(Dense(47, activation="softmax"))

    # compile the keras model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def create_init_model_fashion():
    """
    This must be done on Sharemind.
    """
    # create a neural network

    # CNN
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),)
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)),)
    model.add(Conv2D(64, (3, 3), activation="relu"),)
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)),)
    model.add(Conv2D(64, (3, 3), activation="relu"),)
    model.add(Flatten(),)
    model.add(Dense(64, activation="relu"),)
    model.add(Dense(10, activation="softmax"))

    # compile the keras model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def create_init_model_cifar10(input_shape=(32, 32, 3), dimension='VGG11'):
    """
    This must be done on Sharemind.
    """
    ## Sharemind cannot handle this. too large to download...
    # model = Sequential()
    # model.add(Input(shape=input_shape))

    # for x in cfg[dimension]:
    #     if x == 'M':
    #         model.add(MaxPooling2D(pool_size=(2, 2)))
    #     else:
    #         model.add(Conv2D(x, (3, 3), padding='same', trainable=True))
    #         model.add(BatchNormalization(trainable=True))
    #         model.add(Activation(activations.relu))

    # model.add(AveragePooling2D(pool_size=(1, 1)))
    # model.add(Flatten())
    # model.add(Dense(10, activation='softmax'))

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))

    # Second Convolutional Layer
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.3))

    # Third Convolutional Layer
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.3))

    # Flatten Layer
    model.add(Flatten())

    # Fully Connected Layer
    model.add(Dense(128, activation="relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))

    # Output Layer
    model.add(Dense(10, activation="softmax"))

    # compile the keras model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def create_init_model_casa():
    model = Sequential()
    model.add(LSTM(100, input_shape=(1, 36)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def get_model():
    if os.path.exists(MODEL_NAME):
        model = load_model(MODEL_NAME)
    else:
        if cm.CFG["DATA"] == "diabetes":
            print("Creating an init model for diabetes dataset.")
            model = create_init_model_diabetes()
        elif cm.CFG["DATA"] == "mnist":
            print("Creating an init model for MNIST dataset.")
            model = create_init_model_mnist()
        elif cm.CFG["DATA"] == "fashion":
            print("Creating an init model for fashion dataset.")
            model = create_init_model_fashion()
        elif cm.CFG["DATA"] == "emnist":
            print("Creating an init model for emnist dataset.")
            model = create_init_model_emnist()
        elif cm.CFG["DATA"] == "cifar10":
            print("Creating an init model for cifar10 dataset.")
            model = create_init_model_cifar10()
        elif cm.CFG["DATA"] == "casa":
            print("Creating an init model for casa dataset.")
            model = create_init_model_casa()
        else:
            print("Currently DATA in conf.yml must be either 'diabetes', 'mnist', or 'fashion'")
            raise
        model.save(MODEL_NAME)

    return model


def get_model_shape() -> dict:
    model_shape = {}
    with open(f"{cm.PROJECT_PATH}/client/model.txt", 'r') as f:
        layers = f.read().split("|")
        for i, layer in enumerate(layers):
            if i < 10:
                i = f"0{i}"
            model_shape[f"layer-{i}"] = tuple(int(x) for x in layer.split(','))

    return model_shape


def load_all_pickles(model_type: ModelType, client: str) -> dict:
    if model_type == ModelType.INIT:
        prefix = "init"
    else:
        prefix = "global"

    layers = {}
    path = f"{cm.PROJECT_PATH}/client/{client}/models/recv"
    files = [f for f in os.listdir(path) if isfile(join(path, f))]

    for file in files:
        if prefix in file:
            filename = f"{path}/{file}"
            with open(filename, 'rb') as f:
                layers[file.split(".")[1]] = pickle.load(f)

    # sort the layers(dict)
    layers = dict(sorted(layers.items()))

    return layers


def check_layer_has_weight(layer):
    if isinstance(layer, Flatten):
        return False
    elif isinstance(layer, Activation):
        return False
    elif isinstance(layer, MaxPooling2D):
        return False
    elif isinstance(layer, AveragePooling2D):
        return False
    elif isinstance(layer, Dropout):
        return False

    return True


def reconstruct_from_pickle(client: str, model_type: ModelType):
    model = get_model()
    layers = load_all_pickles(model_type, client)
    layers = list(layers.values())

    # Check their shapes
    for i, weight in enumerate(model.get_weights()):
        assert layers[i].shape == weight.shape

    # Reconstruct the model
    j = 0
    for i in range(len(model.layers)):
        if check_layer_has_weight(model.layers[i]):
            if isinstance(model.layers[i], BatchNormalization):
                # this has 4 weights
                model.layers[i].set_weights([layers[j], layers[j + 1], layers[j + 2], layers[j + 3]])
                j += 4
            elif isinstance(model.layers[i], LSTM):
                # this has 3 weights
                model.layers[i].set_weights([layers[j], layers[j + 1], layers[j + 2]])
                j += 3
            else:
                model.layers[i].set_weights([layers[j], layers[j + 1]])
                j += 2

    # Recompile it
    if cm.CFG["DATA"] == "diabetes":
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=METRICSs)
    else:
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=METRICSs)

    return model


def train(client_name, model):
    """
    For convenience, this returns the updated model, score, and the size of training datasets.
    """
    X_train, X_test, y_train, y_test = read_all_datasets(client_name)
    model.fit(
        X_train,
        y_train,
        epochs=2,
        validation_data=(X_test, y_test)
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
        "kappa": cohen_kappa_score(class_true, class_labels)
    }

    return model, score


def get_dsize():
    client_name = cm.CLIENT_NAME
    common_path = f"{cm.PROJECT_PATH}/client/{client_name}/data/local"
    if cm.CFG["DATA"] == "diabetes":
        return len(pd.read_csv(f"{common_path}/diabetes/y_train.csv", index_col=False))
    elif cm.CFG["DATA"] == "mnist":
        with open(f"{common_path}/mnist/y_train.pickle", 'rb') as f:
            return len(pickle.load(f))
    elif cm.CFG["DATA"] == "fashion":
        with open(f"{common_path}/fashion/y_train.pickle", 'rb') as f:
            return len(pickle.load(f))
    elif cm.CFG["DATA"] == "emnist":
        with open(f"{common_path}/emnist/y_train.pickle", 'rb') as f:
            return len(pickle.load(f))
    elif cm.CFG["DATA"] == "cifar10":
        with open(f"{common_path}/cifar10/y_train.pickle", 'rb') as f:
            return len(pickle.load(f))
    elif cm.CFG["DATA"] == "casa":
        with open(f"{common_path}/casa/y_train.pickle", 'rb') as f:
            return len(pickle.load(f))
    else:
        print("DATA in conf.yml must be either 'diabetes','mnist', or 'fashion' so far.")


def save_weights_to_csv(client_number, model, dsizes):
    """
    Weighted Average.
    Saves weights as vectors, even if not vectors.
    """
    this_weight = dsizes[int(client_number) - 1] / sum(dsizes)

    for i, weight in enumerate(model.get_weights()):
        if i < 10:
            i = f"0{i}"

        filename = f"layer-{i}.csv"
        path = f"{cm.PROJECT_PATH}/client/client{client_number}/models/local"

        df = pd.DataFrame(weight.reshape(-1), columns=["col0"])

        df *= this_weight
        df.to_csv(f"{path}/{filename}", index=False)


if __name__ == "__main__":
    # For debugging
    client_name = "client1"

    # model = reconstruct_from_pickle(client_name, ModelType.INIT)
    model = get_model()
    print(model.summary())
    for i, weight in enumerate(model.get_weights()):
        print(f"Layer: {i}, Shape: {weight.shape}")

    for i, l in enumerate(model.layers):
        print(f"Layer: {i}, type: {type(l)}")
        print(len(l.get_weights()))
        if isinstance(l, BatchNormalization):
            ww = l.get_weights()
            for w in ww:
                print(w)

    print("|".join([",".join(map(str, tup)) for tup in [w.shape for w in model.get_weights()]]))

    # updated, score = train(client_name, model)

    # print('Test loss:', score[0])
    # print('Test accuracy:', score[1])

    # save_weights_to_csv(client_name, updated, [1, 1, 1])
