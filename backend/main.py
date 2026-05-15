from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from config.settings import settings
from routers import cases, dashboard, process


app = FastAPI(
    title="FlowBrief AI",
    description="Banking Workflow Intelligence Assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    allow_credentials=False,
)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request, exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "code": "INTERNAL_ERROR",
        },
    )


app.include_router(process.router)
app.include_router(cases.router)
app.include_router(dashboard.router)


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "FlowBrief AI"}
