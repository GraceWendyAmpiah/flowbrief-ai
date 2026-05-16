from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app


client = TestClient(app)

valid_extracted_dict = {
    "classification": "SME Advisory",
    "customer_name": "Akosua Mensah",
    "request_type": "SME loan application",
    "business_type": "SME",
    "amount_mentioned": "GHS 50000",
    "urgency": "Medium",
    "missing_documents": ["audited financials"],
    "risk_flags": [],
    "recommended_team": "SME Advisory Team",
    "confidence_score": 85,
}

MOCK_REPORT = "## Summary\nA valid handoff report for internal routing."


def _response_code(response):
    payload = response.json()
    return payload.get("code", payload.get("detail", {}).get("code"))


def test_text_input_returns_200_with_full_case_object():
    with (
        patch(
            "routers.process.gemini_service.extract_fields",
            return_value=valid_extracted_dict,
        ),
        patch(
            "routers.process.gemini_service.generate_report",
            return_value=MOCK_REPORT,
        ),
        patch("routers.process.dynamo_service.save_case", return_value=None),
    ):
        response = client.post(
            "/api/process",
            data={"text": "This is a valid text input with enough chars"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert "case_id" in payload
    assert "created_at" in payload
    assert "classification" in payload
    assert "urgency" in payload
    assert "handoff_report" in payload
    assert payload["classification"] == "SME Advisory"


def test_both_text_and_file_returns_400():
    response = client.post(
        "/api/process",
        data={"text": "This is a valid text input with enough chars"},
        files={"file": ("document.pdf", b"file bytes", "application/pdf")},
    )

    assert response.status_code == 400
    assert _response_code(response) == "INVALID_INPUT"


def test_neither_text_nor_file_returns_400():
    response = client.post("/api/process")

    assert response.status_code == 400
    assert _response_code(response) == "INVALID_INPUT"


def test_text_under_20_characters_returns_400():
    response = client.post(
        "/api/process",
        data={"text": "short"},
    )

    assert response.status_code == 400
    assert _response_code(response) == "INVALID_INPUT"


def test_invalid_file_mime_type_returns_400():
    response = client.post(
        "/api/process",
        files={"file": ("notes.txt", b"plain text", "text/html")},
    )

    assert response.status_code == 400
    assert _response_code(response) == "INVALID_FILE_TYPE"


def test_oversized_file_returns_413():
    with patch(
        "routers.process.s3_service.validate_file",
        side_effect=ValueError("FILE_TOO_LARGE: maximum file size is 10MB"),
    ):
        response = client.post(
            "/api/process",
            files={"file": ("document.pdf", b"file bytes", "application/pdf")},
        )

    assert response.status_code == 413
    assert _response_code(response) == "FILE_TOO_LARGE"


def test_gemini_error_on_extract_fields_returns_500():
    with patch(
        "routers.process.gemini_service.extract_fields",
        side_effect=RuntimeError("GEMINI_ERROR: parse failed"),
    ):
        response = client.post(
            "/api/process",
            data={"text": "This is a valid text input with enough chars"},
        )

    assert response.status_code == 500
    assert response.json()["code"] == "GEMINI_ERROR"


def test_gemini_error_on_generate_report_returns_500():
    with (
        patch(
            "routers.process.gemini_service.extract_fields",
            return_value=valid_extracted_dict,
        ),
        patch(
            "routers.process.gemini_service.generate_report",
            side_effect=RuntimeError("GEMINI_ERROR: empty response"),
        ),
    ):
        response = client.post(
            "/api/process",
            data={"text": "This is a valid text input with enough chars"},
        )

    assert response.status_code == 500
    assert response.json()["code"] == "GEMINI_ERROR"


def test_database_error_on_save_case_returns_500():
    with (
        patch(
            "routers.process.gemini_service.extract_fields",
            return_value=valid_extracted_dict,
        ),
        patch(
            "routers.process.gemini_service.generate_report",
            return_value=MOCK_REPORT,
        ),
        patch(
            "routers.process.dynamo_service.save_case",
            side_effect=RuntimeError("DATABASE_ERROR: write failed"),
        ),
    ):
        response = client.post(
            "/api/process",
            data={"text": "This is a valid text input with enough chars"},
        )

    assert response.status_code == 500
    assert response.json()["code"] == "DATABASE_ERROR"


def test_successful_text_input_calls_services_in_correct_order():
    extract_fields_mock = MagicMock(return_value=valid_extracted_dict)
    generate_report_mock = MagicMock(return_value=MOCK_REPORT)
    save_case_mock = MagicMock(return_value=None)

    with (
        patch(
            "routers.process.gemini_service.extract_fields",
            extract_fields_mock,
        ),
        patch(
            "routers.process.gemini_service.generate_report",
            generate_report_mock,
        ),
        patch("routers.process.dynamo_service.save_case", save_case_mock),
    ):
        response = client.post(
            "/api/process",
            data={"text": "This is a valid text input with enough chars"},
        )

    assert response.status_code == 200
    extract_fields_mock.assert_called_once()
    generate_report_mock.assert_called_once()
    save_case_mock.assert_called_once()

    saved_case = save_case_mock.call_args.args[0]
    assert saved_case["classification"] == valid_extracted_dict["classification"]
    assert saved_case["urgency"] == valid_extracted_dict["urgency"]
