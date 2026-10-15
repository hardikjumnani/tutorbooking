"""Tests for the TutorSlot appointment API.

Covered endpoints: /health, /ready, and the full /api/appointments CRUD
plus /api/appointments/stats.
"""


def sample(**overrides):
    """Build a valid appointment payload; override any field as needed."""
    data = {
        "student_name": "Aarav",
        "tutor": "Ms. Rao",
        "subject": "Mathematics",
        "class_time": "2026-10-20T10:00:00",
    }
    data.update(overrides)
    return data


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "UP"}


def test_ready(client):
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json() == {"status": "READY"}


def test_create_appointment(client):
    res = client.post("/api/appointments", json=sample())
    assert res.status_code == 201
    body = res.json()
    assert body["student_name"] == "Aarav"
    assert body["status"] == "BOOKED"  # default applied
    assert "id" in body


def test_list_appointments(client):
    client.post("/api/appointments", json=sample(student_name="Diya"))
    client.post("/api/appointments", json=sample(student_name="Kabir"))
    res = client.get("/api/appointments")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_single_appointment(client):
    created = client.post("/api/appointments", json=sample()).json()
    res = client.get(f"/api/appointments/{created['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == created["id"]


def test_get_missing_appointment_returns_404(client):
    res = client.get("/api/appointments/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Appointment not found"


def test_update_appointment_status(client):
    created = client.post("/api/appointments", json=sample()).json()
    res = client.put(f"/api/appointments/{created['id']}", json={"status": "CONFIRMED"})
    assert res.status_code == 200
    assert res.json()["status"] == "CONFIRMED"


def test_delete_appointment(client):
    created = client.post("/api/appointments", json=sample()).json()
    res = client.delete(f"/api/appointments/{created['id']}")
    assert res.status_code == 204
    # It should be gone now.
    assert client.get(f"/api/appointments/{created['id']}").status_code == 404


def test_stats_counts_by_status(client):
    client.post("/api/appointments", json=sample(status="BOOKED"))
    client.post("/api/appointments", json=sample(status="CONFIRMED"))
    client.post("/api/appointments", json=sample(status="DONE"))
    res = client.get("/api/appointments/stats")
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 3
    assert body["booked"] == 1
    assert body["confirmed"] == 1
    assert body["done"] == 1


def test_create_rejects_missing_fields(client):
    # Missing required fields (tutor, subject, class_time) -> validation error.
    res = client.post("/api/appointments", json={"student_name": "Aarav"})
    assert res.status_code == 422
