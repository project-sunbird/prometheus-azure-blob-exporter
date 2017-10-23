# prometheus-azure-blob-exporter

Prometheus metrics exporter for azure blob storage

### Config example

```yml
exporter_port: 9358 # Port on which Prometheus can call this exporter to get metrics
log_level: info
azure_blob_storage_account_name: '<azure_blob_storage_account_name>'
azure_blob_storage_account_key: '<azure_blob_storage_account_key>'
containers: ['cassandra-backup', 'postgresql-backup']
```

### Metrics

Metrics will available in http://localhost:9358

```sh
$ curl -s localhost:9358
# HELP azure_blob_latest_file_timestamp Last modified timestamp for latest file in container
# TYPE azure_blob_latest_file_timestamp gauge
azure_blob_latest_file_timestamp{container="cassandra-backup"} 1508438059000.0
azure_blob_latest_file_timestamp{container="postgresql-backup"} 1508448600000.0
# HELP azure_blob_oldest_file_timestamp Last modified timestamp for oldest file in container
# TYPE azure_blob_oldest_file_timestamp gauge
azure_blob_oldest_file_timestamp{container="cassandra-backup"} 1505932457000.0
azure_blob_oldest_file_timestamp{container="postgresql-backup"} 1505943016000.0```
```

### Alert Example

```
# Example alert for daily backup
number_of_milliseconds_in_hour = 1 * 60 * 60 * 1000
number_of_milliseconds_in_day = 24 * number_of_milliseconds_in_hour
# Include a slack time for backup process
max_number_of_allowed_milliseconds =  number_of_milliseconds_in_day+ number_of_milliseconds_in_hour

ALERT stale_backup
  IF time() - azure_blob_latest_file_timestamp > max_number_of_allowed_milliseconds
  FOR 5m
  ANNOTATIONS {
      summary = "Backup is stale",
      description = "There is no backup file created for a day in {{ $labels.container }}",
  }
```

### Run

#### Using code (local)

```
# Ensure python 2.x and pip installed
pip install -r app/requirements.txt
python app/exporter.py example/config.yml
```

#### Using docker

```
docker run -p 9358:9358 -v $(pwd)/example/config.yml:/etc/prometheus-azure-blob-exporter/config.yml sunbird/prometheus-azure-blob-exporter /etc/prometheus-azure-blob-exporter/config.yml
```