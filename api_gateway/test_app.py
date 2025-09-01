import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_ingest_patient():
    patient_data = {
        "id": "test123",
        "name": "Test Patient",
        "dob": "1990-01-01",
        "diagnoses": ["diabetes"]
    }
    response = client.post("/ingest", json=patient_data)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["patient_id"] == "test123"

    # Verify patient was stored with empty recommendations (since recommendation service is not available)
    stored_patient = client.get("/patients/test123")
    assert stored_patient.status_code == 200
    patient_data = stored_patient.json()
    assert patient_data["id"] == "test123"
    assert patient_data["name"] == "Test Patient"
    assert "recommendations" in patient_data
    assert patient_data["recommendations"] == []

def test_get_patient():
    # First ingest a patient
    patient_data = {
        "id": "test456",
        "name": "Test Patient 2",
        "dob": "1985-05-15",
        "diagnoses": ["asthma"]
    }
    client.post("/ingest", json=patient_data)

    # Then retrieve it
    response = client.get("/patients/test456")
    assert response.status_code == 200
    assert response.json()["id"] == "test456"
    assert response.json()["name"] == "Test Patient 2"

def test_get_nonexistent_patient():
    response = client.get("/patients/nonexistent")
    assert response.status_code == 404

def test_list_patients():
    response = client.get("/patients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_clear_patients():
    response = client.post("/clear-patients")
    assert response.status_code == 200
    assert "cleared_count" in response.json()
