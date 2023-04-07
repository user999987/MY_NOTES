Two ways to push log to loki
## 1. promtail
```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
- job_name: app
  pipeline_stages:
    - json:
        expressions:
          level: level
          time: timestamp
    - timestamp:
        source: time
        format: RFC3339Nano
    - drop:
        older_than: 168h # 7 days in hours
  static_configs:
  - targets:
      - localhost
    labels:
      author: usr1
      __path__: /var/log/usr1/*log
  - targets:
      - localhost
    labels:
      author: usr2
      __path__: /var/log/usr2/*log
```
There are more config properties you can set in this yaml 

## 2. Hit POST API directly (ref: https://grafana.com/docs/loki/latest/api/#push-log-entries-to-loki)
```bash
curl --location --request POST 'http://localhost:3100/loki/api/v1/push' \
--header 'Content-Type: application/json' \
--data-raw '{
    "streams": [
        {
            "stream": {
                "author": "wayne"
            },
            "values": [
                [
                    "1680835239000000000",
                    "{\"level\":\"INFO\",\"timestamp\":\"2023-03-30T04:01:09Z\",\"caller\":\"logging/initLog.go:51\",\"func\":\"xcloud/paymentchannel/internal/infra/logging.InitLog\",\"message\":\"Log starts to work...\"}"
                ]
            ]
        }
    ]
}'
```