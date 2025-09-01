from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests, json, os, time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
GATEWAY_URL = os.environ.get('GATEWAY_URL', 'http://api_gateway:8000')

# Function to push sample patient data: reads sample_patients.json, clears existing patients, sends each patient to the API Gateway /ingest endpoint, and returns the number of successfully sent patients.
@app.post('/push-json-data')
def push_sample():
    # Clear existing patients first
    try:
        clear_resp = requests.post(f'{GATEWAY_URL}/clear-patients', timeout=5)
        clear_resp.raise_for_status()
        print("Cleared existing patients")
    except Exception as e:
        print("Failed to clear patients:", str(e))
        raise HTTPException(status_code=500, detail='Failed to clear existing patients')

    with open('sample_patients.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    sent = 0
    for p in data.get('patients', []):
        try:
            resp = requests.post(f'{GATEWAY_URL}/ingest', json=p, timeout=5)
            resp.raise_for_status()  # checks the HTTP status code of the response and raises an exception if the request was not successful.
            sent += 1
        except Exception as e:
            print("Failed to send patient:", p.get('id'), str(e))
        time.sleep(0.1)
    return {'sent': sent}

@app.get('/sample-patients')
def get_sample_patients():
    try:
        with open('sample_patients.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except:
        return {'patients': []}

@app.post('/upload-json')
def upload_json(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='No selected file')
    content = file.file.read()
    try:
        data = json.loads(content)
        if 'patients' not in data or not isinstance(data['patients'], list):
            raise HTTPException(status_code=400, detail='Invalid JSON format. Must have "patients" as list.')
    except:
        raise HTTPException(status_code=400, detail='Invalid JSON file')
    with open('sample_patients.json', 'w', encoding='utf-8') as f:
        f.write(content.decode('utf-8'))

    # Clear existing patients first
    try:
        clear_resp = requests.post(f'{GATEWAY_URL}/clear-patients', timeout=5)
        clear_resp.raise_for_status()
        print("Cleared existing patients")
    except Exception as e:
        print("Failed to clear patients:", str(e))
        raise HTTPException(status_code=500, detail='Failed to clear existing patients')

    # push the uploaded data automatically to the API Gateway
    sent = 0
    for p in data.get('patients', []):
        try:
            resp = requests.post(f'{GATEWAY_URL}/ingest', json=p, timeout=5)
            resp.raise_for_status()
            sent += 1
        except Exception as e:
            print("Failed to send patient:", p.get('id'), str(e))
        time.sleep(0.1)

    return {'status': 'uploaded', 'patients_sent': sent}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
