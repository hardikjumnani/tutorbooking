# Submission guide

How each grading module maps to this repo, and what to capture for it.
Repo: https://github.com/hardikjumnani/tutorbooking

Screenshots marked **[cloud]** need the AWS deploy session (see [DEPLOY.md](DEPLOY.md)).

| Module | In this repo | Evidence to submit |
|--------|--------------|--------------------|
| **M1** App (10) | `backend/app/`, `backend/alembic/versions/`, `frontend/`, `docker-compose.yml` | Screenshot of the app in the browser (http://localhost:3000) with an appointment created |
| **M2** Testing (10) | `backend/tests/`, `backend/conftest`/`pytest.ini` | `cd backend && pytest -v` output (10 tests passing) |
| **M3** Git/GitHub (5) | whole repo, `.gitignore` | Repo URL (public) + commit history (11+ commits) |
| **M4** Docker (10) | `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml` | `docker compose up --build` terminal + browser at localhost:3000 |
| **M5** CI/CD (15) | `.github/workflows/ci-cd.yml` | Green pipeline run URL + GHCR packages page (SHA tags) |
| **M6** Trivy (5) | Trivy steps in the workflow | Trivy step output in a run + the 2–3 sentence note below |
| **M7** Terraform (15) | `terraform/` | **[cloud]** `terraform plan` output + AWS console (VPC + EKS) + `terraform destroy` output |
| **M8** K8s + Helm (15) | `helm/tutorslot/`, `k8s/namespace.yaml` | **[cloud]** `kubectl get pods/svc`, `helm list`, app via Ingress |
| **M9** Monitoring (10) | `monitoring/` | **[cloud]** `/metrics` output, Prometheus Targets UP, Grafana panel |
| **M10** Docs + demo (5) | `README.md`, this file | README (done) + live demo: push a change, watch the pipeline, see the deploy update |

## Status right now

- **Done & verified:** M1, M2, M3, M4, M5, M6 (pipeline is green; CVEs found and fixed).
- **Code complete, needs the cloud session:** M7, M8, M9.
- **M10:** README is done; the live demo is part of the cloud session.

## Module 6 — Trivy explanation (ready to paste)

> Trivy scanned both container images — their OS packages and application
> libraries — against a known-vulnerability (CVE) database, set to fail the
> build on any HIGH or CRITICAL issue that has a fix. It caught 3 HIGH CVEs in
> the Python `starlette` library and 41 in the frontend's Alpine/OpenSSL
> packages. We fixed them by upgrading the affected packages and the Nginx base
> image, so the scan now passes clean — no known, fixable high-severity
> vulnerabilities ship in our images.

## Before you submit

- [ ] Repo is **public** and all links work.
- [ ] You submit the form with your **SST email** (`hardik.24bcs10025@sst.scaler.com`).
- [ ] No AWS keys anywhere in the git history.
- [ ] You ran `terraform destroy` after capturing the cloud screenshots.
