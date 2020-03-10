#!/usr/bin/env bash

cd $(dirname "$0") && cd ../
docker build -t crhio/postal:latest -f stack/postal/Dockerfile .
docker push crhio/postal:latest
