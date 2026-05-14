# FlowBrief AI Architecture

FlowBrief AI uses a two-call AI pipeline to classify banking
documents, extract structured operational fields, and generate
staff-ready handoff reports.

Call 1 uses llama-3.1-8b-instant via Groq:
a lightweight open-source model optimised for
speed and cost-efficient structured JSON
extraction.
Call 2 uses llama-3.3-70b-versatile via Groq:
a large open-source model optimised for
reasoning quality and coherent report generation.
This tiered approach reflects a deliberate
architectural decision to match model capability
to task complexity, using open-source Llama
models served through Groq's low-latency
inference API.

The backend integrates with the Groq API through the openai SDK via Groq base URL.
