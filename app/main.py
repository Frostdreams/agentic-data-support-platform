from datetime import datetime, timezone
from uuid import uuid4,UUID

from fastapi import FastAPI,HTTPException, status
from app.models import Incident, IncidentCreate, IncidentStatus,LineageResult
from app.lineage import lineage_by_snowflake_object

app = FastAPI()

incidents_by_id: dict[UUID,Incident] = {}

@app.get("/health")
def health_check():
    return {
            "status": "healthy"
           }

@app.post("/incidents", status_code=status.HTTP_201_CREATED)
def create_incident(incident: IncidentCreate) -> Incident:
    new_incident = Incident(
        **incident.model_dump(),
        incident_id=uuid4(),
        status=IncidentStatus.NEW,
        created_at=datetime.now(timezone.utc),
    )
    incidents_by_id[new_incident.incident_id] = new_incident
    return new_incident

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: UUID) -> Incident:
    if incident_id not in incidents_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Incident not found"
        )
    return incidents_by_id[incident_id]

@app.get("/lineage/{snowflake_object}")
def get_lineage(snowflake_object: str) -> LineageResult:
    normalized_snowflake_object = snowflake_object.upper()
    if normalized_snowflake_object not in lineage_by_snowflake_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lineage not found"
        )
    return lineage_by_snowflake_object[normalized_snowflake_object]