from uuid import UUID, uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def valid_incident_data():
    return {
        "ticket_name": "Incorrect mobile order IDs",
        "description": "The dashboard is missing order IDs.",
        "reporter_email": "analyst@example.com",
        "report_name": "Mobile Orders Dashboard",
        "snowflake_object": "MOBILE_ORDERS",
        "affected_fields": ["order_id"],
        "symptom": "missing",
        "timeframe_start": "2026-08-15T14:00:00Z",
        "timeframe_end": "2026-08-15T15:00:00Z",
        "message_id": "msg-84721",
    }

def test_create_incident():
    incident_data = valid_incident_data()

    response = client.post("/incidents",json=incident_data)
    response_data = response.json()

    assert response.status_code == 201

    for field,value in incident_data.items():
        assert response_data[field] == value

    assert UUID(response_data["incident_id"])
    assert response_data["status"] == "new"
    assert response_data["created_at"]

def test_create_incident_missing_fields():
    incident_data = valid_incident_data()
    del incident_data["report_name"]

    response = client.post("/incidents",json=incident_data)

    assert response.status_code == 422

def test_create_incident_rejects_invalid_email():
    incident_data = valid_incident_data()
    incident_data["reporter_email"] = "not-an-email"

    response = client.post("/incidents", json=incident_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == [
        "body",
        "reporter_email",
    ]

def test_create_incident_rejects_datetime_without_timezone():
    incident_data = valid_incident_data()
    incident_data["timeframe_start"] = "2026-08-15T14:00:00"

    response = client.post("/incidents", json=incident_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == [
        "body",
        "timeframe_start",
    ]

def test_get_incident():
    incident_data = valid_incident_data()
    post_response = client.post("/incidents",json=incident_data)
    assert post_response.status_code == 201
    post_response_data = post_response.json()
    incident_id = post_response_data["incident_id"]

    get_response = client.get("/incidents/" + incident_id)
    assert get_response.status_code == 200
    assert get_response.json() == post_response_data

# case where UUID is valid but entry does not exist
def test_get_incident_not_found():
    incident_id = uuid4()
    get_response = client.get("/incidents/" + str(incident_id))
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Incident not found"

# case where UUID is invalid
def test_get_incident_rejects_invalid_uuid():
    incident_id = "abcdefghijk"
    get_response = client.get("/incidents/" + incident_id)
    assert get_response.status_code == 422
    assert get_response.json()["detail"][0]["loc"] == [
        "path",
        "incident_id",
    ]