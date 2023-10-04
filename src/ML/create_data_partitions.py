# The original version is from https://github.com/saadiabadi/Casa_IoT_Example/tree/main

import os
import pandas as pd
from math import floor
from pathlib import Path
import pickle

import common as cm


def import_data(test_ratio):
    """ Download data. """
    # data = pd.read_csv('http://archive.org/download/train_20211025/train.csv')
    data = pd.read_csv(f"{cm.PROJECT_PATH}/data/train.csv")
    data = data.sample(frac=1).reset_index(drop=True)
    print(data.head())

    num_test = int(test_ratio * data.shape[0])
    testset = data[:num_test]
    trainset = data[num_test:]
    return trainset, testset


def splitset(dataset, parts):
    n = dataset.shape[0]
    local_n = floor(n / parts)
    result = []
    for i in range(parts):
        result.append(dataset[i * local_n: (i + 1) * local_n])
    return result


if __name__ == '__main__':

    nr_of_datasets = 3

    trainset, testset = import_data(0.2)
    print('trainset', len(trainset))
    print('testset', len(testset))

    trainsets = splitset(trainset, nr_of_datasets)
    testsets = splitset(testset, nr_of_datasets)

    # for i in range(nr_of_datasets):
    #     cm_path = f'{cm.PROJECT_PATH}/client/client{i + 1}/data/local/casa'

    #     train_X = trainsets[i].iloc[:, 1:37].values.reshape(-1, 1, 36)
    #     train_y = trainsets[i].iloc[:, 37:]
    #     test_X = testsets[i].iloc[:, 1:37].values.reshape(-1, 1, 36)
    #     test_y = testsets[i].iloc[:, 37:]
    #     print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

    #     with open(f"{cm_path}/x_train.pickle", 'wb') as f:
    #         pickle.dump(train_X, f)
    #     with open(f"{cm_path}/y_train.pickle", 'wb') as f:
    #         pickle.dump(train_y, f)
    #     with open(f"{cm_path}/x_test.pickle", 'wb') as f:
    #         pickle.dump(test_X, f)
    #     with open(f"{cm_path}/y_test.pickle", 'wb') as f:
    #         pickle.dump(test_y, f)
