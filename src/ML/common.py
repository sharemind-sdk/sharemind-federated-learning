import os
import yaml
from enum import Enum


current_path = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.dirname(current_path)
PROJECT_PATH = PARENT_PATH.split("/src")[0]
CLIENT_NUMBER = os.environ.get("CLIENT_NUMBER")
CLIENT_NAME = f"client{CLIENT_NUMBER}"


# Read the configuration
with open(f"{PROJECT_PATH}/conf.yml", 'r') as ymlfile:
    CFG = yaml.safe_load(ymlfile)


# Duplicated in app.py but it should...?
class ReportType(Enum):
    RECEIVED = "received"
    UPLOADED = "uploaded"
    FOR_ALPHA = "for_alpha"
    MPC_RUNNING = "mpc_running"
