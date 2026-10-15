# Screenshots — evidence per module

Captured from the real running app, test run, Docker stack, and pipeline.

## Captured (local evidence)

| File | Module | Shows |
|------|--------|-------|
| `m1_app_dashboard.png` | M1, M4 | The app at http://localhost:3000 with appointments and status counts |
| `m1_swagger_docs.png` | M1 | FastAPI Swagger docs — all REST endpoints (GET/POST/PUT/DELETE) |
| `m2_pytest.png` | M2 | `pytest -v`: 10 tests passing |
| `m3_git_log.png` | M3 | `git log`: 12 meaningful commits |
| `m4_compose_ps.png` | M4 | `docker compose ps`: all 3 services up (postgres healthy) |
| `m4_nonroot.png` | M4 | Containers run non-root (backend uid 10001, frontend uid 101) |
| `m4_images.png` | M4 | Built backend and frontend images |
| `m5_pipeline_run.png` | M5 | GitHub Actions run: green, `test` + `build-scan-push` passed |
| `m5_ghcr_packages.png` | M5 | GHCR packages list: `tutorslot-backend` and `tutorslot-frontend` |
| `m5_ghcr_backend_tags.png` | M5 | Package page with the commit-SHA image tags and pull command |
| `m6_trivy_scan.png` | M6 | Trivy scan: 0 HIGH/CRITICAL on both images |

## Still to capture

- **M7 / M8 / M9 — cloud** (during the AWS session; see [`../../DEPLOY.md`](../../DEPLOY.md)):
  - M7: `terraform plan`, AWS console (VPC + EKS), `terraform destroy`
  - M8: `kubectl get pods/svc`, `helm list`, app through the Ingress
  - M9: `/metrics` output, Prometheus Targets UP, a Grafana panel with live data
