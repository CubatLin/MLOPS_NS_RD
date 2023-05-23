# This is MLOps project created by NS R&Ds.
- by 台灣梯度下降第一品牌

# 開發日誌
### Ethan修正檔案
* build_mongodb_docker_env.py / build_postgres_docker_env.py
* 新增log / notebook / doc資料
* 新增src.controller.process_logger.py 檔案
* 修正from src.model.docker_command import DockerCommand

### 待完成項目
* env_docker_mongodb內參數命名不清
* src.coltroller.logger 使用狀況不明 / logger看來還未生效
* 外層檔案雜亂

## 編修問題紀錄
| 序號 | 建立時間 | 修訂人員 | 問題內容 |
| ----------- | ----------- | ----------- | ----------- |
| 01 | 2023.04.23 | Pat | Project Init |
| 02 | 2023.05.23 | Ethan | 編修DockerCmd to DockerCommand / env_docker檔名編修&參數修正 |


# 環境安裝
## 啟動pyenv
1. 下載 pyenv, pyenv-virtualenv: ```brew install pyenv pyenv-virtualenv```
2. Clone 專案並指定虛擬環境: ```git clone https://github.com/ts01174755/MLOPS.git [Your Project Path]```
3. pyenv 設定
* 切到Project的路徑: ```cd [Your Project Path]``` 
* 把pyenv的環境參數丟到zshrc檔案裡: ```python3 pyenv_setting.py```
* 查看一下shell script: ```source ~/.zshrc```

## 版本控制
- 使用 python 3.8.16: ```pyenv install 3.8.16```
- 為專案建立虛擬環境: 
1. 先建立virtualenv python=3.8.16並命名為mlops_nsrd: ```pyenv virtualenv 3.8.16 mlops_nsrd```
2. 切到專案根目錄: ```cd [Your Project Path]```
3. 把當前local路徑下的專案環境指向mlops_nsrd: ```pyenv local mlops_nsrd```
    
## 建立環境(建議用pyenv)
- 進入env_config修改參數，有五個CONTAINER參數要做修改
1. 修改環境參數檔: ```vim env_config.py```
    ```
    IMAGE_MONGODB_TAG = [YOUR MONGODB IMAGE TAG]
    CONTAINER_MONGODB_NAME = [YOUR MONGODB CONTAINER NAME]
    CONTAINER_MONGODB_PORT_LIST = [YOUR MONGODB PORT LIST]
    CONTAINER_MONGODB_ROOT = [YOUR MONGODB ROOT]
    CONTAINER_MONGODB_ROOT_MAP = [YOUR MONGODB ROOT MAP]
    CONTAINER_MONGO_POSTGRES_NET = [YOUR MONGODB POSTGRES NET]
    CONTAINER_MONGO_ENV_DICT = [CONTAINER_MONGO_ENV_DICT]
    ```
2. 安裝virtual env需要的套件: ```python3 env_local_pkgInstall.py all```
3. 拉mongodb的docker images(這步記得有個env/.env檔案要加): ```python3 build_mongodb_docker_env.py all```
4. 拉postgresql的docker images: ```python3 build_postgres_docker_env.py all```

# MongoDB

### MongoDB - 建立資料庫

> $ mongo -u mongodb -p mongodb --authenticationDatabase admin
>
> ~ use originaldb
 
# Postgres

## Postgres - 建立資料庫
```$ docker inspect [YOUR POSTGRESDB NAME]```

1. 查看 container 資訊，找出Networks.bridge.IPAddress
2. 點擊 "Add Server"
3. Name: [YOUR POSTGRES NAME]
4. Host name/address: [Networks.bridge.IPAddress]
5. Port: [YOUR POSTGRES PORT]
6. Maintenance database: [YOUR POSTGRES DATABASE NAME]
7. Username: [YOUR POSTGRES USERNAME]
8. Password: [YOUR POSTGRES USERPASSWORD]