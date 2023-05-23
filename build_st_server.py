import os
import sys
import env_config
from STPythonServer.controller.st_google_drive import STGoogleDrive
from STPythonServer.controller.st_line_notify import STLineNotify
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging
import json
from src.controller.logger import LoggingMiddleware
from src.model.docker_command import DockerCommand

# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8003
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# ------------------------ env_params ------------------------
CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_NAME     # 執行環境
FILE_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH      # 存放資料的位置
DOWNLOAD_PATH_DOCEKR = env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH   # 存放資料的位置
ROOT_PATH_DOCKER = env_config.MLOPS_ROOT_PATH_DOCKER    # DOCKER 執行路徑
ROOT_PATH_LOCAL = env_config.MLOPS_ROOP_PATH_LOCAL      # LOCAL 執行路徑
INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_INTERPRETER      # 執行的python解釋器
ROUTE_NAME = f"{ROOT_PATH_DOCKER}/build_st_server.py"    # 執行的程式
LOG_PATH = f"{ROOT_PATH_DOCKER}/log_st_server.log"    # 執行的程式
# LOG_PATH = f"{ROOT_PATH_LOCAL}/log_st_server.log"    # 執行的程式
MONGODB = env_config.MONGODB_DOCKER     # mongodb連線資訊
# MONGODB = env_config.MONGODB_LOCAL    # mongodb連線資訊
POSTGRESDB = env_config.POSTGRESDB_DOCKER # postgres連線資訊
# POSTGRESDB = env_config.POSTGRESDB_LOCAL # postgres連線資訊
DEPLOY_DETACH = True

# ------------------------- ROUTE ----------------------------

if RUN == "local":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler()
        ]
    )

app = FastAPI()
app.add_middleware(LoggingMiddleware)


class STCrawlerRequestBody(BaseModel):
    DEFAULT_DICT: dict = {}


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}

@app.get("/stPythonServer/stGoogleDrive")
def st_google_drive_get():
    return {"message": "here is stPythonServer/stGoogleDrive"}

@app.post("/stPythonServer/stGoogleDrive")
def st_google_drive(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    # 每日執行 - 爬蟲
    st_google_drive = STGoogleDrive()
    df = st_google_drive.searchPostgres(
        # MONGODB_INFO=params.DEFAULT_DICT['MONGODB_INFO'],
        POSTGRESDB=POSTGRESDB,
        QUERY_SQL=params.DEFAULT_DICT['QUERY_SQL'],
    )

    # 撰寫 googleDrive 模擬cd, rm, mkdir, 等shell操作
    notifyInfo = st_google_drive.fileMoveAndCopy(
        GOOGLE_DRIVE_INFO=params.DEFAULT_DICT['GOOGLE_DRIVE_INFO'],
        df=df
    )
    if len(notifyInfo) == 0:
        return notifyInfo

    line_message = st_google_drive.line_notify_message(notifyInfo)

    with open(params.DEFAULT_DICT['NOTIFY_TOKEN_FILE'], 'r') as f:
        lineNotifyToken = json.load(f)

    st_line_notify = STLineNotify()
    st_line_notify.postLineNotify(
        token=lineNotifyToken[params.DEFAULT_DICT['NOTIFY_TOKEN_TYPE']],
        message=line_message
    )

    return notifyInfo


if __name__ == "__main__":
    # 執行環境 - 基本上不需要動
    if RUN == "docker":
        DockerCommand.dockerExec(
            name=CONTAINER_NAME,
            cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {INTERPRETER} {ROUTE_NAME} local"',
            detach=DEPLOY_DETACH,
            interactive=True,
            TTY=False,
        )
    elif RUN == "local":
        uvicorn.run(app, host="0.0.0.0", port=DEPLOY_PORT)


