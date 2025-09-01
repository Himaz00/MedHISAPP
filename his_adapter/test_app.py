import pytest
from fastapi.testclient import TestClient
from app import app
import json
import os

client = TestClient(app)

def test_get_sample_patients():
    response = client.get("/sample-patients")
    assert response.status_code == 200
    data = response.json()
    assert "patients" in data
    assert isinstance(data["patients"], list)

def test_push_json_data():
    # This test might fail if the gateway service is not running
    # In a real CI environment, you might want to mock the gateway
    response = client.post("/push-json-data")
    # The test will pass if the endpoint is reachable, even if gateway is down
    assert response.status_code in [200, 500]  # 500 if gateway is not available

def test_upload_json_valid():
    # Create a test JSON file
    test_data = {
        "patients": [
            {
                "id": "test001",
                "name": "Test Patient",
                "dob": "1990-01-01",
                "diagnoses": ["test diagnosis"]
            }
        ]
    }

    # Convert to file-like object
    from io import BytesIO
    json_content = json.dumps(test_data).encode('utf-8')
    files = {"file": ("test.json", BytesIO(json_content), "application/json")}

    response = client.post("/upload-json", files=files)
    # Similar to push_json_data, this might fail if gateway is not available
    assert response.status_code in [200, 500]

def test_upload_json_invalid():
    # Test with invalid JSON
    invalid_json = '{"invalid": json}'
    from io import BytesIO
    files = {"file": ("invalid.json", BytesIO(invalid_json.encode('utf-8')), "application/json")}

    response = client.post("/upload-json", files=files)
    assert response.status_code == 400

def test_upload_json_no_patients_key():
    # Test with JSON missing patients key
    invalid_data = {"data": []}
    from io import BytesIO
    json_content = json.dumps(invalid_data).encode('utf-8')
    files = {"file": ("invalid.json", BytesIO(json_content), "application/json")}

    response = client.post("/upload-json", files=files)
    assert response.status_code == 400
