import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test-access-key")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-secret-key")
os.environ.setdefault("DYNAMODB_TABLE_NAME", "test-cases")
os.environ.setdefault("S3_BUCKET_NAME", "test-bucket")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000")

from main import app


client = TestClient(app)

sample_case = {
    "case_id": "some-uuid",
    "created_at": "2026-05-13T21:00:00Z",
    "raw_input": "Customer requested loan support",
    "classification": "KYC",
    "urgency": "High",
    "confidence_score": 88,
    "customer_name": "Avery Stone",
    "request_type": "Loan application",
    "business_type": "SME",
    "amount_mentioned": "GHS 50000",
    "missing_documents": ["proof of address"],
    "risk_flags": ["missing KYC"],
    "recommended_team": "KYC Team",
    "handoff_report": "Internal handoff details",
}

sample_summary = {
    key: value
    for key, value in sample_case.items()
    if key != "handoff_report"
}


def test_get_cases_returns_200_with_case_list():
    with patch(
        "routers.cases.dynamo_service.list_cases",
        return_value={
            "cases": [sample_summary],
            "total": 1,
            "page": 1,
            "limit": 20,
        },
    ):
        response = client.get("/api/cases")

    assert response.status_code == 200
    payload = response.json()
    assert "cases" in payload
    assert "total" in payload
    assert "page" in payload
    assert "limit" in payload
    assert len(payload["cases"]) == 1


def test_get_cases_passes_query_params_correctly():
    list_cases_mock = MagicMock(
        return_value={"cases": [], "total": 0, "page": 1, "limit": 20}
    )

    with patch("routers.cases.dynamo_service.list_cases", list_cases_mock):
        response = client.get(
            "/api/cases?search=loan&category=KYC&urgency=High"
        )

    assert response.status_code == 200
    list_cases_mock.assert_called_once_with(
        search="loan",
        category="KYC",
        urgency="High",
        page=1,
        limit=20,
    )


def test_get_cases_returns_500_on_database_error():
    with patch(
        "routers.cases.dynamo_service.list_cases",
        side_effect=RuntimeError("DATABASE_ERROR: scan failed"),
    ):
        response = client.get("/api/cases")

    assert response.status_code == 500
    assert response.json()["code"] == "DATABASE_ERROR"


def test_get_case_returns_200():
    with patch(
        "routers.cases.dynamo_service.get_case",
        return_value=sample_case,
    ):
        response = client.get("/api/cases/some-uuid")

    assert response.status_code == 200
    assert "handoff_report" in response.json()


def test_get_case_returns_404():
    with patch(
        "routers.cases.dynamo_service.get_case",
        return_value=None,
    ):
        response = client.get("/api/cases/missing-uuid")

    assert response.status_code == 404
    assert response.json()["code"] == "NOT_FOUND"


def test_get_case_returns_500():
    with patch(
        "routers.cases.dynamo_service.get_case",
        side_effect=RuntimeError("DATABASE_ERROR: read failed"),
    ):
        response = client.get("/api/cases/some-uuid")

    assert response.status_code == 500
    assert response.json()["code"] == "DATABASE_ERROR"
