FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ARG PIP_NO_CACHE_DIR=1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . /app 
    
CMD ["python", "app.py"]