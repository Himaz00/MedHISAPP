from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests, os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RECOMM_URL = os.environ.get('RECOMM_URL', 'http://recommendation_service:8001/')

class Patient(BaseModel):
    id: str
    name: str
    dob: str # Date of birth
    diagnoses: list = []

PATIENTS = {}

# Function to ingest patient data: This POST endpoint accepts patient data and stores it in an in-memory dictionary.
@app.post("/ingest")
def ingest(p: Patient):
    PATIENTS[p.id] = p.dict()
    try:
        r = requests.post(RECOMM_URL, json=p.dict(), timeout=5)
        r.raise_for_status()
        recs = r.json()
        PATIENTS[p.id]['recommendations'] = recs
    except Exception as e:
        # If recommendation service is unavailable, store patient without recommendations
        # This makes the service more resilient and allows testing without external dependencies
        PATIENTS[p.id]['recommendations'] = []
    return {"status": "ok", "patient_id": p.id}

# Function to retrieve a specific patient by ID: This GET endpoint retrieves the data for a specific patient by their ID.
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    p = PATIENTS.get(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

# Function to list all patients: This GET endpoint returns a list of all patients currently stored in the system.
@app.get("/patients")
def list_patients():
    return list(PATIENTS.values())

# Function to clear all patients: This POST endpoint clears all patient data from the system.
@app.post("/clear-patients")
def clear_patients():
    cleared_count = len(PATIENTS)
    PATIENTS.clear()
    return {"status": "cleared", "cleared_count": cleared_count}