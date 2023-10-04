import pickle
import json
import os
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from sklearn.metrics import cohen_kappa_score
from keras.models import load_model

import common as cm
import ml


RESULT1 = {
    "acc": [],
    "kappa": [],
    "f1": [],
    "auc": [],
}
RESULT2 = {
    "acc": [],
    "kappa": [],
    "f1": [],
    "auc": [],
}
RESULT3 = {
    "acc": [],
    "kappa": [],
    "f1": [],
    "auc": [],
}


def local_train(client_name: str, iter: int, metrics: list):
    if client_name not in ["client1", "client2", "client3"]:
        return

    ds = cm.CFG['DATA']
    model_path = f"{cm.PROJECT_PATH}/client/{client_name}/models/local/{ds}.keras"

    if iter == 0:
        if ds == "mnist":
            model = ml.create_init_model_mnist()
            print("Model for MNSIT is created.")
        elif ds == "fashion":
            model = ml.create_init_model_fashion()
            print("Model for Fashion-MNSIT is created.")
        elif ds == "emnist":
            model = ml.create_init_model_emnist()
            print("Model for EMNSIT is created.")
        elif ds == "cifar10":
            model = ml.create_init_model_cifar10()
            print("Model for CIFAR10 is created.")
        elif ds == "casa":
            model = ml.create_init_model_casa()
            print("Model for CASA is created.")
    else:
        if os.path.exists(model_path):
            model = load_model(model_path)
        else:
            return

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=metrics)

    with open(f"{cm.PROJECT_PATH}/client/{client_name}/data/local/{ds}/x_train.pickle", 'rb') as f:
        X_train = pickle.load(f)
    with open(f"{cm.PROJECT_PATH}/client/{client_name}/data/local/{ds}/x_test.pickle", 'rb') as f:
        X_test = pickle.load(f)
    with open(f"{cm.PROJECT_PATH}/client/{client_name}/data/local/{ds}/y_train.pickle", 'rb') as f:
        y_train = pickle.load(f)
    with open(f"{cm.PROJECT_PATH}/client/{client_name}/data/local/{ds}/y_test.pickle", 'rb') as f:
        y_test = pickle.load(f)

    model.fit(
        X_train,
        y_train,
        epochs=2,
        validation_data=(X_test, y_test)
    )

    _, accuracy, f1, auc = model.evaluate(X_test, y_test)
    class_true = np.argmax(y_test, axis=-1)
    class_labels = np.argmax(model.predict(X_test), axis=-1)
    kappa = cohen_kappa_score(class_true, class_labels)
    print(f"acc: {accuracy}, kappa: {kappa}, f1: {f1}, auc: {auc}")

    if client_name == "client1":
        RESULT1["acc"].append(accuracy)
        RESULT1["kappa"].append(kappa)
        RESULT1["f1"].append(f1)
        RESULT1["auc"].append(auc)
    if client_name == "client2":
        RESULT2["acc"].append(accuracy)
        RESULT2["kappa"].append(kappa)
        RESULT2["f1"].append(f1)
        RESULT2["auc"].append(auc)
    if client_name == "client3":
        RESULT3["acc"].append(accuracy)
        RESULT3["kappa"].append(kappa)
        RESULT3["f1"].append(f1)
        RESULT3["auc"].append(auc)

    model.save(model_path)

    del X_train, y_train, X_test, y_test


def aggregate_avg():
    print("aggregating models...")
    model1_path = f"{cm.PROJECT_PATH}/client/client1/models/local/{cm.CFG['DATA']}.keras"
    model2_path = f"{cm.PROJECT_PATH}/client/client2/models/local/{cm.CFG['DATA']}.keras"
    model3_path = f"{cm.PROJECT_PATH}/client/client3/models/local/{cm.CFG['DATA']}.keras"
    model1 = load_model(model1_path)
    model2 = load_model(model2_path)
    model3 = load_model(model3_path)

    weights1 = model1.get_weights()
    weights2 = model2.get_weights()
    weights3 = model3.get_weights()

    # Taking the average of the weights
    avg_weights = [np.add(w1, np.add(w2, w3)) / 3. for w1, w2, w3 in zip(weights1, weights2, weights3)]

    # Create a new model to set the averaged weights
    global_model = model1
    global_model.set_weights(avg_weights)

    global_model.save(model1_path)
    global_model.save(model2_path)
    global_model.save(model3_path)

    print("A global model is created.")
    del model1, model2, model3, global_model


if __name__ == "__main__":
    ds = cm.CFG["DATA"]

    num_classes = 47 if ds == "emnist" else 10
    METRICSs = [
        'accuracy',
        tfa.metrics.F1Score(num_classes=num_classes, average='macro'),
        tf.keras.metrics.AUC()
    ]

    clients = ["client1", "client2", "client3"]
    nrounds = 200

    for i in range(nrounds):
        print()
        print(f"Round {i + 1}/{nrounds}")
        for c in clients:
            local_train(c, i, METRICSs)
        aggregate_avg()

    with open(f"{cm.PROJECT_PATH}/result/FL-plain/{ds}/result_client1.json", 'w') as fp:
        json.dump(RESULT1, fp)
    with open(f"{cm.PROJECT_PATH}/result/FL-plain/{ds}/result_client2.json", 'w') as fp:
        json.dump(RESULT2, fp)
    with open(f"{cm.PROJECT_PATH}/result/FL-plain/{ds}/result_client3.json", 'w') as fp:
        json.dump(RESULT3, fp)

    # Average of them
    RESULT = {}
    RESULT["acc"] = [(a + b + c) / 3 for a, b, c in zip(RESULT1["acc"], RESULT2["acc"], RESULT3["acc"])]
    RESULT["kappa"] = [(a + b + c) / 3 for a, b, c in zip(RESULT1["kappa"], RESULT2["kappa"], RESULT3["kappa"])]
    RESULT["f1"] = [(a + b + c) / 3 for a, b, c in zip(RESULT1["f1"], RESULT2["f1"], RESULT3["f1"])]
    RESULT["auc"] = [(a + b + c) / 3 for a, b, c in zip(RESULT1["auc"], RESULT2["auc"], RESULT3["auc"])]

    with open(f"{cm.PROJECT_PATH}/result/FL-plain/{ds}/result.json", 'w') as fp:
        json.dump(RESULT, fp)

    # print(RESULT)
