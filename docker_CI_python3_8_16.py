import os
import env_config
from src.model.docker_command import DockerCommand


if __name__ == "__main__":
    # ------------------------ env_params ------------------------
    CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_NAME
    ROOT_PATH_DOCKER = env_config.MLOPS_ROOT_PATH_DOCKER    # DOCKER 執行路徑
    ROOT_PATH_LOCAL = env_config.MLOPS_ROOP_PATH_LOCAL      # LOCAL 執行路徑

    # 重啟docker container
    DockerCommand.dockerRestart(CONTAINER_NAME)

    # 移除container中的舊程式
    DockerCommand.dockerExec(
        name=CONTAINER_NAME,
        cmd=f"rm -rf {ROOT_PATH_DOCKER}",
        detach=False,
        interactive=True,
        TTY=False,
    )

    # 把gitHub上的程式碼clone到docker container中
    GITHUB_URL = env_config.GITHUB_URL
    DockerCommand.dockerExec(
        name=CONTAINER_NAME,
        cmd=f"git clone {GITHUB_URL} {ROOT_PATH_DOCKER}",
        detach=False,
        interactive=True,
        TTY=False,
    )

    # CONTAINERNAME - CI
    for root, dirs, files in os.walk(ROOT_PATH_LOCAL):
        rootCheck = False
        for r_ in ["__pycache__", ".git", ".idea", "venv", "OLD"]:
            if root.find(r_) != -1:
                rootCheck = True
        if rootCheck:
            continue

        DockerCommand.dockerExec(
            name=CONTAINER_NAME,
            cmd=f"mkdir -p {root.replace(ROOT_PATH_LOCAL, ROOT_PATH_DOCKER)}",
            detach=False,
            interactive=True,
            TTY=False,
        )

        for file in files:
            # 把現在執行的程式更新到container中
            DockerCommand.dockerCopy(
                name=CONTAINER_NAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace(
                    ROOT_PATH_LOCAL, ROOT_PATH_DOCKER
                ),
            )