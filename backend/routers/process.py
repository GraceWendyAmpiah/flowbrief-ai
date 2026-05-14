import uuid
import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from models.case_model import CaseResponse
from services import ai_service as gemini_service
from services import dynamo_service
from services import s3_service


router = APIRouter()


@router.post("/api/process", response_model=CaseResponse)
async def process_document(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    if text is not None and file is not None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Provide either text or file, not both",
                "code": "INVALID_INPUT",
            },
        )
    if text is None and file is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Provide either text or file",
                "code": "INVALID_INPUT",
            },
        )
    if text is not None and len(text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Text input must be at least 20 characters",
                "code": "INVALID_INPUT",
            },
        )

    if file is not None:
        file_bytes = await file.read()

        try:
            s3_service.validate_file(
                file.filename,
                file.content_type,
                len(file_bytes),
            )
        except ValueError as e:
            error_msg = str(e)
            if "FILE_TOO_LARGE" in error_msg:
                raise HTTPException(
                    status_code=413,
                    detail={
                        "error": error_msg,
                        "code": "FILE_TOO_LARGE",
                    },
                )
            raise HTTPException(
                status_code=400,
                detail={
                    "error": error_msg,
                    "code": "INVALID_FILE_TYPE",
                },
            )

        case_id = str(uuid.uuid4())

        try:
            s3_key = s3_service.upload_file(
                case_id,
                file.filename,
                file_bytes,
                file.content_type,
            )
        except RuntimeError as e:
            return JSONResponse(
                status_code=500,
                content={"error": str(e), "code": "S3_ERROR"},
            )

        try:
            retrieved_bytes = s3_service.get_file_bytes(s3_key)
        except RuntimeError as e:
            return JSONResponse(
                status_code=500,
                content={"error": str(e), "code": "S3_ERROR"},
            )

        raw_text = retrieved_bytes.decode("utf-8", errors="replace")

    if text is not None:
        case_id = str(uuid.uuid4())
        raw_text = text.strip()

    try:
        extracted = gemini_service.extract_fields(raw_text)
    except RuntimeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "GEMINI_ERROR"},
        )

    try:
        handoff_report = gemini_service.generate_report(
            extracted,
            raw_text,
        )
    except RuntimeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "GEMINI_ERROR"},
        )

    created_at = datetime.now(timezone.utc).isoformat()
    case_dict = {
        "case_id": case_id,
        "created_at": created_at,
        "raw_input": raw_text,
        "classification": extracted["classification"],
        "urgency": extracted["urgency"],
        "confidence_score": extracted["confidence_score"],
        "customer_name": extracted.get("customer_name"),
        "request_type": extracted["request_type"],
        "business_type": extracted.get("business_type"),
        "amount_mentioned": extracted.get("amount_mentioned"),
        "missing_documents": extracted.get("missing_documents", []),
        "risk_flags": extracted.get("risk_flags", []),
        "recommended_team": extracted["recommended_team"],
        "handoff_report": handoff_report,
    }

    try:
        dynamo_service.save_case(case_dict)
    except RuntimeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "DATABASE_ERROR"},
        )

    return CaseResponse(**case_dict)
