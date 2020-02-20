#!/bin/bash

# create matching user if user does not exist (just do this once per user)
if ! id "$1" > /dev/null 2>&1; then

    # create user
    useradd -s /bin/bash -u $2 $1 -m
    adduser $1 sudo
    echo "$1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

    # set default workdir
    su $1 -c 'echo "cd /postal" >> ~/.bashrc'

    # set env vars so remote ssh calls will work
    echo POSTAL_AWS_BUCKET=$POSTAL_AWS_BUCKET >> /etc/environment
    echo POSTAL_AWS_REGION=$POSTAL_AWS_REGION >> /etc/environment
    echo AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID >> /etc/environment
    echo AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY >> /etc/environment

    # add user to docker group
    usermod -aG docker $1

    # install in editable mode
    pip install -e /postal

    # generate and authorize keys
    su $1 -c "ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa"
    su $1 -c "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
    su $1 -c "chmod 600 ~/.ssh/authorized_keys"
fi

# setup shell
export TERM=xterm-color

# disable pycache
export PYTHONDONTWRITEBYTECODE=1

# switch user
su $1
