from fastapi import FastAPI
from app.models import IncidentCreate

app = FastAPI()

@app.get("/health")
def health_check():
    return {
            "status": "healthy"
           }

@app.post("/incidents")
def create_incident(incident: IncidentCreate) -> IncidentCreate:
    return incident