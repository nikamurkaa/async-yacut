#!/bin/sh
set -eu

flask db upgrade

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4 \
    --timeout 180 \
    --access-logfile - \
    --error-logfile - \
    yacut:app
