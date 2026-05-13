from pydantic import BaseModel
from typing import Optional


class CaseResponse(BaseModel):
    case_id: str
    created_at: str
    raw_input: str
    classification: str
    urgency: str
    confidence_score: int
    customer_name: Optional[str]
    request_type: str
    business_type: Optional[str]
    amount_mentioned: Optional[str]
    missing_documents: list[str]
    risk_flags: list[str]
    recommended_team: str
    handoff_report: str


class CaseSummary(BaseModel):
    case_id: str
    created_at: str
    raw_input: str
    classification: str
    urgency: str
    confidence_score: int
    customer_name: Optional[str]
    request_type: str
    business_type: Optional[str]
    amount_mentioned: Optional[str]
    missing_documents: list[str]
    risk_flags: list[str]
    recommended_team: str


class CaseListResponse(BaseModel):
    cases: list[CaseSummary]
    total: int
    page: int
    limit: int


class DashboardResponse(BaseModel):
    total_cases: int
    by_category: dict[str, int]
    high_priority_count: int
    average_confidence: int
    missing_document_count: int