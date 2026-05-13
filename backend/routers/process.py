from fastapi import APIRouter

router = APIRouter()


@router.post("/api/process")
async def process_document():
    return {"status": "stub — not implemented"}