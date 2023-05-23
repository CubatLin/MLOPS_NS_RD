'''這隻程式專用來pull images, build container等創建動作; 在啟動container行為上不在此程式範疇'''
import os
import env_config
import sys
from src.model.docker_command import DockerCommand
import time
import subprocess

## params
# RUN = ['pull_images', 'build_container', 'pkg_init', 'gpt_base', 'python_package', 'OTHER', 'all']
RUN = 'pull_images' if len(sys.argv) == 1 else sys.argv[1]


if __name__ == "__main__":
    if RUN == 'pull_images' or RUN == 'all':
        # dockerCmd pull Images
        DockerCommand.dockerPull(tag=env_config.IMAGE_POSTGRES_TAG)
        DockerCommand.dockerPull(tag=env_config.IMAGE_PGADMIN_TAG)

    if RUN == 'build_container' or RUN == 'all':
        subprocess.run(f"mkdir -p {env_config.CONTAINER_POSTGRES_ROOT_MAP}", shell=True)
        subprocess.run(f"mkdir -p {env_config.CONTAINER_PGADMIN_ROOT_MAP}", shell=True)

        # dockerCmd run mongodb
        DockerCommand.dockerRun(
            tag=env_config.IMAGE_POSTGRES_TAG,
            name=env_config.CONTAINER_POSTGRES_NAME,
            port=env_config.CONTAINER_POSTGRES_PORT_LIST,
            volume=f'{env_config.CONTAINER_POSTGRES_ROOT_MAP}:{env_config.CONTAINER_POSTGRES_ROOT}',
            envDict=env_config.CONTAINER_POSTGRES_ENV_DICT,
            network=env_config.CONTAINER_MONGO_POSTGRES_NET,
            detach=True, interactive=False, TTY=False
        )

        # dockerCmd run dpage/pgadmin4:6.20
        DockerCommand.dockerRun(
            tag=env_config.IMAGE_PGADMIN_TAG,
            name=env_config.CONTAINER_PGADMIN_NAME,
            port=env_config.CONTAINER_PGADMIN_PORT_LIST,
            volume=f'{env_config.CONTAINER_PGADMIN_ROOT_MAP}:{env_config.CONTAINER_PGADMIN_ROOT}',
            envDict=env_config.CONTAINER_PGADMIN_ENV_DICT,
            network=env_config.CONTAINER_MONGO_POSTGRES_NET,
            detach=True, interactive=False, TTY=False
        )

        time.sleep(5)
        os.system(f'open http://localhost:{env_config.CONTAINER_PGADMIN_PORT_LIST[0].split(":")[0]}')

    if RUN == 'update' or RUN == 'all':
        # 更新apt-get
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_POSTGRES_NAME,
            cmd="apt-get update",
            detach=False,
            interactive=True,
            TTY=False,
        )
        # 更新pip
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_POSTGRES_NAME,
            cmd='bash -c "pip install --upgrade pip"',
            detach=False,
            interactive=True,
            TTY=False,
        )

    if RUN == 'gpt_base' or RUN == 'all':
        apt_install_package = [
            'git', 'make', 'vim', 'libpq-dev', 'gcc', 'python', 'python3', 'python3-pip', 'unzip'
        ]
        for package in apt_install_package:
            DockerCommand.dockerExec(
                name=env_config.CONTAINER_POSTGRES_NAME,
                cmd=f'bash -c "apt-get install -y {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )

    if RUN == 'python_package' or RUN == 'all':
        # 更新pip
        python_install_package = [
            'psycopg2', 'psycopg2-binary', 'pymongo', 'requests', 'python-dotenv', 'beautifulsoup4',
            'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'google-auth', 'oauth2client'
        ]
        for package in python_install_package:
            DockerCommand.dockerExec(
                name=env_config.CONTAINER_POSTGRES_NAME,
                cmd=f'bash -c "pip install {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )
    if RUN == 'OTHER':
        # dockerCmd postgres:15.2 - 建立資料庫
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_POSTGRES_NAME,
            cmd=f"psql -U postgres -c \'CREATE DATABASE {env_config.CONTAINER_POSTGRES_DB1};\'",
            detach=False, interactive=True, TTY=False
        )  # 建立資料庫 crawlerdb
