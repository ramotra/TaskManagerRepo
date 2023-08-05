#!/bin/bash
set -x
# cp /app/secrets/taskmanager /usr/src/app/taskmanager/local_settings.py

echo Starting gunicorn

exec gunicorn \
--workers 5 \
--timeout 600 \
--bind=0.0.0.0:8000 \
taskmanager.wsgi
