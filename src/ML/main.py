"""
Use fedmind/client/open_tmux.sh
"""
import os
import requests
import subprocess
from time import sleep
from datetime import datetime

import common as cm
import ml


SERVER_ENDPOINT = "http://172.20.0.3:8443"
REPORT_ENDPOINT = f"{SERVER_ENDPOINT}/report/"
STATUS_ENDPOINT = f"{SERVER_ENDPOINT}/status"


def generate_others(N):
    return {i: [j for j in range(1, N + 1) if j != i] for i in range(1, N + 1)}


OTHERS = generate_others(cm.CFG["NUMBER_CLIENTS"])


def delete_all_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Ensure the item is a file before deleting it
        if os.path.isfile(filepath):
            os.remove(filepath)


def report(
        rtype: cm.ReportType,
        cnum: int,
        rnum: int,
        dsize: int = 0,
        acc: float = 0,
        kappa: float = 0,
        f1: float = 0,
        auc: float = 0,
        mpc_running: bool = False,
        agg_exe: bool = False):

    params = {
        "cnum": cnum,
        "rnum": rnum,
        "dsize": dsize,
        "acc": acc,
        "kappa": kappa,
        "f1": f1,
        "auc": auc,
        "mpc_running": mpc_running,
        "agg_exe": agg_exe
    }

    # Report that you received a model from MPC safely
    response = requests.get(f"{REPORT_ENDPOINT}{rtype.value}", params=params)
    if not response.ok:
        raise Exception(f"Error when reporting {rtype}.")

    return response


def get_status():
    response = requests.get(STATUS_ENDPOINT)
    if not response.ok:
        raise Exception("Error when get the status.")

    return response.json()


def execute_cmd(script, client_number, flag=None):
    args = ["-c", str(client_number), "-f", flag] if flag else ["-c", str(client_number)]
    cmd = [script] + args
    return subprocess.run(cmd, capture_output=True, text=True)


def gen_xml_log(script):
    return subprocess.run(["python", script], capture_output=True, text=True)


if __name__ == "__main__":
    print(f"Using {cm.CFG['DATA']}")
    # Read the environment variable
    client_number = cm.CLIENT_NUMBER
    client_name = cm.CLIENT_NAME

    # Delete all pre/received models
    dirs = [
        f"{cm.PROJECT_PATH}/client/client{client_number}/models/recv",
        f"{cm.PROJECT_PATH}/client/client{client_number}/models/local",
        f"{cm.PROJECT_PATH}/client/client{client_number}/models/"
    ]
    for dir in dirs:
        delete_all_files(dir)

    # ROUND!
    script_path = f"{cm.PROJECT_PATH}/client/run_script.sh"
    importer_path = f"{cm.PROJECT_PATH}/client/importer.sh"
    py_xml_path = f"{cm.PROJECT_PATH}/src/ML/gen_importer.py"

    dsize = ml.get_dsize()

    for r in range(1, cm.CFG["NUMBER_ROUNDS"] + 1):
        flag = "init" if r == 1 else "global"
        res = execute_cmd(script_path, client_number, flag)
        report(cm.ReportType.RECEIVED, client_number, r, dsize)

        if r > 1:
            while True:
                status = get_status()
                if status["agg_exe"][r - 2]:
                    break
                if all(status["uploaded"][r - 2]):
                    # Tell the MPC to aggregate the model
                    report(cm.ReportType.MPC_RUNNING, client_number, r - 1, mpc_running=True)
                    res = execute_cmd(script_path, client_number, "agg")
                    report(cm.ReportType.MPC_RUNNING, client_number, r - 1, mpc_running=False, agg_exe=True)
                else:
                    print("Other parties have not uploaded. Waiting for 3 sec.")
                    sleep(3)

        # Now it gets the init/global model. Train/update it locally
        model = ml.reconstruct_from_pickle(client_name, ml.ModelType.INIT if r == 1 else ml.ModelType.GLOBAL)
        updated, scores = ml.train(client_name, model)

        # Save it locally. Weights will be diminished there according to the data size.
        ml.save_weights_to_csv(client_number, updated, get_status()["dsize"])

        # generate .xml and .log
        res = gen_xml_log(py_xml_path)

        # Upload to the MPC
        res = execute_cmd(importer_path, client_number)
        report(
            cm.ReportType.UPLOADED,
            client_number,
            r,
            acc=scores["acc"],
            kappa=scores["kappa"],
            f1=scores["f1"],
            auc=scores["auc"],
            dsize=dsize
        )
        print(res.stderr)

    # Out side of Rounds
    while True:
        status = get_status()
        if status["agg_exe"][r - 1]:
            break
        if all(status["uploaded"][r - 1]):
            # Tell the MPC to aggregate the model
            report(cm.ReportType.MPC_RUNNING, client_number, r, mpc_running=True)
            execute_cmd(script_path, client_number, "agg")
            report(cm.ReportType.MPC_RUNNING, client_number, r, mpc_running=False, agg_exe=True)
        else:
            print("Other parties have not uploaded. Waiting for 3 sec.")
            sleep(3)

    # Download th efinal global model
    execute_cmd(script_path, client_number, "global")

    print("FML is finished! Thanks:)")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
