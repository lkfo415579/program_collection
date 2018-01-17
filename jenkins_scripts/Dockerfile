FROM jenkins/jenkins:lts
# if we want to install via apt
USER root

COPY PKG /etc/apt/sources.list

RUN apt-get update && apt-get install -y python python-pip
# Install docker
RUN apt-get install -y \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common

RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get install -y docker-ce
#
RUN pip install pyinstaller
# JENKINS python packages
RUN apt-get install -y python-numpy libicu-dev libmecab-dev mecab mecab-ipadic-utf8
RUN pip install validictory tornado polyglot requests regex jieba mecab-python3
# drop back to the regular jenkins user - good practice
USER jenkins
