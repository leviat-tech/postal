#!/usr/bin/env bash

CONTAINER=$(docker ps -aqf "name=postal_postal")
read -e -p "Public key to add (default: ~/.ssh/id_rsa.pub): " PUBLIC_KEY
PUBLIC_KEY=${PUBLIC_KEY:-~/.ssh/id_rsa.pub}
docker exec -i $CONTAINER tee -a /root/.ssh/authorized_keys < $PUBLIC_KEY
docker exec -i $CONTAINER cat /root/.ssh/authorized_keys
