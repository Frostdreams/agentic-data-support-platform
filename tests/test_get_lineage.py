from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
expected_stages = [("kafka","na-orders"),("eks","mobile-orders-consumer"),("mongodb","orders.mobile_orders"),("aws_batch","mobile-orders-export"),("s3","s3://analytics-landing/mobile-orders/"),("airflow","mobile-orders-to-snowflake"),("snowflake","MOBILE_ORDERS")]

def test_get_lineage():
    get_response = client.get("/lineage/MOBILE_ORDERS")
    assert get_response.status_code == 200

    lineage = get_response.json()
    assert lineage["snowflake_object"] == "MOBILE_ORDERS"
    assert lineage["pipelines"][0]["pipeline_id"] == "mobile-orders-pipeline"

    for actual_stage, expected_stage in zip(lineage["pipelines"][0]["stages"], expected_stages, strict=True):
        assert actual_stage["system_type"] == expected_stage[0]
        assert actual_stage["resource_id"] == expected_stage[1] 

def test_get_lowercase_lineage():
    get_response = client.get("/lineage/mobile_orders")
    assert get_response.status_code == 200

    lineage = get_response.json()
    assert lineage["snowflake_object"] == "MOBILE_ORDERS"

def test_get_lineage_not_found():
    get_response = client.get("/lineage/UNKNOWN_TABLE")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Lineage not found"