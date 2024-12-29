#!/bin/bash

docker build -t gustavofcunha/recommendation_rules:v3 -f Model/Dockerfile.model .
docker push gustavofcunha/recommendation_rules:v3
docker build -t gustavofcunha/rest_api_server:v3 -f APIs/Dockerfile.api .
docker push gustavofcunha/rest_api_server:v3
