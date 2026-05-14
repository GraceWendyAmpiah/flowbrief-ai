import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")
os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test-access-key")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-secret-key")
os.environ.setdefault("DYNAMODB_TABLE_NAME", "test-cases")
os.environ.setdefault("S3_BUCKET_NAME", "test-bucket")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000")

from services import ai_service as gemini_service


@pytest.fixture
def valid_extraction():
    return {
        "customer_name": "Akosua Mensah",
        "request_type": "SME loan application",
        "business_type": "SME",
        "amount_mentioned": "GHS 50000",
        "urgency": "Medium",
        "missing_documents": ["audited financials"],
        "risk_flags": [],
        "recommended_team": "SME Advisory",
        "confidence_score": 85,
        "classification": "SME Advisory",
    }


def response_with_text(text: str):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = text
    return mock_response


def test_extract_fields_returns_valid_dict_on_success(monkeypatch, valid_extraction):
    generate_content = Mock(return_value=response_with_text(json.dumps(valid_extraction)))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    result = gemini_service.extract_fields("Customer requests an SME loan")

    assert result == valid_extraction


def test_extract_fields_retries_once_on_first_json_parse_failure(
    monkeypatch, valid_extraction
):
    generate_content = Mock(
        side_effect=[
            response_with_text("not json"),
            response_with_text(json.dumps(valid_extraction)),
        ]
    )
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    result = gemini_service.extract_fields("Customer requests an SME loan")

    assert generate_content.call_count == 2
    assert result == valid_extraction


def test_extract_fields_raises_gemini_error_after_two_json_parse_failures(monkeypatch):
    generate_content = Mock(return_value=response_with_text("not json"))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    with pytest.raises(RuntimeError) as exc_info:
        gemini_service.extract_fields("Customer requests an SME loan")

    assert "GEMINI_ERROR" in str(exc_info.value)
    assert generate_content.call_count == 2


def test_extract_fields_raises_gemini_error_on_invalid_classification(
    monkeypatch, valid_extraction
):
    invalid_response = {**valid_extraction, "classification": "InvalidCategory"}
    generate_content = Mock(return_value=response_with_text(json.dumps(invalid_response)))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    with pytest.raises(RuntimeError) as exc_info:
        gemini_service.extract_fields("Customer requests an SME loan")

    assert "GEMINI_ERROR" in str(exc_info.value)


def test_extract_fields_raises_gemini_error_on_invalid_urgency(
    monkeypatch, valid_extraction
):
    invalid_response = {**valid_extraction, "urgency": "Critical"}
    generate_content = Mock(return_value=response_with_text(json.dumps(invalid_response)))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    with pytest.raises(RuntimeError) as exc_info:
        gemini_service.extract_fields("Customer requests an SME loan")

    assert "GEMINI_ERROR" in str(exc_info.value)


def test_extract_fields_accepts_all_five_valid_classification_values(
    monkeypatch, valid_extraction
):
    classifications = [
        "KYC",
        "Complaint",
        "SME Advisory",
        "Trade Finance",
        "Account Opening",
    ]

    for classification in classifications:
        valid_response = {**valid_extraction, "classification": classification}
        generate_content = Mock(return_value=response_with_text(json.dumps(valid_response)))
        monkeypatch.setattr(
            gemini_service.openai_client.chat.completions,
            "create",
            generate_content,
        )

        result = gemini_service.extract_fields("Customer requests banking support")

        assert result["classification"] == classification


def test_extract_fields_accepts_all_three_valid_urgency_values(
    monkeypatch, valid_extraction
):
    for urgency in ["Low", "Medium", "High"]:
        valid_response = {**valid_extraction, "urgency": urgency}
        generate_content = Mock(return_value=response_with_text(json.dumps(valid_response)))
        monkeypatch.setattr(
            gemini_service.openai_client.chat.completions,
            "create",
            generate_content,
        )

        result = gemini_service.extract_fields("Customer requests banking support")

        assert result["urgency"] == urgency


@pytest.fixture
def valid_extracted():
    return {
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


def test_generate_report_returns_markdown_string(monkeypatch, valid_extracted):
    markdown_response = "## Summary\nAkosua Mensah requests SME loan support."
    generate_content = Mock(return_value=response_with_text(markdown_response))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    result = gemini_service.generate_report(
        valid_extracted,
        "Akosua Mensah requests an SME loan.",
    )

    assert result == markdown_response
    generate_content.assert_called_once()


def test_generate_report_raises_gemini_error_on_empty_response(
    monkeypatch, valid_extracted
):
    generate_content = Mock(return_value=response_with_text(""))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    with pytest.raises(RuntimeError) as exc_info:
        gemini_service.generate_report(
            valid_extracted,
            "Akosua Mensah requests an SME loan.",
        )

    assert "GEMINI_ERROR" in str(exc_info.value)


def test_generate_report_raises_gemini_error_on_whitespace_only_response(
    monkeypatch, valid_extracted
):
    generate_content = Mock(return_value=response_with_text("   "))
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    with pytest.raises(RuntimeError) as exc_info:
        gemini_service.generate_report(
            valid_extracted,
            "Akosua Mensah requests an SME loan.",
        )

    assert "GEMINI_ERROR" in str(exc_info.value)


def test_generate_report_does_not_call_extract_fields_or_extraction_model(
    monkeypatch, valid_extracted
):
    extract_fields = Mock()
    generate_content = Mock(
        return_value=response_with_text("## Summary\nPrepared report.")
    )
    monkeypatch.setattr(gemini_service, "extract_fields", extract_fields)
    monkeypatch.setattr(
        gemini_service.openai_client.chat.completions,
        "create",
        generate_content,
    )

    gemini_service.generate_report(
        valid_extracted,
        "Akosua Mensah requests an SME loan.",
    )

    extract_fields.assert_not_called()
    generate_content.assert_called_once()
