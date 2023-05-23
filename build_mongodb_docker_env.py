import os
import env_config
import sys
from src.model.docker_command import DockerCommand
from src.controller.process_logger import Logger
import time
import subprocess

## params
# RUN = ['images', 'build_container', 'pkg_init', 'gpt_base', 'python_package', 'OTHER', 'all']
RUN = 'pull_images' if len(sys.argv) == 1 else sys.argv[1]
mongodb_logger = Logger(path = './log/mongodb.log', 
                        cmd_level='error', file_level='debug')


if __name__ == "__main__":
    mongodb_logger.debug(f'MongoDB Process: {RUN}')

    if RUN == 'pull_images' or RUN == 'all':
        # dockerCmd pull Images
        DockerCommand.dockerPull(tag=env_config.IMAGE_MONGODB_TAG)
        DockerCommand.dockerPull(tag=env_config.IMAGE_MONGODB_EXPRESS_TAG)

    if RUN == 'build_container' or RUN == 'all':
        # dockerCmd 建立網路
        DockerCommand.dockerNetworkRemove(name=f'{env_config.CONTAINER_MONGO_POSTGRES_NET}')
        DockerCommand.dockerNetworkCreate(name=f'{env_config.CONTAINER_MONGO_POSTGRES_NET}')

        subprocess.run(f"mkdir -p {env_config.CONTAINER_MONGODB_ROOT_MAP}", shell=True)
        subprocess.run(f"mkdir -p {env_config.CONTAINER_MONGODB_EXPRESS_ROOT_MAP}", shell=True)

        # dockerCmd run mongodb
        DockerCommand.dockerRun(
            tag=env_config.IMAGE_MONGODB_TAG,
            name=env_config.CONTAINER_MONGODB_NAME,
            port=env_config.CONTAINER_MONGODB_PORT_LIST,
            volume=f'{env_config.CONTAINER_MONGODB_ROOT_MAP}:{env_config.CONTAINER_MONGODB_ROOT}',
            envDict=env_config.CONTAINER_MONGO_ENV_DICT,
            network=env_config.CONTAINER_MONGO_POSTGRES_NET,
            detach=True, interactive=False, TTY=False
        )

        # dockerCmd run mongodb-express
        DockerCommand.dockerRun(
            tag=env_config.IMAGE_MONGODB_EXPRESS_TAG,
            name=env_config.CONTAINER_MONGODB_EXPRESS_NAME,
            port=env_config.CONTAINER_MONGODB_EXPRESS_PORT_LIST,
            volume=f'{env_config.CONTAINER_MONGODB_EXPRESS_ROOT_MAP}:{env_config.CONTAINER_MONGODB_EXPRESS_ROOT}',
            envDict=env_config.CONTAINER_MONGO_EXPRESS_ENV_DICT,
            network=env_config.CONTAINER_MONGO_POSTGRES_NET,
            detach=True, interactive=False, TTY=False
        )
        
        time.sleep(5)
        os.system(f'open http://localhost:{env_config.CONTAINER_MONGODB_EXPRESS_PORT_LIST[0].split(":")[0]}')


    if RUN == 'pkg_init' or RUN == 'all':
        # 更新apt-get
        DockerCommand.dockerExec(
            name=env_config.CONTAINER_MONGODB_NAME,
            cmd="apt-get update",
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
                name=env_config.CONTAINER_MONGODB_NAME,
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
                name=env_config.CONTAINER_MONGODB_NAME,
                cmd=f'bash -c "pip install {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )
    if RUN == 'OTHER':
        pass