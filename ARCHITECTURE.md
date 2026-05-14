# FlowBrief AI Architecture

FlowBrief AI uses a two-call AI pipeline to classify banking
documents, extract structured operational fields, and generate
staff-ready handoff reports.

Call 1 uses gpt-4o-mini: optimised for speed
and cost-efficient structured JSON extraction.
Call 2 uses gpt-4o: optimised for reasoning
quality and coherent report generation.
This tiered approach reflects a deliberate
architectural decision to match model capability
to task complexity, balancing cost and output
quality across the two inference steps.

The backend integrates with the OpenAI API through the openai SDK.
