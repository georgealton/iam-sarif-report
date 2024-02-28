FROM python:3.12-alpine
RUN apk add --no-cache bash git wget

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

COPY . .
ARG PSEUDO_VERSION=1
RUN SETUPTOOLS_SCM_PRETEND_VERSION=${PSEUDO_VERSION} pip install --upgrade --no-cache-dir --quiet --no-input .
RUN chmod +x /scripts/entrypoint.sh
ENTRYPOINT ["/scripts/entrypoint.sh"]
