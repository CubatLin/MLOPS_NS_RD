import os
import sys
import env_config
from MongoDB.controller.mongodb_crawler_data import CrawlerData
from MongoDB.controller.mongodb_googleform_data import GoogleFormData
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging
from src.controller.logger import LoggingMiddleware
from src.model.docker_command import DockerCommand
# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8001
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# ------------------------ env_params ------------------------
CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_NAME     # 執行環境
FILE_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH      # 存放資料的位置
DOWNLOAD_PATH_DOCEKR = env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH   # 存放資料的位置
ROOT_PATH_DOCKER = env_config.MLOPS_ROOT_PATH_DOCKER    # DOCKER 執行路徑
ROOT_PATH_LOCAL = env_config.MLOPS_ROOP_PATH_LOCAL      # LOCAL 執行路徑
INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_INTERPRETER      # 執行的python解釋器
ROUTE_NAME = f"{ROOT_PATH_DOCKER}/build_crawler_server.py"    # 執行的程式
LOG_PATH = f"{ROOT_PATH_DOCKER}/log_crawler_server.log"    # 執行的程式
# LOG_PATH = f"{ROOT_PATH_LOCAL}/log_crawler_server.log"    # 執行的程式
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
    DATA_TIME: str = None
    URL: str = None
    COOKIES: dict = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None
    MONGODB_PORT: int = None
    MONGODB_HOST: str = None
    MONGODB_DATABASE: str = None
    COLLECTION: str = None


class CrawlerFileRequestBody(BaseModel):
    URL: str = None
    FILENAME: str = None


class GoogleFormDataRequestBody(BaseModel):
    DATA_TIME: str = None
    TOKEN: str = None
    CLIENT_SECRET_FILE: str = None
    SCOPES: str = None
    FORMID: str = None
    DISCOVERY_DOC: str = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None
    MONGODB_PORT: int = None
    MONGODB_HOST: str = None
    MONGODB_DATABASE: str = None
    COLLECTION: str = None


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.post("/MongoDB/crawlerDataPost")
def crawler_data_post(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    crawler_data = CrawlerData()

    # 爬蟲
    crawler_data.get_crawlerdata_to_mongodb(
        URL=params.URL,
        COOKIES=params.COOKIES,
        Mongodb = MONGODB,
        COLLECTION=params.COLLECTION,
        DATATIME=params.DATA_TIME,
    )
    return {"message": "insert success"}


@app.post("/MongoDB/crawlerZipFilePost")
def crawler_zip_file_post(params: CrawlerFileRequestBody = CrawlerFileRequestBody()):
    crawler_data = CrawlerData()

    # 爬蟲
    crawler_data.get_crawlerZipFile_to_fileSystem(
        URL=params.URL,
        FILEPATH=f'/{DOWNLOAD_PATH_DOCEKR}/{params.FILENAME}',
    )
    return {"message": "insert success"}


@app.post("/MongoDB/googleFormDataPost")
def google_form_data_post(params: GoogleFormDataRequestBody = GoogleFormDataRequestBody()):
    google_form_data = GoogleFormData()

    google_form_data.get_googleformdata_to_mongodb(
        TOKEN=params.TOKEN,
        CLIENT_SECRET_FILE=params.CLIENT_SECRET_FILE,
        SCOPES=params.SCOPES,
        DISCOVERY_DOC=params.DISCOVERY_DOC,
        Mongodb = MONGODB,
        COLLECTION=params.COLLECTION,
        FORMID=params.FORMID,
        DATATIME=params.DATA_TIME,
    )
    return {"message": "insert success"}


# Main entry point
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
