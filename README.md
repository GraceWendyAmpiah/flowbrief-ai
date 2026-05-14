# FlowBrief AI

**Banking Workflow Intelligence Assistant**

A lightweight document intelligence and workflow
routing assistant that helps internal banking staff
classify customer requests, extract structured
information, identify missing documents, and
generate staff handoff reports.

Built as a technical demonstration for a
Société Générale Ghana IT Developer application.

---

## What It Does

FlowBrief AI accepts a document upload or pasted
text, runs it through a two-tier AI pipeline, and
returns a structured case containing:

- Classified request type (KYC, Complaint, SME
  Advisory, Trade Finance, or Account Opening)
- Extracted fields: customer name, request type,
  urgency, missing documents, risk flags, and
  recommended team
- A formatted staff handoff report with summary,
  required next steps, and escalation notes for
  high-priority cases
- A confidence score for the extraction

All cases are saved and retrievable via a case
history view and an operational dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI — Extraction | Groq API (llama-3.1-8b-instant) |
| AI — Report Generation | Groq API (llama-3.3-70b-versatile) |
| Backend | Python, FastAPI, uvicorn |
| Database | AWS DynamoDB |
| File Storage | AWS S3 |
| Frontend | React, Vite, Tailwind CSS |
| Frontend Deployment | AWS Amplify |
| Backend Deployment | AWS App Runner |

---

## Architecture

The system uses a two-tier AI strategy:

**Call 1** uses llama-3.1-8b-instant via Groq —
a lightweight model optimised for fast, structured
JSON extraction at low cost.

**Call 2** uses llama-3.3-70b-versatile via Groq —
a large model optimised for reasoning quality and
coherent report generation.

Frontend and backend are completely isolated and
communicate exclusively via a defined REST API
contract. See ARCHITECTURE.md for the full
component diagram and design decisions.

---

## Running Locally

**Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your credentials in .env
uvicorn main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env
# Set VITE_API_URL to your backend URL
npm run dev
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| GROQ_API_KEY | Yes | Groq API key |
| AWS_REGION | Yes | AWS region |
| AWS_ACCESS_KEY_ID | Yes | AWS access key |
| AWS_SECRET_ACCESS_KEY | Yes | AWS secret key |
| DYNAMODB_TABLE_NAME | Yes | DynamoDB table name |
| S3_BUCKET_NAME | Yes | S3 bucket name |
| ALLOWED_ORIGINS | Yes | Comma-separated frontend URLs |

---

## Disclaimer

This project is a technical demonstration built
for a job application. It does not process real
customer data, does not connect to any live
banking system, and does not make financial
decisions. All AI output is advisory and intended
to assist human staff workflows, not replace
human judgment.

---

## Documentation

See the /docs directory for:
- deployment-guide.md — step-by-step AWS deployment
- ethical-ai-note.md — AI use and limitations
- resume-bullets.md — technical summary for
  application purposes

---
