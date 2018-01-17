#!/bin/bash
python --version
rm -r dist/ build/
pyinstaller -y ./server_batch.py
cp -r dist/server_batch/* jenkins_data/SERVER/bin/

DOCKER_VERSION=$(<version)
docker build . -t newtranx_server-gpu:v$DOCKER_VERSION
IMAGE_ID=$(docker images | grep -E "newtranx_server-gpu " | grep -E "${DOCKER_VERSION} " | tr -s ' ' | cut -d ' ' -f3)
docker image save ${IMAGE_ID} -o newtranx_server-gpu.v${DOCKER_VERSION}.tar
tar zcvf newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz newtranx_server-gpu.v${DOCKER_VERSION}.tar
#
mkdir -p scp
rm scp/*
rm newtranx_server-gpu.v${DOCKER_VERSION}.tar
#
mv newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz scp/newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz
#sudo scp -P 10086 newtranx_server-gpu.v${DOCKER_VERSION}.tar.gz newtranx@121.46.13.39:/home/newtranx/decoder