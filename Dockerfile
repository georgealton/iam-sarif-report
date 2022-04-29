FROM python:3.9-alpine
RUN apk add --no-cache bash git wget

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
    pip install \
        --upgrade \
        --no-cache-dir \
        git+https://github.com/georgealton/iam-sarif-report.git

COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
