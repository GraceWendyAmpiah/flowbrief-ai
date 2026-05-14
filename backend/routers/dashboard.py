from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.case_model import DashboardResponse
from services import dynamo_service


router = APIRouter()


@router.get("/api/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    try:
        stats = dynamo_service.get_dashboard_stats()
        return DashboardResponse(**stats)
    except RuntimeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "DATABASE_ERROR"},
        )
