import boto3
import botocore.exceptions

from config.settings import settings


ACCEPTED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "text/plain",
    "text/markdown",
}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def validate_file(filename, content_type, size_bytes) -> None:
    if content_type not in ACCEPTED_MIME_TYPES:
        raise ValueError(
            "INVALID_FILE_TYPE: accepted types are application/pdf, image/jpeg, image/png, text/plain, text/markdown"
        )

    if size_bytes > MAX_FILE_SIZE_BYTES:
        raise ValueError("FILE_TOO_LARGE: maximum file size is 10MB")

    return None


def upload_file(case_id, filename, file_bytes, content_type) -> str:
    key = f"uploads/{case_id}/{filename}"

    try:
        s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
            Body=file_bytes,
            ContentType=content_type,
        )
    except botocore.exceptions.ClientError as error:
        raise RuntimeError(f"S3_ERROR: {error}") from error

    return key


def get_file_bytes(s3_key) -> bytes:
    try:
        response = s3_client.get_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
        )
        return response["Body"].read()
    except botocore.exceptions.ClientError as error:
        raise RuntimeError(f"S3_ERROR: {error}") from error
