# TutorSlot

A simple tutoring appointment booking system. Students book a tutor for a subject at a chosen time.

This project is built for the DevOps capstone: it goes from code on a laptop all the way to a monitored Kubernetes deployment.

## Tech stack

- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (SQLite for quick local dev)
- **ORM / migrations:** SQLAlchemy + Alembic
- **Tests:** pytest
- **Containers:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Security scan:** Trivy
- **Registry:** GitHub Container Registry (GHCR)
- **Infrastructure:** Terraform (AWS VPC + EKS)
- **Deployment:** Kubernetes + Helm (Ingress, HPA)
- **Monitoring:** Prometheus + Grafana

## Run the backend locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Then open:

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

No database setup is needed for local dev — the app uses a SQLite file by default.

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
