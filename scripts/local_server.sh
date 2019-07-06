#!/bin/sh

docker-compose build app
docker-compose run --service-ports app
