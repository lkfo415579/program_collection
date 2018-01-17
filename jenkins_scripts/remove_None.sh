sudo docker images | grep "none" | tr -s " " | cut -d " " -f3 | sudo xargs \
docker rmi
