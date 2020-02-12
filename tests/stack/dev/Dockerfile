FROM ubuntu:latest

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    wget \
    curl \
    nano \
    sudo \
    python3 \
    python3-pip

COPY stack/dev/enter.sh /enter.sh
CMD tail -f /dev/null
