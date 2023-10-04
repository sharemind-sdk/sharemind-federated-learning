import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pickle
from keras.datasets import mnist, fashion_mnist, cifar10
from keras.utils import to_categorical
from sklearn.utils import shuffle

import common as cm


DATA_FOLDER = f"{cm.PROJECT_PATH}/data"

if __name__ == "__main__":
    # MNIST
    (train_X, train_y), (test_X, test_y) = mnist.load_data()
    print("MNIST dataset")
    print(f"training dataset size: {len(train_y)}, test dataset size: {len(test_y)}")

    # reshape and rescale
    train_X = train_X.reshape((60000, 28, 28, 1))
    train_X = train_X.astype('float32') / 255

    test_X = test_X.reshape((10000, 28, 28, 1))
    test_X = test_X.astype('float32') / 255

    # Convert labels to one-hot encoded format
    train_y = to_categorical(train_y)
    test_y = to_categorical(test_y)

    # Shuffle
    train_X, train_y = shuffle(train_X, train_y, random_state=42)
    test_X, test_y = shuffle(test_X, test_y, random_state=42)

    # Split into 3
    train_Xs = np.array_split(train_X, 3)
    train_ys = np.array_split(train_y, 3)
    test_Xs = np.array_split(test_X, 3)
    test_ys = np.array_split(test_y, 3)

    for i in range(3):
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/mnist/x_train.pickle", 'wb') as f:
            pickle.dump(train_Xs[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/mnist/x_test.pickle", 'wb') as f:
            pickle.dump(test_Xs[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/mnist/y_train.pickle", 'wb') as f:
            pickle.dump(train_ys[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/mnist/y_test.pickle", 'wb') as f:
            pickle.dump(test_ys[i], f)

    # fashion MNIST
    (train_X, train_y), (test_X, test_y) = fashion_mnist.load_data()
    print("fashion MNIST dataset")
    print(f"training dataset size: {len(train_y)}, test dataset size: {len(test_y)}")

    # reshape and rescale
    train_X = train_X.reshape((60000, 28, 28, 1))
    train_X = train_X.astype('float32') / 255

    test_X = test_X.reshape((10000, 28, 28, 1))
    test_X = test_X.astype('float32') / 255

    # Convert labels to one-hot encoded format
    train_y = to_categorical(train_y)
    test_y = to_categorical(test_y)

    # Shuffle
    train_X, train_y = shuffle(train_X, train_y, random_state=42)
    test_X, test_y = shuffle(test_X, test_y, random_state=42)

    # Split into 3
    train_Xs = np.array_split(train_X, 3)
    train_ys = np.array_split(train_y, 3)
    test_Xs = np.array_split(test_X, 3)
    test_ys = np.array_split(test_y, 3)

    for i in range(3):
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/fashion/x_train.pickle", 'wb') as f:
            pickle.dump(train_Xs[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/fashion/x_test.pickle", 'wb') as f:
            pickle.dump(test_Xs[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/fashion/y_train.pickle", 'wb') as f:
            pickle.dump(train_ys[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/fashion/y_test.pickle", 'wb') as f:
            pickle.dump(test_ys[i], f)

    # CIFAR10
    (train_X, train_y), (test_X, test_y) = cifar10.load_data()  # (50000, 32, 32, 3), (50000, 1), (10000, 32, 32, 3), (10000, 1)
    print("CIFAR10 dataset")
    print(f"training dataset size: {len(train_y)}, test dataset size: {len(test_y)}")

    # scale
    train_X = train_X.astype('float32') / 255
    test_X = test_X.astype('float32') / 255

    # Convert labels to one-hot encoded format
    train_y = to_categorical(train_y)  # (50000, 10)
    test_y = to_categorical(test_y)    # (10000, 10)

    # Shuffle
    train_X, train_y = shuffle(train_X, train_y, random_state=42)
    test_X, test_y = shuffle(test_X, test_y, random_state=42)

    # Split into 3
    train_Xs = np.array_split(train_X, 3)
    train_ys = np.array_split(train_y, 3)
    test_Xs = np.array_split(test_X, 3)
    test_ys = np.array_split(test_y, 3)

    for i in range(3):
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/cifar10/x_train.pickle", 'wb') as f:
            pickle.dump(train_Xs[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/cifar10/x_test.pickle", 'wb') as f:
            pickle.dump(test_Xs[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/cifar10/y_train.pickle", 'wb') as f:
            pickle.dump(train_ys[i], f)
        with open(f"{cm.PROJECT_PATH}/client/client{i + 1}/data/local/cifar10/y_test.pickle", 'wb') as f:
            pickle.dump(test_ys[i], f)
