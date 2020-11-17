#!/bin/bash

# create matching user if user does not exist (just do this once per user)
if ! id "$1" > /dev/null 2>&1; then

    # create user
    useradd -s /bin/bash -u $2 $1 -m
    adduser $1 sudo
    echo "$1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

    # add user to docker group
    usermod -aG docker $1

    # generate and authorize keys
    su $1 -c "ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa"
    su $1 -c "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
    su $1 -c "chmod 600 ~/.ssh/authorized_keys"
    cat /home/$1/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

    # set default workdir
    su $1 -c 'echo "cd /postal" >> ~/.bashrc'

    # install in editable mode
    su $1 -c 'poetry install'

    # alias postal
    echo -e '#!/usr/bin/env bash\npoetry run postal $@' > /usr/local/bin/postal
    chmod +x /usr/local/bin/postal
fi

# switch user
su $1
