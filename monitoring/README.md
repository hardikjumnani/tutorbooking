# Monitoring — Prometheus + Grafana

Installed with the **kube-prometheus-stack** Helm chart (Prometheus Operator,
Prometheus, Grafana, and default dashboards). The app exposes metrics at
`/metrics`; our ServiceMonitor tells Prometheus to scrape it.

## Install (after the cluster and the app are running)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack \
  prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f monitoring/prometheus-values.yaml

# Turn on our ServiceMonitor so Prometheus scrapes the app:
helm upgrade tutorslot ./helm/tutorslot -n tutorslot \
  --reuse-values --set monitoring.serviceMonitor.enabled=true
```

## Open the dashboards

```bash
# Grafana (user: admin, password: tutorslot-admin)
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3001:80

# Prometheus (check Status > Targets: the app should show as UP)
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
```

- Grafana: http://localhost:3001 — import `monitoring/grafana-dashboard.json`
  via **Dashboards > New > Import**, then pick the Prometheus data source.
- Prometheus: http://localhost:9090 — **Status > Targets** should list the
  `tutorslot-backend` target as UP.

## Useful queries (our app's metrics)

| What | Query |
|------|-------|
| Request rate | `sum(rate(http_requests_total[1m]))` |
| Rate by endpoint | `sum by (handler) (rate(http_requests_total[1m]))` |
| 95th percentile latency | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` |
| Total requests | `sum(http_requests_total)` |
