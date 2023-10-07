# MPCFL: Towards Multi-party Computation for Secure Federated Learning Aggregation

This work aims to integrate MPC with FL, especially by using [Sharemind MPC](https://sharemind.cyber.ee/sharemind-mpc/), for secure FL aggregation. This repository builds off [SecreC language](https://sharemind-sdk.github.io/stdlib/reference/index.html), the domain specific language for Sharemind MPC. To have experiments, therefore, you need Sharemind MPC, its standard library and several licensed components (see below). Please refer and contact to <https://docs.sharemind.cyber.ee/> for this environment settings. You also need Docker.

## Software Architecture

There will be three FL clients, one control server, and three Sharemind MPC servers with two hundred communication rounds by default. You can set another communication round number in `conf.yml`. There you can also specify the number of clients, however, currently codes do not support numbers other than 3.

## How to run

The instructions below are only for reproducing the results of the paper. This repository assumes that users have three independent machine and control them by own. Therefore, some procedures are simplified and do not reflect reality (ex. key exchanges).

Also, to perform the following instructions with using Sharemind MPC, some licensed components are needed (in addtion to [SecreC Standard Library](https://sharemind-sdk.github.io/stdlib/reference/pages.html)). Those are
- Sharemind Application Server (for the `license.p7b`)
- SecreC Analytics Library for `analytics_common.sc` and `option.sc`.
- Sharemind CSV Importer

1. Create a virtual env and install Python libraries.

      ```sh
      $python3 -m venv venv
      $source ./venv/bin/activate
      $pip install -r ml.requirements.txt
      ```

2. Create necessary folders

      ```sh
      $./init.sh
      ```

3. Prepare the local datasets  
      See below for dataset details.

      ```sh
      # For MNIST, (Fashion-MNIST), CIFAR10 (script downloads and splits into train&test datasets)
      (venv)$python ./src/ML/split.py

      # For CASA (Human Activity Recognition from Continuous Ambient Sensor Data)
      # Download the dataset (127 MB):
      wget http://archive.org/download/train_20211025/train.csv
      # or curl -L http://archive.org/download/train_20211025/train.csv -o train.csv
      (venv)$python ./src/ML/create_data_partitions.py
      ```

4. Generate the model shape

      ```sh
      (venv)$python ./src/ML/gen_sample.py
      ```

   This script generates `./client/model.txt` which is sent to each Sharemind server to tell the model architecture in order to let them create the init model.

5. Generate the tailored access control confs based on the model

      ```sh
      (venv)$python ./src/ML/gen_access_ctl.py
      ```

6. Create keys.

      ```sh
      $./fake-key-change.sh
      ```

7. Add the `license-dev.p7b` to each `./server/server*/`.
   Sharemind servers can run now but we need tailored access control.

8. Exchange keys and send all necessary files to each server.
   Before the command below, enable ssh communication between the host and each machine.

      ```sh
      $./init-cluster.sh
      ```

9. Run Sharemind MPC

      ```sh
      # Login each server, move to the project folder and run
      $sh run.sh
      ```

10. Run FL with Sharemind MPC

      ```sh
      # This splits the terminal into four. Three for FL clients and one for the control server.
      # The Python environments are already activated. 
      # For the first time, one panel starts building a docker container and this takes a time.
      /client$./open_tmux.sh

      # Change the client-panel (ctrl+b and press the arrow-key) and start FL.
      $python ./src/ML/main.py
      ```

11. You can check the scores (<http://172.20.0.3:8443/status>) or each graph.

+ <http://172.20.0.3:8443/acc>
+ <http://172.20.0.3:8443/kappa>
+ <http://172.20.0.3:8443/f1>
+ <http://172.20.0.3:8443/auc>

   To create a comparison graph, save the <http://172.20.0.3:8443/status> as a `./result/FL-Sharemind/result.json`.

12. If necessary, you can check the central learning and FL but without using Sharemind.

      ```sh
      $python3 src/ML/central.py
      $python3 src/ML/FL-plain.py

      # plotting the results
      $python3 src/ML/result_plot.py
      ```

## Used Datasets
- [MNIST](https://keras.io/api/datasets/mnist/)
- [fashion MNIST](https://keras.io/api/datasets/fashion_mnist/)
- [CIFAR10](https://keras.io/api/datasets/cifar10/)

These three will be downloaded via Keras library once `./src/ML/split.py` is executed.
- Human Activity Recognition from Continuous Ambient Sensor Data (CASA)  
Original dataset can be found [here](https://archive.ics.uci.edu/dataset/506/human+activity+recognition+from+continuous+ambient+sensor+data) but we use [the pre-processed one](https://archive.org/download/train_20211025) that one of our authors Sadi AlAwadi, Halmstad University, made.

## Warning

Currently, there is, at least, one crucial bug. When you run the first, at the end of the first communication round, the program will crash. Please run again (the problem disappears).  
