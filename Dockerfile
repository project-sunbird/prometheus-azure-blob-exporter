FROM python:2.7.14-alpine3.6

COPY app /opt/prometheus-azure-blob-exporter

RUN apk add --no-cache gcc libffi-dev musl-dev openssl-dev perl py-pip python python-dev

RUN pip install -r /opt/prometheus-azure-blob-exporter/requirements.txt

EXPOSE 9358

ENTRYPOINT ["python", "/opt/prometheus-azure-blob-exporter/exporter.py"]