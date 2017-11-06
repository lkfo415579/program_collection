DOCKER_ID=71b03d32ed97
DOCKER_VERSION=7.2
sudo docker commit ${DOCKER_ID} newtranx_server-gpu:v${DOCKER_VERSION}
IMAGE_ID=$(sudo docker images | grep -E "${DOCKER_VERSION} " | tr -s ' ' | cut -d ' ' -f3)
sudo docker image save ${IMAGE_ID} -o newtranx_server-gpu.v${DOCKER_VERSION}.tar
sudo tar zcvf newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz newtranx_server-gpu.v${DOCKER_VERSION}.tar
sudo scp newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz test@10.0.100.181:/home/test/DOCKER


DOCKER_ID=3e7a0ef62f09
DOCKER_VERSION=7.2-key
sudo docker commit ${DOCKER_ID} newtranx_server-gpu-key:v${DOCKER_VERSION}
IMAGE_ID=$(sudo docker images | grep -E "${DOCKER_VERSION} " | tr -s ' ' | cut -d ' ' -f3)
sudo docker image save ${IMAGE_ID} -o newtranx_server-gpu.v${DOCKER_VERSION}.tar
sudo tar zcvf newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz newtranx_server-gpu.v${DOCKER_VERSION}.tar
sudo scp newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz test@10.0.100.181:/home/test/DOCKER
