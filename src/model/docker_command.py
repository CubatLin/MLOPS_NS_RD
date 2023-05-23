import subprocess


class DockerFileSystem:
    @classmethod
    def dockerWrite(cls, name, path, data):
        # 把資料寫入docker container
        print(f"docker exec -i {name} /bin/bash -c 'echo {data} > {path}'")
        subprocess.run(
            f"docker exec -i {name} /bin/bash -c 'echo -e \"{data}\" > {path}'",
            shell=True,
        )

    @classmethod
    def dockerCopy(cls, name, filePath, targetPath):
        # 把資料寫入docker container
        print(f"docker cp {filePath} {name}:{targetPath}")
        subprocess.run(f"docker cp {filePath} {name}:{targetPath}", shell=True)


class DockerContainer:
    @classmethod
    def dockerRun(
        cls,
        tag,
        name,
        volume,
        port=[],
        envDict={},
        detach=True,
        interactive=True,
        TTY=False,
        network="",
    ):  # 建立docker container
        env = ""
        for key, value in envDict.items():
            env += f"-e {key}={value} "
        par = "-" if interactive | detach | TTY else ""
        par += "i" if interactive else ""
        par += "d" if detach else ""
        par += "t" if TTY else ""

        port = " ".join([f"-p {p}" for p in port])
        if network != "":
            network = f"--network {network}"
        print(
            f"docker run {par} {port} {env} {network} --name {name} -v {volume} {tag}"
        )
        subprocess.run(
            f"docker run {par} {port} {env} {network} --name {name} -v {volume} {tag}",
            shell=True,
        )

    @classmethod
    def dockerCreate(cls, tag, name, port, volume):  # 建立docker container
        print(f"docker create --name {name} -p {port} -v {volume} {tag}")
        subprocess.run(
            f"docker create --name {name} -p {port} -v {volume} {tag}", shell=True
        )

    @classmethod
    def dockerRemove(cls, name):  # 刪除docker container
        print(f"docker rm {name}")
        subprocess.run(f"docker rm {name}", shell=True)

    # 重啟docker container
    @classmethod
    def dockerRestart(cls, name):
        print(f"docker restart {name}")
        subprocess.run(f"docker restart {name}", shell=True)

    @classmethod
    def dockerStart(cls, name):  # 啟動docker container
        print(f"docker start {name}")
        subprocess.run(f"docker start {name}", shell=True)

    @classmethod
    def dockerStop(cls, name):  # 停止docker container
        print(f"docker stop {name}")
        subprocess.run(f"docker stop {name}", shell=True)

    @classmethod
    def dockerExec(
        cls, name, cmd, detach=True, interactive=False, TTY=False
    ):  # 執行docker container的指令
        par = "-" if interactive | detach | TTY else ""
        par += "i" if interactive else ""
        par += "d" if detach else ""
        par += "t" if TTY else ""
        print(f"docker exec {par} {name} {cmd}")
        subprocess.run(f"docker exec {par} {name} {cmd}", shell=True)

    @classmethod
    def dockerPs(cls):  # 查看docker container
        print("docker ps -a")
        subprocess.run("docker ps -a", shell=True)

    @classmethod
    def dockerLogs(cls, name):  # 查看docker container的log
        print(f"docker logs {name}")
        subprocess.run(f"docker logs {name}", shell=True)

    @classmethod
    def dockerInspect(cls, name):  # 查看docker container的詳細資訊，並回傳成Jason格式
        print(f"docker inspect {name}")
        return subprocess.getoutput(f"docker inspect {name}")


class DockerImage:
    @classmethod
    def dockerPull(cls, tag):  # 從docker hub下載image
        print(f"docker push {tag}")
        subprocess.run(f"docker pull {tag}", shell=True)

    @classmethod
    def dockerBuild(cls, dockerfile, tag):  # 建立docker image
        print(f"docker build -f {dockerfile} -t {tag} .")
        subprocess.run(f"docker build -f {dockerfile} -t {tag} .", shell=True)

    @classmethod
    def dockerTag(cls, tag, newTag):  # 重新命名image
        print(f"docker tag {tag} {newTag}")
        subprocess.run(f"docker tag {tag} {newTag}", shell=True)

    @classmethod
    def dockerSave(cls, tag, path):  # 儲存image
        print(f"docker save {tag} -o {path}")
        subprocess.run(f"docker save {tag} -o {path}", shell=True)

    @classmethod
    def dockerLoad(cls, path):  # 載入image
        print(f"docker load -i {path}")
        subprocess.run(f"docker load -i {path}", shell=True)

    @classmethod
    def dockerPush(cls, tag):  # 上傳image到docker hub
        print(f"docker push {tag}")
        subprocess.run(f"docker push {tag}", shell=True)

    @classmethod
    def dockerRmi(cls, tag):  # 刪除docker image
        print(f"docker rmi {tag}")
        subprocess.run(f"docker rmi {tag}", shell=True)

    @classmethod
    def dockerImages(cls):  # 查看docker image
        print("docker images")
        subprocess.run("docker images", shell=True)


class dockerNetwork:
    @classmethod
    def dockerNetworkCreate(cls, name):  # 建立docker network
        print(f"docker network create {name}")
        subprocess.run(f"docker network create {name}", shell=True)

    @classmethod
    def dockerNetworkRemove(cls, name):  # 刪除docker network
        print(f"docker network rm {name}")
        subprocess.run(f"docker network rm {name}", shell=True)

    @classmethod
    def dockerNetworkConnect(cls, name, container):  # 將docker container加入docker network
        print(f"docker network connect {name} {container}")
        subprocess.run(f"docker network connect {name} {container}", shell=True)

    @classmethod
    def dockerNetworkDisconnect(
        cls, name, container
    ):  # 將docker container從docker network移除
        print(f"docker network disconnect {name} {container}")
        subprocess.run(f"docker network disconnect {name} {container}", shell=True)

    @classmethod
    def dockerNetworkInspect(cls, name):  # 查看docker network的詳細資訊，並回傳成Jason格式
        print(f"docker network inspect {name}")
        return subprocess.getoutput(f"docker network inspect {name}")

    @classmethod
    def dockerNetworkLs(cls):  # 查看docker network
        print("docker network ls")
        subprocess.run("docker network ls", shell=True)


# 將docker的操作進行封裝
class DockerCommand(DockerFileSystem, DockerContainer, DockerImage, dockerNetwork):
    @classmethod
    def dockerLogin(cls, username, password):  # 登入docker hub
        print(f"docker login -u {username} -p {password}")
        subprocess.run(f"docker login -u {username} -p {password}", shell=True)
