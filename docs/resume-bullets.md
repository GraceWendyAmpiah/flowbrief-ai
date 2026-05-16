# FlowBrief AI — Resume Bullets

## Project Summary

**FlowBrief AI** — Banking Workflow Intelligence Assistant
Full-stack AI application built as a technical demonstration
for a Société Générale Ghana IT Developer application.

Live deployment:
- Frontend: https://main.d382k6j2vboqjr.amplifyapp.com
- Backend: https://flowbrief-ai-production.up.railway.app
- Repository: https://github.com/GraceWendyAmpiah/flowbrief-ai

---

## Resume Bullets

- Architected and deployed a full-stack banking document
  intelligence system using Python FastAPI, React, AWS
  DynamoDB, AWS S3, and AWS Amplify, with the backend
  containerised via Docker and hosted on Railway

- Designed a two-tier AI inference pipeline using
  open-source Llama models served through the Groq API:
  llama-3.1-8b-instant for structured JSON field extraction
  and llama-3.3-70b-versatile for natural language report
  generation, with model selection justified by task
  complexity and cost-quality trade-offs

- Implemented an automated document classification system
  that processes unstructured banking request documents,
  extracts ten structured fields, routes cases across five
  categories (KYC, Complaint, SME Advisory, Trade Finance,
  Account Opening), and generates formatted staff handoff
  reports with urgency scoring and escalation logic

- Defined and enforced a strict REST API contract between
  a FastAPI backend and a React frontend, maintaining
  complete directory isolation between two AI coding agents
  throughout a constrained 16-hour build window with zero
  cross-boundary contamination

- Built an operational dashboard in React using Recharts
  displaying live aggregated metrics from DynamoDB including
  case volume, category distribution, average AI confidence
  score, and high-priority case counts

- Diagnosed and resolved a DynamoDB composite key schema
  mismatch in production by migrating from get_item to a
  partition-key query, and fixed browser-side CORS failures
  on unhandled 500 responses by implementing a FastAPI
  global exception handler

- Configured end-to-end cloud deployment across Railway
  and AWS Amplify including environment variable management,
  CORS policy enforcement, React Router redirect rules, and
  automated redeploy on GitHub push

- Managed two provider migrations during the build — from
  Google Gemini to OpenAI to Groq — maintaining architectural
  integrity and full test suite coverage throughout,
  documenting each decision in Architecture Decision Records