FROM python:3.11-slim
WORKDIR /app
COPY app.py sample_patients.json ./
RUN pip install --no-cache-dir fastapi uvicorn python-multipart requests
EXPOSE 5000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
