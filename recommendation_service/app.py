# recommendation_service/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Recommendation Service")

class Patient(BaseModel):
    id: str
    name: str
    dob: str
    diagnoses: List[str] = []

# Function to run recommendations based on patient diagnoses and age.
@app.post("/", response_model=List[dict])
def run_recommendations(p: Patient):
    recs = []
    # Simple example rules
    diag_lower = [d.lower() for d in p.diagnoses]
    if any("bluthochdruck" in d for d in diag_lower):
        recs.append({"text": "Blutdruck kontrollieren, bei Bedarf ACE-Hemmer in Betracht ziehen."})
    if any("diabetes" in d for d in diag_lower):
        recs.append({"text": "Blutzuckerspiegel überwachen, bei Bedarf Metformin in Betracht ziehen."})
    if any("asthma" in d for d in diag_lower):
        recs.append({"text": "Inhalator wie verordnet verwenden, Auslöser vermeiden."})
    if any("herzkrankheit" in d for d in diag_lower):
        recs.append({"text": "Regelmäßige Kardiologie-Untersuchungen, Betablocker in Betracht ziehen."})
    if any("migräne" in d for d in diag_lower):
        recs.append({"text": "Kopfschmerztagebuch führen, Triptane für akute Anfälle in Betracht ziehen."})

    try:
        year = int(p.dob.split("-")[0])
        if year <= 1959:
            recs.append({"text": "Bewertung der Pneumokokken-Impfung bei älteren Menschen."})
    except:
        pass
    if not recs:
        recs.append({"text": "Es gibt keine besonderen Empfehlungen."})
    return recs


