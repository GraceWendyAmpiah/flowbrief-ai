import os
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError


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

from services import dynamo_service


def make_case(
    case_id: str = "some-uuid",
    created_at: str = "2026-05-13T21:00:00Z",
    raw_input: str = "Customer requested account opening support",
    classification: str = "Account Opening",
    urgency: str = "Medium",
    confidence_score: int = 90,
    missing_documents: list[str] | None = None,
) -> dict:
    return {
        "case_id": case_id,
        "created_at": created_at,
        "raw_input": raw_input,
        "classification": classification,
        "urgency": urgency,
        "confidence_score": confidence_score,
        "customer_name": "Avery Stone",
        "request_type": "Support",
        "business_type": "Retail",
        "amount_mentioned": None,
        "missing_documents": missing_documents or [],
        "risk_flags": [],
        "recommended_team": "Operations",
        "handoff_report": "Internal handoff details",
    }


@pytest.fixture
def mock_table(monkeypatch):
    table = Mock()
    monkeypatch.setattr(dynamo_service, "table", table)
    return table


def test_save_case_writes_correct_item(mock_table):
    sample_case = make_case()
    mock_table.put_item.return_value = {}

    result = dynamo_service.save_case(sample_case)

    assert result is None
    mock_table.put_item.assert_called_once_with(Item=sample_case)


def test_get_case_returns_item_when_found(mock_table):
    sample_case = make_case()
    mock_table.query.return_value = {"Items": [sample_case]}

    result = dynamo_service.get_case("some-uuid")

    assert result == sample_case
    mock_table.query.assert_called_once()


def test_get_case_returns_none_when_not_found(mock_table):
    mock_table.query.return_value = {"Items": []}

    result = dynamo_service.get_case("missing-uuid")

    assert result is None
    mock_table.query.assert_called_once()


def test_list_cases_filters_by_category(mock_table):
    cases = [
        make_case("1", "2026-05-13T21:00:00Z", classification="KYC"),
        make_case("2", "2026-05-13T20:00:00Z", classification="Complaint"),
        make_case("3", "2026-05-13T19:00:00Z", classification="KYC"),
    ]
    mock_table.scan.return_value = {"Items": cases}

    result = dynamo_service.list_cases(
        search=None,
        category="KYC",
        urgency=None,
        page=1,
        limit=20,
    )

    assert [item["classification"] for item in result["cases"]] == ["KYC", "KYC"]
    assert all("handoff_report" not in item for item in result["cases"])


def test_list_cases_filters_by_search_term(mock_table):
    cases = [
        make_case(
            "1",
            created_at="2026-05-13T20:00:00Z",
            raw_input="Customer needs a working capital loan",
        ),
        make_case(
            "2",
            created_at="2026-05-13T19:00:00Z",
            raw_input="Customer submitted KYC documents",
        ),
        make_case(
            "3",
            created_at="2026-05-13T21:00:00Z",
            raw_input="Loan repayment question",
        ),
    ]
    mock_table.scan.return_value = {"Items": cases}

    result = dynamo_service.list_cases(
        search="loan",
        category=None,
        urgency=None,
        page=1,
        limit=20,
    )

    assert [item["case_id"] for item in result["cases"]] == ["3", "1"]


def test_list_cases_paginates_correctly(mock_table):
    cases = [
        make_case(
            str(index),
            created_at=f"2026-05-13T{index:02d}:00:00Z",
        )
        for index in range(25)
    ]
    mock_table.scan.return_value = {"Items": cases}

    result = dynamo_service.list_cases(
        search=None,
        category=None,
        urgency=None,
        page=2,
        limit=10,
    )

    assert len(result["cases"]) == 10
    assert result["total"] == 25
    assert result["page"] == 2
    assert result["limit"] == 10


def test_get_dashboard_stats_returns_correct_counts(mock_table):
    cases = [
        make_case(
            "1",
            classification="KYC",
            urgency="High",
            confidence_score=80,
            missing_documents=["passport", "utility bill"],
        ),
        make_case(
            "2",
            classification="Complaint",
            urgency="Low",
            confidence_score=90,
            missing_documents=[],
        ),
        make_case(
            "3",
            classification="Trade Finance",
            urgency="High",
            confidence_score=100,
            missing_documents=["invoice"],
        ),
    ]
    mock_table.scan.return_value = {"Items": cases}

    result = dynamo_service.get_dashboard_stats()

    assert result == {
        "total_cases": 3,
        "by_category": {
            "KYC": 1,
            "Complaint": 1,
            "SME Advisory": 0,
            "Trade Finance": 1,
            "Account Opening": 0,
        },
        "high_priority_count": 2,
        "average_confidence": 90,
        "missing_document_count": 3,
    }


def test_database_error_raised_on_client_error(mock_table):
    mock_table.put_item.side_effect = ClientError(
        {
            "Error": {
                "Code": "ValidationException",
                "Message": "Invalid item",
            }
        },
        "PutItem",
    )

    with pytest.raises(RuntimeError, match=r"^DATABASE_ERROR"):
        dynamo_service.save_case(make_case())
