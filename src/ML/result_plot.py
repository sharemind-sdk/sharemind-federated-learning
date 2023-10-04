import json
import numpy as np
import matplotlib.pyplot as plt
import common as cm

font = {'size': 22}

plt.rc('font', **font)

datasets = ["mnist"]
# datasets = ["mnist", "casa", "cifar10"]
metrics = ["acc", "kappa", "f1", "auc"]
models = ["central", "FL-plain", "FL-Sharemind"]
# Average acc of average acc across clients
for ds in datasets:
    # central training
    result_central = json.load(open(f"{cm.PROJECT_PATH}/result/local/{ds}/central.json"))

    # FL-plain
    result_plain = json.load(open(f"{cm.PROJECT_PATH}/result/FL-plain/{ds}/result.json"))

    # FL-sharemind
    result_sharemind = json.load(open(f"{cm.PROJECT_PATH}/result/FL-Sharemind/{ds}/result.json"))

    for met in ["acc", "kappa", "f1", "auc"]:
        plt.figure(figsize=(12, 7))
        r_s = [(a + b + c) / 3 for a, b, c in result_sharemind[met]]
        plt.axhline(y=result_central[met], linestyle="-", label="central", color="#1f77b4")
        plt.plot(range(1, len(result_plain[met]) + 1), result_plain[met], linestyle="--", label="FL-plain", color='#ff7f0e')
        plt.plot(range(1, len(r_s) + 1), r_s, linestyle="--", label="FL-Sharemind", color='#2ca02c')
        ds = "Fashion-MNIST" if ds == "fashion" else ds.upper()
        # plt.title(f"Accuracy on the {ds}")
        plt.xlabel("Round")
        plt.ylabel(met.capitalize() + " score")
        if ds == "MNIST":
            if met == "acc":
                plt.ylim(0.96, 1.)
            elif met == "kappa":
                plt.ylim(0.96, 1.)
            elif met == "f1":
                plt.ylim(0.96, 1.)
            elif met == "auc":
                plt.ylim(0.99, 1.)

        plt.legend()
        plt.savefig(f"{cm.PROJECT_PATH}/result/images/result_{met}_{ds}.png")
        plt.close()

    bar_width = 0.2
    index = np.arange(len(metrics))

    plt.figure(figsize=(12, 7))
    # scores dimensions: [num_models][num_metrics]
    r_s_acc = [(a + b + c) / 3 for a, b, c in result_sharemind["acc"]]
    r_s_kappa = [(a + b + c) / 3 for a, b, c in result_sharemind["kappa"]]
    r_s_f1 = [(a + b + c) / 3 for a, b, c in result_sharemind["f1"]]
    r_s_auc = [(a + b + c) / 3 for a, b, c in result_sharemind["auc"]]
    scores = [
        [result_central["acc"], result_central["kappa"], result_central["f1"], result_central["auc"]],
        [result_plain["acc"][-1], result_plain["kappa"][-1], result_plain["f1"][-1], result_plain["auc"][-1]],
        [r_s_acc[-1], r_s_kappa[-1], r_s_f1[-1], r_s_auc[-1]]
    ]

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for j, score in enumerate(scores):
        plt.bar(index + j * bar_width, score, bar_width, label=models[j], color=colors[j])
        # plt.bar(index + j * bar_width, score, bar_width, label=models[j], color=["#1f77b4", '#ff7f0e', '#2ca02c'])

    plt.xlabel('Metric')
    plt.ylabel('Scores')
    plt.xticks(index + bar_width, metrics)
    plt.ylim(0.5, 1.)  # Set y-axis limits; starting at 0.5
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{cm.PROJECT_PATH}/result/images/performance_{ds}.png")  # Save the figure
    plt.cla()
