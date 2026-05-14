from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional
from models.case_model import CaseResponse, CaseListResponse
from services import dynamo_service


router = APIRouter()


@router.get("/api/cases", response_model=CaseListResponse)
async def list_cases(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    urgency: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
):
    try:
        result = dynamo_service.list_cases(
            search=search,
            category=category,
            urgency=urgency,
            page=page,
            limit=limit,
        )
        return CaseListResponse(**result)
    except RuntimeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "DATABASE_ERROR"},
        )


@router.get("/api/cases/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str):
    try:
        case = dynamo_service.get_case(case_id)
    except RuntimeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "DATABASE_ERROR"},
        )

    if case is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Case not found", "code": "NOT_FOUND"},
        )

    return CaseResponse(**case)
