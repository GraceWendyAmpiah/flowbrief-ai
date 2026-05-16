# FlowBrief AI — Ethical AI Note

## Purpose of This Document

This document describes the intended use, known
limitations, and ethical boundaries of FlowBrief AI.
It is intended for reviewers, evaluators, and any
organisation considering deploying or adapting this
system.

---

## What This System Does

FlowBrief AI is a document intelligence assistant
designed to support internal banking operations staff.
It accepts customer request documents, extracts
structured information using a large language model,
classifies the request type, identifies potentially
missing documents, and generates a staff handoff report
to assist with routing and processing.

---

## What This System Does Not Do

FlowBrief AI does not and is not designed to:

- Approve or reject loan applications
- Make credit decisions of any kind
- Verify the authenticity of submitted documents
- Guarantee the accuracy of extracted information
- Replace compliance officer review or sign-off
- Act as a regulatory authority
- Process or store real customer data in any
  production banking environment
- Authenticate users or enforce access controls

---

## AI Output Is Advisory Only

Every extraction, classification, and handoff report
produced by this system is an AI-generated suggestion.
All output must be reviewed and verified by a qualified
human staff member before any banking action is taken.
The confidence score visible on each case report is a
self-assessed estimate from the AI model and does not
constitute a reliability guarantee.

The system is explicitly designed to assist human
workflows, not to replace human judgment at any point
in the process.

---

## Data Handling

This system was built as a technical demonstration.
It does not connect to any live banking infrastructure
or process real customer data. All sample documents
used during development and testing are fictitious.

In any production deployment, operators would be
responsible for ensuring compliance with applicable
data protection regulations including the Ghana Data
Protection Act and any relevant financial services
regulations.

---

## Model Transparency

The AI inference layer uses open-source Llama models
served through the Groq API:

- Extraction: llama-3.1-8b-instant
- Report generation: llama-3.3-70b-versatile

These are general-purpose language models not
specifically trained on banking data. Their outputs
reflect patterns from general training data and may
not align with specific regulatory requirements,
internal policy, or jurisdictional norms without
additional fine-tuning or guardrails.

---

## Known Limitations

- The system may misclassify ambiguous requests
- Extracted fields may be incomplete or incorrect
  when documents are poorly structured
- The system has no memory across sessions
- Missing document detection is based on language
  patterns, not a definitive compliance checklist
- The handoff report may contain factual errors
  if the source document is unclear or incomplete

---

## Intended Use Statement

FlowBrief AI is intended as a productivity tool for
trained banking operations staff in a supervised
environment. It is not suitable for unsupervised
deployment, public-facing customer interactions,
or any context where AI-generated output would be
acted upon without human review.