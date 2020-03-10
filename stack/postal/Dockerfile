FROM ubuntu:latest

# install dev tools
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    wget \
    curl \
    nano \
    sudo \
    python3 \
    python3-pip

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

# create authorized keys file
RUN mkdir -p /root/.ssh && touch /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

# tell python not to write bytecode and simlink python3 to python
ENV PYTHONDONTWRITEBYTECODE 1
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# install postal
COPY ./ /postal
WORKDIR /postal
RUN pip install -e /postal
CMD ["/usr/sbin/sshd", "-D"]
