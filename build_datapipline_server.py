import os
import sys
import env_config
from PostgresDB.controller.postgres_parse_mongodb_data import PosgresParseMongodbData
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging
from src.controller.logger import LoggingMiddleware
from src.model.docker_command import DockerCommand

# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8002
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# ------------------------ env_params ------------------------
CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_NAME     # 執行環境
FILE_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH      # 存放資料的位置
DOWNLOAD_PATH_DOCEKR = env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH   # 存放資料的位置
ROOT_PATH_DOCKER = env_config.MLOPS_ROOT_PATH_DOCKER    # DOCKER 執行路徑
ROOT_PATH_LOCAL = env_config.MLOPS_ROOP_PATH_LOCAL      # LOCAL 執行路徑
INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_INTERPRETER      # 執行的python解釋器
ROUTE_NAME = f"{ROOT_PATH_DOCKER}/build_datapipline_server.py"    # 執行的程式
LOG_PATH = f"{ROOT_PATH_DOCKER}/log_datapipline_server.log"    # 執行的程式
# LOG_PATH = f"{ROOT_PATH_LOCAL}/log_datapipline_server.log"    # 執行的程式
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
    MONGODB_COLLECTION: str = None
    MONGODB_QUERY: dict = None
    PROGRESDB_TABLE: str = None
    PROGRESDB_SCHEMA: str = None
    PROGRESDB_SCHEMA_DICT: dict = None
    KWARGS: dict = None

# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.post("/PostgresDB/mongodbToProgres/stCreateCourseForm")
def st_create_course_form(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    # 每日執行 - 爬蟲
    posgresParseMongodbData = PosgresParseMongodbData()
    googleFormDF = posgresParseMongodbData.parseGoogleSTFromData(
        MONGODB=MONGODB,
        DATA_TIME=params.DATA_TIME,
        MONGODB_COLLECTION=params.MONGODB_COLLECTION,
        MONGODB_QUERY=params.MONGODB_QUERY,
        PROGRESDB_SCHEMA_DICT=params.PROGRESDB_SCHEMA_DICT,
    )

    # 連接PostgresDB與寫入資料
    posgresParseMongodbData.insertPostgresData(
        PROGRESDB=POSTGRESDB,
        PROGRESDB_TABLE=params.PROGRESDB_TABLE,
        PROGRESDB_SCHEMA=params.PROGRESDB_SCHEMA,
        dataFrame=googleFormDF,
    )
    return {"message": "insert success"}


@app.post("/PostgresDB/mongodbToProgres/stAdminCourses")
def st_admin_course(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    # 每日執行 - 爬蟲
    posgresParseMongodbData = PosgresParseMongodbData()
    googleFormDF = posgresParseMongodbData.parseSTData(
        MONGODB=MONGODB,
        MONGODB_COLLECTION=params.MONGODB_COLLECTION,
        MONGODB_QUERY=params.MONGODB_QUERY,
        PROGRESDB_SCHEMA_DICT=params.PROGRESDB_SCHEMA_DICT,
        DATA_TIME=params.DATA_TIME,
    )

    # 連接PostgresDB與寫入資料
    posgresParseMongodbData.insertPostgresData(
        PROGRESDB=POSTGRESDB,
        dataFrame=googleFormDF,
        PROGRESDB_TABLE=params.PROGRESDB_TABLE,
        PROGRESDB_SCHEMA=params.PROGRESDB_SCHEMA,
    )
    return {"message": "insert success"}

@app.post("/PostgresDB/mongodbToProgres/makeSchemaFile")
def make_schema_file(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    posgresParseMongodbData = PosgresParseMongodbData()
    posgresParseMongodbData.makeDataSchema(
        PROGRESDB=POSTGRESDB,
        tableName=params.PROGRESDB_TABLE,
        schemaDict=params.KWARGS['PROGRESDB_SCHEMA_DICT'],
        columnList=params.KWARGS['COLUMNS_LIST'],
        schemaFilePath=f'/{FILE_PATH_DOCKER}/{params.KWARGS["PROGRESDB_SCHEMA_FILE"]}',
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

