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
# HELP azure_blob_latest_file_timestamp Last modified timestamp(milliseconds) for latest file in container
# TYPE azure_blob_latest_file_timestamp gauge
azure_blob_latest_file_timestamp{container="cassandra-backup"} 1508697219000.0
azure_blob_latest_file_timestamp{container="postgresql-backup"} 1508707802000.0
# HELP azure_blob_oldest_file_timestamp Last modified timestamp(milliseconds) for oldest file in container
# TYPE azure_blob_oldest_file_timestamp gauge
azure_blob_oldest_file_timestamp{container="cassandra-backup"} 1506191638000.0
azure_blob_oldest_file_timestamp{container="postgresql-backup"} 1506202237000.0
# HELP azure_blob_latest_file_size Size in bytes for latest file in container
# TYPE azure_blob_latest_file_size gauge
azure_blob_latest_file_size{container="cassandra-backup"} 3065762.0
azure_blob_latest_file_size{container="postgresql-backup"} 5606443.0
# HELP azure_blob_oldest_file_size Size in bytes for oldest file in container
# TYPE azure_blob_oldest_file_size gauge
azure_blob_oldest_file_size{container="cassandra-backup"} 2425517.0
azure_blob_oldest_file_size{container="postgresql-backup"} 3392110.0
```

### Alert Example

* Alert for time of latest backup. This example checks backup is created every day

```
# 24 hours + 1 hour slack time for backup process
# threshold_interval_in_milliseconds => 25 * 60 * 60 * 1000 => 90000000
ALERT backup_is_too_old
  IF (time() * 1000) - azure_blob_latest_file_timestamp > 90000000
  FOR 5m
  ANNOTATIONS {
      summary = "Backup is too old",
      description = "There is no backup file created for a day in {{ $labels.container }}",
  }
```

* Alert for size of latest backup. This example checks latest backup file created has minimum size of 1MB

```
# threshold_size_in_bytes => 1MB => 1000000
ALERT backup_size_is_too_small
  IF azure_blob_latest_file_size < 1000000
  FOR 5m
  ANNOTATIONS {
      summary = "Backup size is too small",
      description = "Latest backup file is smaller than 1MB in {{ $labels.container }}",
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