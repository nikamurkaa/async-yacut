#!/bin/sh
set -eu

docker compose \
    -f /opt/yacut/infra/compose.yml \
    exec -T nginx nginx -s reload
