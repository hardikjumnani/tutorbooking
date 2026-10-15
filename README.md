# TutorSlot

A simple **tutoring appointment booking system**. Students book a tutor for a
subject at a chosen time. The app is small on purpose — the goal is to show the
full DevOps journey: from code on a laptop to a monitored Kubernetes cluster on AWS.

## What it does

- Book a tutoring session (student, tutor, subject, date/time).
- See all sessions, filter by status, change status, or delete.
- Live counts by status (Booked / Confirmed / Done) on the dashboard.

## Architecture

```text
            Browser
               |
        React + Nginx  (frontend)
               |  /api
         FastAPI  (backend)  --->  PostgreSQL
               |
            /metrics
               |
        Prometheus  --->  Grafana

Pipeline:  Git push -> GitHub Actions -> pytest -> build images
           -> Trivy scan -> push to GHCR (tagged by commit SHA)

Cloud:     Terraform -> AWS VPC + EKS -> Helm -> Ingress + HPA
```

## Tech stack

| Layer | Tools |
|-------|-------|
| Frontend | React + Vite, served by Nginx |
| Backend | FastAPI (Python), SQLAlchemy, Alembic |
| Database | PostgreSQL (SQLite for quick local dev) |
| Tests | pytest |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Security | Trivy image scanning |
| Registry | GitHub Container Registry (GHCR) |
| Infrastructure | Terraform (AWS VPC + EKS) |
| Deployment | Kubernetes + Helm (Ingress, HPA) |
| Monitoring | Prometheus + Grafana |

## Repository structure

```text
tutorslot/
├── backend/            # FastAPI app, tests, Alembic migrations, Dockerfile
├── frontend/           # React + Vite app, Nginx config, Dockerfile
├── docker-compose.yml  # full local stack (frontend + backend + postgres)
├── .github/workflows/  # CI/CD pipeline
├── terraform/          # AWS VPC + EKS (Infrastructure as Code)
├── helm/tutorslot/     # Helm chart for Kubernetes
├── k8s/                # namespace manifest
├── monitoring/         # Prometheus + Grafana config and dashboard
├── scripts/            # load-test helper (for the HPA demo)
├── DEPLOY.md           # step-by-step AWS deploy runbook
└── SUBMISSION.md       # how each grading module maps to evidence
```

## Run locally — the easy way (Docker)

```bash
docker compose up --build
```

- App: http://localhost:3000
- Backend API docs: http://localhost:8001/docs

Stop with `docker compose down` (add `-v` to also delete the database).

> The backend is published on host port **8001** (port 8000 is often taken by
> other apps). Inside the containers it still uses 8000.

## Run the backend without Docker

No database setup needed — it defaults to a local SQLite file.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows (use source .venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8010
```

Open http://localhost:8010/docs. To also run the UI:

```bash
cd frontend
set VITE_API_TARGET=http://localhost:8010    # point the dev proxy at the backend
npm install
npm run dev                                   # opens http://localhost:5173
```

## Run the tests

```bash
cd backend
pytest -q
```

## CI/CD

On every push to `main`, GitHub Actions (`.github/workflows/ci-cd.yml`):

1. runs **pytest** and builds the frontend (quality gate),
2. builds the backend and frontend **Docker images**,
3. scans both with **Trivy** (fails on HIGH/CRITICAL vulnerabilities),
4. pushes them to **GHCR**, tagged with the commit SHA.

## Deploy to AWS

See **[DEPLOY.md](DEPLOY.md)** for the full runbook (Terraform → Helm →
monitoring → teardown). Details also live in
[`terraform/README.md`](terraform/README.md) and
[`monitoring/README.md`](monitoring/README.md).

## API endpoints

| Method | Path | What it does |
|--------|------|--------------|
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness check (verifies the database) |
| GET | `/metrics` | Prometheus metrics |
| GET | `/api/appointments` | List all appointments |
| GET | `/api/appointments/stats` | Counts by status |
| GET | `/api/appointments/{id}` | Get one appointment |
| POST | `/api/appointments` | Create an appointment |
| PUT | `/api/appointments/{id}` | Update an appointment |
| DELETE | `/api/appointments/{id}` | Delete an appointment |
