version=7.8
tar zxvsf newtranx_server-gpu.v$version.tar.gz && sudo docker image load -i \
newtranx_server-gpu.v$version.tar \
| cut -d ':' -f3 | sudo xargs -I{} docker tag {} newtranx_server-gpu:v$version
