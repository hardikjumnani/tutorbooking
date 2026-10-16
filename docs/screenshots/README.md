# Screenshots — evidence per module

Captured from the real running app, test run, Docker stack, CI pipeline, and a
real Kubernetes cluster (a local `kind` cluster running the exact same Helm chart,
Ingress, HPA, and monitoring config used for the AWS deployment).

## Captured

| File | Module | Shows |
|------|--------|-------|
| `m1_app_dashboard.png` | M1, M4 | The app at http://localhost:3000 with appointments and status counts |
| `m1_swagger_docs.png` | M1 | FastAPI Swagger docs — all REST endpoints (GET/POST/PUT/DELETE) |
| `m2_pytest.png` | M2 | `pytest -v`: 10 tests passing |
| `m3_git_log.png` | M3 | `git log`: meaningful commit history |
| `m4_compose_ps.png` | M4 | `docker compose ps`: all 3 services up (postgres healthy) |
| `m4_nonroot.png` | M4 | Containers run non-root (backend uid 10001, frontend uid 101) |
| `m4_images.png` | M4 | Built backend and frontend images |
| `m5_pipeline_run.png` | M5 | GitHub Actions run: green, `test` + `build-scan-push` passed |
| `m5_ghcr_packages.png` | M5 | GHCR packages list: `tutorslot-backend` and `tutorslot-frontend` |
| `m5_ghcr_backend_tags.png` | M5 | Package page with the commit-SHA image tags and pull command |
| `m6_trivy_scan.png` | M6 | Trivy scan: 0 HIGH/CRITICAL on both images |
| `m8_pods.png` | M8 | `kubectl get pods`: all 5 pods Running (2 backend, 2 frontend, 1 postgres) |
| `m8_deployments.png` | M8 | Deployments at 2/2 replicas each |
| `m8_services.png` | M8 | ClusterIP services: `backend`, `frontend`, `postgres` |
| `m8_ingress.png` | M8 | Ingress resource (host `tutorslot.local`, class nginx) |
| `m8_helm_list.png` | M8 | `helm list`: release `tutorslot` deployed |
| `m8_hpa.png` | M8 | HPA live (`cpu: 3%/60%`, 2–6 replicas) + `kubectl top pods` |
| `m8_app_via_ingress.png` | M8 | The app opened through the Ingress hostname |
| `m8_api_via_ingress.png` | M8 | `/api` route answered by the backend through the Ingress |
| `m9_metrics_endpoint.png` | M9 | `curl /metrics`: Prometheus-format output from the backend |
| `m9_monitoring_pods.png` | M9 | Prometheus + Grafana pods Running |
| `m9_prometheus_targets.png` | M9 | Prometheus Targets: `tutorslot-backend` scrape target 2/2 UP |
| `m9_grafana_dashboard.png` | M9 | Grafana panels with live request rate and p95 latency |
| `m10_before.png` | M10 | Live demo, before: Helm revision 2, app 1.0.0, image tag `d514cc6` |
| `m10_pipeline_run.png` | M10 | Live demo: the v1.1 commit's pipeline run, green |
| `m10_after.png` | M10 | Live demo, after: `helm upgrade` → revision 3, app 1.1.0, new image tag, pods rolled |
| `m10_app_after_update.png` | M10 | Live demo: the running app (via Ingress) now shows v1.1 |

## Still to capture

- **M7 — Terraform on AWS:** `terraform plan` output, AWS console (VPC + EKS),
  `terraform destroy` output. Needs an AWS account — see [`../../DEPLOY.md`](../../DEPLOY.md).

## Notes

- **M8 / M9** were captured on a local Kubernetes cluster (`kind`), deploying the same
  `helm/tutorslot` chart with the same values, Ingress controller, Metrics Server,
  and `kube-prometheus-stack` monitoring that the AWS runbook uses.
- **M10** live demo flow: commit `0f7d722` (bump to v1.1) → GitHub Actions run green
  → `helm upgrade` to the new SHA-tagged images → rolling update → app shows v1.1.
  It can be repeated live on request.
