from enum import Enum
from uuid import UUID
from pydantic import AwareDatetime, BaseModel, EmailStr

class IncidentCreate(BaseModel):
    ticket_name: str  # short human readable title of the incident
    description: str  # what is the problem, what is the expected vs actual behavior
    reporter_email: EmailStr  # email of the BI team member that sent this ticket

    report_name: str  # what report/dashboard is displaying the discrepancy
    snowflake_object: str  # what is the snowflake table or view that feeds data into the report
    affected_fields: list[str]  # what field(s) are showing the data discrepancy in the table
    symptom: str  # category of discrepancy, such as incorrect, missing,stale, or duplicated
    timeframe_start: AwareDatetime  # beginning of affected period
    timeframe_end: AwareDatetime # end of affected period
    message_id: str | None = None # optional representative message or correlation ID

class IncidentStatus(str, Enum):
    NEW = "new"
    DIAGNOSING = "diagnosing"
    AWAITING_APPROVAL = "awaiting_approval"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class SystemType(str, Enum):
    KAFKA = "kafka"
    EKS = "eks"
    MONGODB = "mongodb"
    S3 = "s3"
    AIRFLOW = "airflow"
    SNOWFLAKE = "snowflake"
    AWS_BATCH = "aws_batch"
    AWS_LAMBDA = "aws_lambda"

# represents stage in pipeline
class LineageStage(BaseModel):
    system_type: SystemType  # see SystemType class 
    resource_id: str  # actual topic, bucket path, collection etc
    description: str  

class PipelineLineage(BaseModel):
    pipeline_id: str 
    stages: list[LineageStage]

class LineageResult(BaseModel):
    snowflake_object: str 
    pipelines: list[PipelineLineage]

class Incident(IncidentCreate):
    incident_id: UUID
    status: IncidentStatus
    created_at: AwareDatetime