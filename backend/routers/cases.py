from fastapi import APIRouter

router = APIRouter()


@router.get("/api/cases")
async def list_cases():
    return {"status": "stub — not implemented"}


@router.get("/api/cases/{case_id}")
async def get_case(case_id: str):
    return {"status": "stub — not implemented"}