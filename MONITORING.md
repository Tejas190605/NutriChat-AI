# Monitoring & Telemetry Guide (MONITORING.md)

## Prometheus Telemetry
- Prometheus scrapes backend `/metrics` endpoint on port 9090.
- Grafana dashboard accessible on `http://localhost:3001` (Default login: admin/admin).

## Tracked Metrics
- `http_requests_total`: Total inbound HTTP requests count.
- `http_request_duration_seconds`: Response latency histogram.
- `active_websocket_connections`: Real-time SSE / WebSocket connection counts.
