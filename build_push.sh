#!/bin/bash

docker build -t gustavofcunha/recommendation_rules:v2 -f Model/Dockerfile.model .
docker push gustavofcunha/recommendation_rules:v2
docker build -t gustavofcunha/rest_api_server:v2 -f APIs/Dockerfile.api .
docker push gustavofcunha/rest_api_server:v2
