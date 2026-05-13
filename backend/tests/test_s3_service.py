from unittest.mock import MagicMock, patch

import botocore.exceptions
import pytest

from services import s3_service


def make_client_error():
    return botocore.exceptions.ClientError(
        error_response={
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied",
            }
        },
        operation_name="PutObject",
    )


def test_validate_file_passes_for_valid_pdf():
    s3_service.validate_file("brief.pdf", "application/pdf", 1024)


def test_validate_file_passes_for_valid_jpeg():
    s3_service.validate_file("photo.jpg", "image/jpeg", 1024)


def test_validate_file_passes_for_valid_png():
    s3_service.validate_file("image.png", "image/png", 1024)


def test_validate_file_rejects_invalid_mime_type():
    with pytest.raises(ValueError) as exc_info:
        s3_service.validate_file("notes.txt", "text/plain", 1024)

    assert "INVALID_FILE_TYPE" in str(exc_info.value)


def test_validate_file_rejects_oversized_file():
    with pytest.raises(ValueError) as exc_info:
        s3_service.validate_file("brief.pdf", "application/pdf", 10485761)

    assert "FILE_TOO_LARGE" in str(exc_info.value)


def test_validate_file_type_check_runs_before_size_check():
    with pytest.raises(ValueError) as exc_info:
        s3_service.validate_file("page.html", "text/html", 10485761)

    assert "INVALID_FILE_TYPE" in str(exc_info.value)
    assert "FILE_TOO_LARGE" not in str(exc_info.value)


def test_upload_file_returns_correct_s3_key():
    case_id = "case-123"
    filename = "brief.pdf"
    file_bytes = b"pdf-bytes"
    content_type = "application/pdf"
    expected_key = f"uploads/{case_id}/{filename}"
    mock_client = MagicMock()

    with patch.object(s3_service, "s3_client", mock_client):
        key = s3_service.upload_file(case_id, filename, file_bytes, content_type)

    assert key == expected_key
    mock_client.put_object.assert_called_once_with(
        Bucket=s3_service.settings.s3_bucket_name,
        Key=expected_key,
        Body=file_bytes,
        ContentType=content_type,
    )


def test_get_file_bytes_returns_correct_bytes():
    s3_key = "uploads/case-123/brief.pdf"
    expected_bytes = b"stored-bytes"
    mock_body = MagicMock()
    mock_body.read.return_value = expected_bytes
    mock_client = MagicMock()
    mock_client.get_object.return_value = {"Body": mock_body}

    with patch.object(s3_service, "s3_client", mock_client):
        file_bytes = s3_service.get_file_bytes(s3_key)

    assert file_bytes == expected_bytes
    mock_client.get_object.assert_called_once_with(
        Bucket=s3_service.settings.s3_bucket_name,
        Key=s3_key,
    )


def test_s3_error_raised_on_upload_client_error():
    mock_client = MagicMock()
    mock_client.put_object.side_effect = make_client_error()

    with patch.object(s3_service, "s3_client", mock_client):
        with pytest.raises(RuntimeError) as exc_info:
            s3_service.upload_file("case-123", "brief.pdf", b"bytes", "application/pdf")

    assert str(exc_info.value).startswith("S3_ERROR")


def test_s3_error_raised_on_get_client_error():
    mock_client = MagicMock()
    mock_client.get_object.side_effect = make_client_error()

    with patch.object(s3_service, "s3_client", mock_client):
        with pytest.raises(RuntimeError) as exc_info:
            s3_service.get_file_bytes("uploads/case-123/brief.pdf")

    assert str(exc_info.value).startswith("S3_ERROR")
