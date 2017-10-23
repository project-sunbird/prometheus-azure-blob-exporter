#!/usr/bin/python

import time
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import argparse
import yaml
import logging
from azure.storage.blob import BlockBlobService

DEFAULT_PORT=9358
DEFAULT_LOG_LEVEL='info'

def datetime_to_timestamp(datetime_value):
  return time.mktime(datetime_value.timetuple()) * 1000 + datetime_value.microsecond / 1000

class AzureBlobStorageCollector(object):
  def __init__(self, config):
    self._config = config

  def collect(self):
    azure_blob_storage_account_name = self._config['azure_blob_storage_account_name']
    azure_blob_storage_account_key = self._config['azure_blob_storage_account_key']
    azure_blob_storage_containers = self._config['azure_blob_storage_containers']

    blob_service = BlockBlobService(account_name=azure_blob_storage_account_name, account_key=azure_blob_storage_account_key)
    azure_blob_latest_file_timestamp_gauge = GaugeMetricFamily('azure_blob_latest_file_timestamp', 'Last modified timestamp for latest file in container', labels=['container'])
    azure_blob_oldest_file_timestamp_gauge = GaugeMetricFamily('azure_blob_oldest_file_timestamp', 'Last modified timestamp for oldest file in container', labels=['container'])
    for container in azure_blob_storage_containers:
      blobs_generator = blob_service.list_blobs(container)
      blob_last_modified_times = [blob.properties.last_modified for blob in blobs_generator]
      latest_file_time = max(blob_last_modified_times)
      oldest_file_time = min(blob_last_modified_times)
      azure_blob_latest_file_timestamp_gauge.add_metric([container], datetime_to_timestamp(latest_file_time))
      azure_blob_oldest_file_timestamp_gauge.add_metric([container], datetime_to_timestamp(oldest_file_time))
    yield azure_blob_latest_file_timestamp_gauge
    yield azure_blob_oldest_file_timestamp_gauge


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Expose metrics for azure blob storage')
  parser.add_argument('config_file_path', help='Path of the config file')
  args = parser.parse_args()
  with open(args.config_file_path) as config_file:
    config = yaml.load(config_file)
    log_level = config.get('log_level', DEFAULT_LOG_LEVEL)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.getLevelName(log_level.upper()))
    exporter_port = config.get('exporter_port', DEFAULT_PORT)
    logging.debug("Config %s", config)
    logging.info('Starting server on port %s', exporter_port)
    start_http_server(exporter_port)
    REGISTRY.register(AzureBlobStorageCollector(config))
  while True: time.sleep(1)