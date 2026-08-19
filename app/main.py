from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, status
from app.models import Incident, IncidentCreate, IncidentStatus

app = FastAPI()

@app.get("/health")
def health_check():
    return {
            "status": "healthy"
           }

@app.post("/incidents", status_code=status.HTTP_201_CREATED)
def create_incident(incident: IncidentCreate) -> Incident:
    return Incident(
        **incident.model_dump(),
        incident_id=uuid4(),
        status=IncidentStatus.NEW,
        created_at=datetime.now(timezone.utc),
    )