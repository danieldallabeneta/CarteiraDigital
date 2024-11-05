FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app3

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3", "run.py"]