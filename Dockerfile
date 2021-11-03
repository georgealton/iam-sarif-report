FROM python:3.9.7-alpine
RUN apk add --no-cache bash git wget
RUN pip install git+https://github.com/georgealton/iam-policy-validator-to-sarif.git
COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
