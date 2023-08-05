#build stage 1
FROM python:3.8

# WORKDIR /taskmanager

RUN apt-get update && apt-get install -y \
    python3-psycopg2 \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . taskmanager
WORKDIR /taskmanager
EXPOSE 8000

ENTRYPOINT ["python", "taskmanager/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]