# FlowBrief AI — Architecture

FlowBrief AI is a two-tier AI document intelligence
system deployed on AWS and Railway. The frontend and
backend are completely isolated and communicate
exclusively via a defined REST API contract.

---

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│         React + Vite · AWS Amplify                  │
│                                                     │
│  Upload Page · Report View · Dashboard · History    │
└───────────────────────┬─────────────────────────────┘
                        │ HTTPS REST API
                        │ (API Contract)
┌───────────────────────▼─────────────────────────────┐
│                    BACKEND                          │
│         Python FastAPI · Railway                    │
│                                                     │
│  POST /api/process                                  │
│  GET  /api/cases                                    │
│  GET  /api/cases/{case_id}                          │
│  GET  /api/dashboard                                │
└───┬───────────────┬───────────────┬─────────────────┘
    │               │               │
    ▼               ▼               ▼
┌───────┐    ┌──────────┐    ┌──────────┐
│ Groq  │    │ DynamoDB │    │    S3    │
│  API  │    │  AWS     │    │  AWS     │
└───────┘    └──────────┘    └──────────┘
```

---

### Two-Tier AI Strategy

Every document processed makes two sequential
AI calls to the Groq API. The model selection
reflects a deliberate architectural decision
to match model capability to task complexity.

**Call 1 — Extraction and Classification**
Model: llama-3.1-8b-instant
Purpose: Fast, structured JSON extraction.
A lightweight 8B parameter model is used here
because the task is schema-constrained and
deterministic. Speed and cost efficiency
matter more than reasoning depth at this stage.
Returns: customer name, request type, urgency,
classification, missing documents, risk flags,
confidence score, recommended team.

**Call 2 — Handoff Report Generation**
Model: llama-3.3-70b-versatile
Purpose: Coherent operational report writing.
A large 70B parameter model is used here because
the output is a narrative document read by human
staff. Reasoning quality and language coherence
directly affect operational usefulness.
Returns: a markdown-formatted staff handoff report
with summary, classification, required next steps,
missing information, source excerpts, and
escalation note where applicable.

---

### API Contract

The API contract is the single boundary between
the frontend and backend. Neither agent modified
it without explicit approval during the build.

All requests use HTTPS. All responses are JSON.
Authentication is not implemented in the MVP.

| Endpoint | Method | Purpose |
|---|---|---|
| /api/process | POST | Process a document, run AI pipeline, save case |
| /api/cases | GET | List cases with search and filter |
| /api/cases/{case_id} | GET | Retrieve a single full case |
| /api/dashboard | GET | Aggregated operational statistics |

---

### Data Flow

1. Staff submits document text or file via the
   Upload page
2. Frontend sends multipart/form-data to
   POST /api/process on the backend
3. If a file, backend uploads to S3 before
   processing
4. Backend calls Groq Call 1 with the document
   text to extract structured fields
5. Backend calls Groq Call 2 with the extracted
   fields to generate the handoff report
6. Backend saves the full case to DynamoDB
7. Backend returns the complete case object
   to the frontend
8. Frontend navigates to the Report View page
   and renders the case

---

### Infrastructure

| Component | Service | Notes |
|---|---|---|
| Frontend | AWS Amplify | Auto-deploys from GitHub main branch |
| Backend | Railway | Docker container, auto-deploys from GitHub |
| Database | AWS DynamoDB | On-demand capacity, us-east-1 |
| File Storage | AWS S3 | Private bucket, temporary file staging |
| AI Inference | Groq API | OpenAI-compatible SDK via base_url override |

---

### Key Design Decisions

**Frontend and backend isolation**
The two agents building this system (Claude Code
for frontend, Codex for backend) were given strict
directory boundaries. No shared code, no shared
deployment pipeline. The API contract was defined
upfront and treated as immutable during the build.

**Scan-based DynamoDB queries**
For MVP scope, list and dashboard operations use
full table scans with Python-level filtering. This
is intentional — the access patterns were not
finalised during the build window. Query-based
access with GSIs is the appropriate next step
for a production system.

**OpenAI SDK for Groq**
The openai Python package is used as the HTTP
client for the Groq API via a base_url override.
This requires no additional dependency and keeps
the SDK surface familiar. The GEMINI_ERROR error
code retained internally reflects the provider
migration history documented in ADR-001.

---

## Provider History

The system was originally designed for Google
Gemini. During integration testing, the free tier
quota was exhausted. The provider was migrated to
Groq. Full decision record: reports/ADR-001.md
