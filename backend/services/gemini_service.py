import json

import google.generativeai as genai

from config.settings import settings


VALID_CLASSIFICATIONS = {
    "KYC",
    "Complaint",
    "SME Advisory",
    "Trade Finance",
    "Account Opening",
}
VALID_URGENCIES = {"Low", "Medium", "High"}


genai.configure(api_key=settings.gemini_api_key)

extraction_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={"temperature": 0},
)

report_model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config={"temperature": 1},
)


def generate_report(extracted: dict, raw_text: str) -> str:
    system_instruction = """You are a senior banking operations analyst preparing
an internal staff handoff report. Your reports are
factual, concise, and operationally useful. You do not
fabricate information. You do not make financial
decisions. You prepare routing and preparation summaries
for the appropriate internal team."""

    user_message = f"""Prepare a staff handoff report based on the following
extracted information from a customer document.

Classification: {extracted['classification']}
Customer Name: {extracted['customer_name']}
Request Type: {extracted['request_type']}
Business Type: {extracted['business_type']}
Amount Mentioned: {extracted['amount_mentioned']}
Urgency: {extracted['urgency']}
Missing Documents: {extracted['missing_documents']}
Risk Flags: {extracted['risk_flags']}
Recommended Team: {extracted['recommended_team']}
Confidence Score: {extracted['confidence_score']}

Original document excerpt:
{raw_text}

Generate the report in this exact markdown structure:

## Summary
[2-3 factual sentences describing the request]

## Classification
[Restate classification and recommended team]

## Required Next Steps
1. [First required action]
2. [Second required action]
[Continue as needed, minimum 2 steps]

## Missing Information
[List missing documents if any. Omit this entire
section if missing_documents is empty]

## Source Excerpts
> [Direct quote from document supporting classification]
> [Additional quote if relevant]

## Escalation Note
[Include only when urgency is High. Omit this entire
section otherwise. State clearly why escalation is
warranted and which team lead should be notified]"""

    response = report_model.generate_content([system_instruction, user_message])
    response_text = response.text.strip()

    if not response_text:
        raise RuntimeError(
            "GEMINI_ERROR: report generation returned an empty response"
        )

    return response_text


SYSTEM_INSTRUCTION = """You are a banking document analyst processing
internal customer and SME requests. Extract
structured information from the document provided.
Classify the request into exactly one category.
Return valid JSON only. No explanation. No markdown
formatting. No code fences. Raw JSON object only."""


def _generation_config():
    try:
        return genai.types.GenerationConfig(response_mime_type="application/json")
    except TypeError:
        return None


def extract_fields(raw_text: str) -> dict:
    generation_config = _generation_config()
    user_message = f"""Document content:
{raw_text}

Extract and return this exact JSON schema:
{{
  'customer_name': string or null,
  'request_type': string,
  'business_type': string or null,
  'amount_mentioned': string or null,
  'urgency': 'Low' or 'Medium' or 'High',
  'missing_documents': [array of strings],
  'risk_flags': [array of strings],
  'recommended_team': string,
  'confidence_score': integer between 0 and 100,
  'classification': one of exactly: KYC, Complaint,
    SME Advisory, Trade Finance, Account Opening
}}

Rules:
- urgency must be exactly one of: Low, Medium, High
- classification must be exactly one of the five
  categories listed, nothing else
- missing_documents must be an array, empty if none
- risk_flags must be an array, empty if none
- confidence_score reflects your confidence in the
  accuracy of this extraction based on document clarity
- Do not fabricate information not present in the document
- Return null for fields not present in the document"""

    try:
        if generation_config is not None:
            response = extraction_model.generate_content(
                [SYSTEM_INSTRUCTION, user_message],
                generation_config=generation_config,
            )
        else:
            response = extraction_model.generate_content([SYSTEM_INSTRUCTION, user_message])
        response_text = response.text.strip()
        parsed = json.loads(response_text)
    except Exception:
        try:
            if generation_config is not None:
                response = extraction_model.generate_content(
                    [SYSTEM_INSTRUCTION, user_message],
                    generation_config=generation_config,
                )
            else:
                response = extraction_model.generate_content(
                    [SYSTEM_INSTRUCTION, user_message]
                )
            response_text = response.text.strip()
            parsed = json.loads(response_text)
        except Exception as exc:
            raise RuntimeError(
                "GEMINI_ERROR: failed to parse JSON response after two attempts"
            ) from exc

    if parsed.get("classification") not in VALID_CLASSIFICATIONS:
        raise RuntimeError(
            f"GEMINI_ERROR: invalid classification value: {parsed.get('classification')}"
        )
    if parsed.get("urgency") not in VALID_URGENCIES:
        raise RuntimeError(
            f"GEMINI_ERROR: invalid urgency value: {parsed.get('urgency')}"
        )

    return parsed
