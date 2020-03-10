#!/usr/bin/env bash

cd $(dirname "$0") && cd ../
docker build -t postal:latest -f stack/postal/Dockerfile .
docker stack deploy -c stack/production.yml postal
