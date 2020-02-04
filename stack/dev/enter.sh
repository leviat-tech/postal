#!/bin/bash

# create matching user if user does not exist (just do this once per user)
if ! id "$1" > /dev/null 2>&1; then

    # create user
    useradd -s /bin/bash -u $2 $1 -m
    adduser $1 sudo
    echo "$1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

    # set default workdir
    su $1 -c 'echo "cd /postal" >> ~/.bashrc'

    # add user to docker group
    usermod -aG docker $1

    # install in editable mode
    pip install -e /postal
fi

# setup shell
export TERM=xterm-color

# disable pycache
export PYTHONDONTWRITEBYTECODE=1

# switch user
su $1
