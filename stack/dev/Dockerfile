FROM ubuntu:focal

# install dev tools
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    wget \
    curl \
    nano \
    sudo \
    python3 \
    python3-pip \
    python-is-python3

# add docker apt repository
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
RUN apt-key fingerprint 0EBFCD88 | grep "9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88"
RUN add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

# install docker
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io

# install docker compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# install open ssh server
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# setup user bash environment
RUN echo TERM=xterm-color >> /etc/environment
RUN echo PYTHONDONTWRITEBYTECODE=1 >> /etc/environment

# install poetry
RUN pip3 install poetry

# copy enter script and run
WORKDIR /postal
COPY stack/dev/enter.sh /enter.sh

#CMD tail -f /dev/null
CMD ["/usr/sbin/sshd", "-D"]
