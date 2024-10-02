#!/usr/bin/env bash
# -*- coding: utf-8 -*-
export ENVIRONMENT=local
export PYTHONDONTWRITEBYTECODE=1
main_env=src/.env

docker compose -f docker/docker-compose-core.yml up --build
docker compose -f docker/docker-compose-core.yml down
exit
