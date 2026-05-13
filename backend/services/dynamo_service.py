import boto3
import botocore.exceptions

from config.settings import settings


dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)
table = dynamodb.Table(settings.dynamodb_table_name)


def _database_error(error: botocore.exceptions.ClientError) -> RuntimeError:
    return RuntimeError(f"DATABASE_ERROR: {error}")


def save_case(case_data: dict) -> None:
    try:
        table.put_item(Item=case_data)
    except botocore.exceptions.ClientError as error:
        raise _database_error(error) from error


def get_case(case_id: str) -> dict | None:
    try:
        response = table.get_item(Key={"case_id": case_id})
    except botocore.exceptions.ClientError as error:
        raise _database_error(error) from error

    return response.get("Item")


def list_cases(
    search: str | None = None,
    category: str | None = None,
    urgency: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> dict:
    page = max(page, 1)
    limit = min(max(limit, 1), 50)

    try:
        response = table.scan()
    except botocore.exceptions.ClientError as error:
        raise _database_error(error) from error

    filtered = response.get("Items", [])

    if search is not None:
        normalized_search = search.lower()
        filtered = [
            item
            for item in filtered
            if normalized_search in item["raw_input"].lower()
        ]

    if category is not None:
        filtered = [
            item
            for item in filtered
            if item["classification"] == category
        ]

    if urgency is not None:
        filtered = [
            item
            for item in filtered
            if item["urgency"] == urgency
        ]

    filtered = sorted(
        filtered,
        key=lambda item: item["created_at"],
        reverse=True,
    )

    offset = (page - 1) * limit
    page_items = [
        {key: value for key, value in item.items() if key != "handoff_report"}
        for item in filtered[offset : offset + limit]
    ]

    return {
        "cases": page_items,
        "total": len(filtered),
        "page": page,
        "limit": limit,
    }


def get_dashboard_stats() -> dict:
    try:
        response = table.scan()
    except botocore.exceptions.ClientError as error:
        raise _database_error(error) from error

    items = response.get("Items", [])
    total_cases = len(items)
    by_category = {
        "KYC": 0,
        "Complaint": 0,
        "SME Advisory": 0,
        "Trade Finance": 0,
        "Account Opening": 0,
    }

    for item in items:
        classification = item["classification"]
        if classification in by_category:
            by_category[classification] += 1

    high_priority_count = sum(1 for item in items if item["urgency"] == "High")
    average_confidence = (
        round(sum(item["confidence_score"] for item in items) / total_cases)
        if total_cases
        else 0
    )
    missing_document_count = sum(
        len(item["missing_documents"])
        for item in items
    )

    return {
        "total_cases": total_cases,
        "by_category": by_category,
        "high_priority_count": high_priority_count,
        "average_confidence": average_confidence,
        "missing_document_count": missing_document_count,
    }
