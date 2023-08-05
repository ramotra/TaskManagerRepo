#!/bin/bash
set -x
# cp /app/secrets/taskmanager /usr/src/app/taskmanager/local_settings.py

echo Starting celery service

exec celery \
--app=taskmanager \
worker \
--concurrency=2
