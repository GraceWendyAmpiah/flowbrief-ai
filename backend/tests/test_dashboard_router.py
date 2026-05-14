import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch


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

sample_stats = {
    "total_cases": 10,
    "by_category": {
        "KYC": 2,
        "Complaint": 3,
        "SME Advisory": 2,
        "Trade Finance": 2,
        "Account Opening": 1,
    },
    "high_priority_count": 3,
    "average_confidence": 78,
    "missing_document_count": 5,
}


def test_get_dashboard_returns_200_with_stats():
    with patch(
        "routers.dashboard.dynamo_service.get_dashboard_stats",
        return_value=sample_stats,
    ):
        response = client.get("/api/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert "total_cases" in payload
    assert "by_category" in payload
    assert "high_priority_count" in payload
    assert "average_confidence" in payload
    assert "missing_document_count" in payload
    assert payload["total_cases"] == 10
    assert set(payload["by_category"]) == {
        "KYC",
        "Complaint",
        "SME Advisory",
        "Trade Finance",
        "Account Opening",
    }


def test_get_dashboard_returns_500_on_error():
    with patch(
        "routers.dashboard.dynamo_service.get_dashboard_stats",
        side_effect=RuntimeError("DATABASE_ERROR: scan failed"),
    ):
        response = client.get("/api/dashboard")

    assert response.status_code == 500
    assert response.json()["code"] == "DATABASE_ERROR"
