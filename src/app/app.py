from enum import Enum
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import matplotlib.pyplot as plt
import os
import yaml


# Read the configuration
with open("conf.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

app = Flask(__name__)


START_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
NUMBER_CLIENTS = cfg["NUMBER_CLIENTS"]
NUMBER_ROUNDS = cfg["NUMBER_ROUNDS"]
DATA_SIZE = [0] * NUMBER_CLIENTS
AGG_EXE = [False] * NUMBER_ROUNDS
RECEIVED = [[False for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
UPLOADED = [[False for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
ACCs = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
KAPPAs = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
F1s = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
AUCs = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
MPC_RUNNING = False


class ReportType(Enum):
    RECEIVED = "received"
    UPLOADED = "uploaded"
    FOR_ALPHA = "for_alpha"
    MPC_RUNNING = "mpc_running"


def get_and_validate_args(rargs) -> dict:
    cnum = rargs.get("cnum")
    rnum = rargs.get("rnum")
    dsize = rargs.get("dsize")  # optional, 0 by default
    acc = rargs.get("acc")
    kappa = rargs.get("kappa")
    f1 = rargs.get("f1")
    auc = rargs.get("auc")
    mpc_running = True if rargs.get("mpc_running") == "True" else False
    agg_exe = True if rargs.get("agg_exe") == "True" else False

    if not cnum:
        return {"error": "Set a variable cnum for your client number."}
    if not rnum:
        return {"error": "Set a variable rnum for the round number."}

    try:
        cnum, rnum, dsize, acc, kappa, f1, auc = int(cnum), int(rnum), int(dsize), float(acc), float(kappa), float(f1), float(auc)
        if 1 <= cnum <= NUMBER_CLIENTS and 1 <= rnum <= NUMBER_ROUNDS and 0 <= acc <= 1:
            return {
                "cnum": cnum - 1,
                "rnum": rnum - 1,
                "dsize": dsize,
                "acc": acc,
                "kappa": kappa,
                "f1": f1,
                "auc": auc,
                "mpc_running": mpc_running,
                "agg_exe": agg_exe
            }
        else:
            return {"error": "Invalid client, round and/or acc number."}
    except ValueError:
        return {"error": "Client and round numbers must be integers."}


@app.route('/')
def index():
    return 'Hello, HTTPS World!'


@app.route('/init')
def init():
    global DATA_SIZE, AGG_EXE, RECEIVED, UPLOADED, ACCs, KAPPAs, F1s, AUCs, MPC_RUNNING
    DATA_SIZE = [0] * NUMBER_CLIENTS
    AGG_EXE = [False] * NUMBER_ROUNDS
    RECEIVED = [[False for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
    UPLOADED = [[False for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
    ACCs = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
    KAPPAs = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
    F1s = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
    AUCs = [[0 for _ in range(NUMBER_CLIENTS)] for _ in range(NUMBER_ROUNDS)]
    MPC_RUNNING = False
    return jsonify(success=True)


@app.route('/report/<string:report_type>')
def report_status(report_type):
    args = get_and_validate_args(request.args)

    if "error" in args:
        return jsonify(args), 400

    global RECEIVED, UPLOADED, MPC_RUNNING

    if report_type == ReportType.RECEIVED.value:
        RECEIVED[args["rnum"]][args["cnum"]] = True
        DATA_SIZE[args["cnum"]] = args["dsize"]
        return jsonify(RECEIVED)

    elif report_type == ReportType.UPLOADED.value:
        UPLOADED[args["rnum"]][args["cnum"]] = True
        ACCs[args["rnum"]][args["cnum"]] = args["acc"]
        KAPPAs[args["rnum"]][args["cnum"]] = args["kappa"]
        F1s[args["rnum"]][args["cnum"]] = args["f1"]
        AUCs[args["rnum"]][args["cnum"]] = args["auc"]
        return jsonify(UPLOADED)

    elif report_type == ReportType.MPC_RUNNING.value:
        MPC_RUNNING = args["mpc_running"]
        AGG_EXE[args["rnum"]] = args["agg_exe"]
        return jsonify(AGG_EXE)

    else:
        return jsonify({"error": "Invalid report type."}), 400


@app.route('/status')
def get_status():
    return jsonify({
        "received": RECEIVED,
        "uploaded": UPLOADED,
        "mpc_running": MPC_RUNNING,
        "dsize": DATA_SIZE,
        "acc": ACCs,
        "kappa": KAPPAs,
        "f1": F1s,
        "auc": AUCs,
        "agg_exe": AGG_EXE,
        "start_time": START_TIME
    })


def create_avg_img():
    avg = [sum(sublist) / len(sublist) for sublist in ACCs]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(avg, marker='o', linestyle='-', color='b')
    plt.title('Average Accuracy Across Clients')
    plt.xlabel('at Round')
    plt.ylabel('Average Accuracy')
    plt.grid(True)

    # Save the plot to the 'static' directory
    if not os.path.exists('static'):
        os.makedirs('static')

    img_path = os.path.join('static', 'average_values_plot.png')
    plt.savefig(img_path)
    plt.close()


def create_kappa_img():
    kappa = [sum(sublist) / len(sublist) for sublist in KAPPAs]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(kappa, marker='o', linestyle='-', color='b')
    plt.title('Average Kappa score Across Clients')
    plt.xlabel('at Round')
    plt.ylabel('Average Kappa score')
    plt.grid(True)

    # Save the plot to the 'static' directory
    if not os.path.exists('static'):
        os.makedirs('static')

    img_path = os.path.join('static', 'kappa_values_plot.png')
    plt.savefig(img_path)
    plt.close()


def create_f1_img():
    f1 = [sum(sublist) / len(sublist) for sublist in F1s]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(f1, marker='o', linestyle='-', color='b')
    plt.title('Average F1 score Across Clients')
    plt.xlabel('at Round')
    plt.ylabel('Average F1 score')
    plt.grid(True)

    # Save the plot to the 'static' directory
    if not os.path.exists('static'):
        os.makedirs('static')

    img_path = os.path.join('static', 'f1_values_plot.png')
    plt.savefig(img_path)
    plt.close()


def create_auc_img():
    auc = [sum(sublist) / len(sublist) for sublist in AUCs]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(auc, marker='o', linestyle='-', color='b')
    plt.title('Average AUC Across Clients')
    plt.xlabel('at Round')
    plt.ylabel('Average Accuracy')
    plt.grid(True)

    # Save the plot to the 'static' directory
    if not os.path.exists('static'):
        os.makedirs('static')

    img_path = os.path.join('static', 'auc_values_plot.png')
    plt.savefig(img_path)
    plt.close()


@app.route('/acc')
def show_avg():
    create_avg_img()
    return send_from_directory('static', 'average_values_plot.png')


@app.route('/kappa')
def show_kappa():
    create_kappa_img()
    return send_from_directory('static', 'kappa_values_plot.png')


@app.route('/f1')
def show_f1():
    create_f1_img()
    return send_from_directory('static', 'f1_values_plot.png')


@app.route('/auc')
def show_auc():
    create_auc_img()
    return send_from_directory('static', 'auc_values_plot.png')


if __name__ == '__main__':
    # app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=8443)
    app.run(host='0.0.0.0', port=8443)
