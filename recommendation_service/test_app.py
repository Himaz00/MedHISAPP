import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_run_recommendations_hypertension():
    patient_data = {
        "id": "test001",
        "name": "Test Patient",
        "dob": "1980-01-01",
        "diagnoses": ["Bluthochdruck"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    # Check if hypertension recommendation is present
    hypertension_rec = any("Blutdruck" in rec["text"] for rec in recommendations)
    assert hypertension_rec

def test_run_recommendations_diabetes():
    patient_data = {
        "id": "test002",
        "name": "Test Patient",
        "dob": "1975-06-15",
        "diagnoses": ["Diabetes mellitus"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    # Check if diabetes recommendation is present
    diabetes_rec = any("Blutzucker" in rec["text"] for rec in recommendations)
    assert diabetes_rec

def test_run_recommendations_asthma():
    patient_data = {
        "id": "test003",
        "name": "Test Patient",
        "dob": "1995-03-20",
        "diagnoses": ["Asthma bronchiale"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    # Check if asthma recommendation is present
    asthma_rec = any("Inhalator" in rec["text"] for rec in recommendations)
    assert asthma_rec

def test_run_recommendations_heart_disease():
    patient_data = {
        "id": "test004",
        "name": "Test Patient",
        "dob": "1960-12-10",
        "diagnoses": ["Herzkrankheit"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    # Check if heart disease recommendation is present
    heart_rec = any("Kardiologie" in rec["text"] for rec in recommendations)
    assert heart_rec

def test_run_recommendations_migraine():
    patient_data = {
        "id": "test005",
        "name": "Test Patient",
        "dob": "1988-09-05",
        "diagnoses": ["Migräne"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    # Check if migraine recommendation is present
    migraine_rec = any("Kopfschmerztagebuch" in rec["text"] for rec in recommendations)
    assert migraine_rec

def test_run_recommendations_elderly():
    patient_data = {
        "id": "test006",
        "name": "Elderly Patient",
        "dob": "1955-07-22",
        "diagnoses": ["Some diagnosis"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    # Check if elderly recommendation is present
    elderly_rec = any("Pneumokokken" in rec["text"] for rec in recommendations)
    assert elderly_rec

def test_run_recommendations_no_match():
    patient_data = {
        "id": "test007",
        "name": "Test Patient",
        "dob": "1990-01-01",
        "diagnoses": ["Unknown diagnosis"]
    }
    response = client.post("/", json=patient_data)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    # Should return default recommendation
    assert len(recommendations) == 1
    assert "keine besonderen Empfehlungen" in recommendations[0]["text"]
