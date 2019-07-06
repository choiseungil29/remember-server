#!/bin/sh

if [ "$1" = "revision" ];then
  docker-compose build alembic
fi
docker-compose run alembic alembic $@