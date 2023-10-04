import numpy as np
import re
import pickle
import sys

import common as cm
import ml


def create_regex_pattern(variable: str) -> str:
    return f"({variable}):\s([^\s,]+)"


def to_pickle(filename, value):
    for i in [1, 2, 3]:
        with open(f"{cm.PROJECT_PATH}/client/client{i}/models/recv/{filename}", "wb") as f:
            pickle.dump(value, f)


if __name__ == "__main__":
    model_shape = ml.get_model_shape()

    with open(sys.argv[1], 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            name = re.findall(create_regex_pattern("name"), line)
            if name:
                name = name[0][1]  # ex. [('name', 'layer-0')]

                if "{" in line:
                    value = re.findall(r"(value):\s\{([^{}]*)\}", line)[0][1]
                    value = [float(n) for n in value.split(",")]
                    value = np.array(value).reshape(model_shape[name])
                else:
                    value = re.findall(create_regex_pattern("value"), line)[0][1]
                    value = np.array([float(value)])

                to_pickle(f"{sys.argv[2]}.{name}.pickle", value)
