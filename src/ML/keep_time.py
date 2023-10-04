import main
import common as cm
import time
import numpy as np

if __name__ == "__main__":
    script_path = f"{cm.PROJECT_PATH}/client/run_script.sh"
    importer_path = f"{cm.PROJECT_PATH}/client/importer.sh"
    py_xml_path = f"{cm.PROJECT_PATH}/src/ML/gen_importer.py"
    agg_time = []
    upload_time = []
    download_time = []
    niter = 10

    # aggregation
    for i in range(niter):
        start = time.time()
        res = main.execute_cmd(script_path, 1, "agg")
        agg_time.append(time.time() - start)
    agg_time = np.array(agg_time)
    print("Agg: ", agg_time)
    print(agg_time.mean(), agg_time.std(), 2 * agg_time.std())

    # generate .xml and .log
    res = main.gen_xml_log(py_xml_path)

    # Upload to the MPC
    for i in range(niter):
        start = time.time()
        res = main.execute_cmd(importer_path, 1)
        upload_time.append(time.time() - start)
    upload_time = np.array(upload_time)
    print("Upload: ", upload_time)
    print(upload_time.mean(), upload_time.std(), 2 * upload_time.std())

    # Downloading
    for i in range(niter):
        start = time.time()
        res = main.execute_cmd(script_path, 1, "global")
        download_time.append(time.time() - start)
    download_time = np.array(download_time)
    print("Download: ", download_time)
    print(download_time.mean(), download_time.std(), 2 * download_time.std())
