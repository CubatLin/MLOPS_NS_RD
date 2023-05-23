import os
import env_config
import sys
from src.model.docker_command import DockerCommand
import subprocess

## params
RUN = ['images', 'build', 'init', 'gpt_base', 'python_package', 'OTHER', 'all']
RUN = 'images' if len(sys.argv) == 1 else sys.argv[1]

if __name__ == "__main__":
    if RUN == 'images' or RUN == 'all':
        # 建構Python3.8的Docker Image
        # dockerCmd pull Images
        DockerCommand.dockerPull(tag=env_config.IMAGE_PYTHON_3_8_18_TAG)

    if RUN == 'build' or RUN == 'all':
        subprocess.run(f"mkdir -p {env_config.CONTAINER_PYTHON_3_8_18_ROOT_MAP}", shell=True)

        DockerCommand.dockerRun(
            tag=env_config.IMAGE_PYTHON_3_8_18_TAG,
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            port=env_config.CONTAINER_PYTHON_3_8_18_PORT_LIST,
            volume=f'{env_config.CONTAINER_PYTHON_3_8_18_ROOT_MAP}:{env_config.CONTAINER_PYTHON_3_8_18_ROOT}',
            detach=True, interactive=True, TTY=False
        )
        DockerCommand.dockerNetworkConnect(name=env_config.CONTAINER_MONGO_POSTGRES_NET, container=env_config.CONTAINER_PYTHON_3_8_18_NAME)

        # 建立基礎Folder
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd=f'bash -c "mkdir -p {env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH}"',
            detach=False,
            interactive=True,
            TTY=False
        )
        # 建立基礎Folder
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd=f'bash -c "mkdir -p {env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH}"',
            detach=False,
            interactive=True,
            TTY=False
        )

    if RUN == 'init' or RUN == 'all':
        # 更新apt-get
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd="apt-get update",
            detach=False,
            interactive=True,
            TTY=False,
        )
        # 更新pip
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd='bash -c "pip install --upgrade pip"',
            detach=False,
            interactive=True,
            TTY=False,
        )

    if RUN == 'gpt_base' or RUN == 'all':
        # dockerCmd postgres:15.2 - 基礎安裝
        apt_install_package = ['tzdata', 'git', 'make', 'gcc', 'vim', 'wget', 'zlib1g-dev', '']
        for package in apt_install_package:
            DockerCommand.dockerExec(
                name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
                cmd=f'apt-get install -y {package}',
                detach=False,
                interactive=True,
                TTY=False,
            )
    if RUN == 'python_package' or RUN == 'all':
        # 更新pip
        python_install_package = [
            'python-dotenv', 'fastapi', 'uvicorn', 'psycopg2', 'pymongo', 'setuptools', 'requests', 'beautifulsoup4',
            'pandas', 'black', 'build', 'tree', 'google-api-python-client', 'google-auth', 'google-auth-oauthlib',
            'google-auth-httplib2', 'oauth2client', 'aiofiles', 'Jinja2==3.1.2', 'sqlalchemy'
        ]
        for package in python_install_package:
            DockerCommand.dockerExec(
                name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
                cmd=f'bash -c "pip install {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )

    if RUN == 'OTHER' or RUN == 'all':
        # docker 修改時區
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd='bash -c "ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime"',
            detach=False,
            interactive=True,
            TTY=False,
        )  # 修改時區

    if RUN == 'TEMP':
        # 顯示已安裝的python套件
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd='bash -c "pip list"',
            detach=False,
            interactive=True,
            TTY=False,
        )

        # 卸載python pkg
        python_install_package = ['oauth2client']
        for package in python_install_package:
            DockerCommand.dockerExec(
                name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
                cmd=f'bash -c "pip uninstall -y {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )