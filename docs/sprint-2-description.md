# Sprint 2 Description

Sprint 2 improved the existing MVP without rebuilding the project or replacing
the original planning pipeline. The goal was to make the assistant more robust,
more transparent and easier to present in a live demo.

## 1. Better German and English Input Handling

In Sprint 1, weak words from natural input could appear as focus areas, for
example `Moechte`. Sprint 2 improved text preprocessing and keyword detection.

Implemented improvements:

- German and English stopword filtering
- normalization of German umlauts to ASCII-friendly forms
- filtering of weak intent words such as `ich`, `moechte`, `gerne`, `ueber`,
  `want`, `would`, `like` and `about`
- cleaner focus-area labels such as `Agentic AI`, `Security`, `Tool Usage`,
  `Evaluation`, `Prototype` and `Research Design`

Result: the topic analysis is cleaner and more useful for students.

## 2. Explicit Research Question Validation

Sprint 2 added a structured validation step for every generated research
question. Each question is checked by:

- clarity
- testability
- scope
- feasibility
- improvement suggestion

This validation is part of the structured project plan and is displayed in the
Streamlit app as a table. It helps users understand whether a question is
realistic, measurable and focused enough for a student project.

## 3. Structured Generation Error Handling

Sprint 2 introduced the local planning scaffold and the first SAIA integration.
The final-delivery contract is now stricter: the scaffold defines the complete
`ProjectPlan` structure, while Academic Cloud / SAIA generates the final
content.

Handled error cases:

- missing `ACADEMIC_CLOUD_API_KEY`
- unreachable API
- invalid JSON response
- response data that does not validate as `ProjectPlan`

The final app shows a clear error in these cases and does not return or save the
local scaffold as if it were a complete final plan. Existing saved plans and
local history operations remain available. Pydantic validates the technical
structure of the response; it does not verify the scientific correctness of the
plan.

## 4. Improved Streamlit UI

Sprint 2 reorganized the Streamlit interface to make the generated plan easier
to understand during a presentation.

Implemented UI improvements:

- cleaner input column
- memory moved into a collapsed section
- generated output split into tabs
- overview tab for topic analysis and focus areas
- research question cards with RQ badges
- question validation shown as a table
- methodology tab for method, evaluation and risks
- export tab for Markdown, JSON and PDF downloads
- status badges for generated, saved and export-ready plans

The UI keeps the existing modern card style but improves spacing, readability
and structure.

## 5. Tests and Quality Checks

Sprint 2 added a small pytest suite for the most important behavior:

- weak German stopwords are removed from topic analysis
- research questions are generated
- question validation returns the expected fields
- memory save/load works with JSON fallback
- Markdown and JSON export files are created
- final LLM generation raises a clear configuration error without an API key

The project also uses `ruff` and `compileall` as lightweight quality checks.

## 6. Repository Cleanup

The project structure was cleaned for GitHub submission:

- generated output folders are ignored
- local `.env` files are ignored
- virtual environments are ignored
- Python cache files are ignored
- the old duplicate Sprint-1 source snapshot was removed
- Sprint-1 preparation notes were kept under `docs/`

## Final-Delivery Architecture Update

```text
User Input
→ Local Planning Scaffold
→ Structured SAIA Request
→ LLM JSON Response
→ Pydantic Validation
→ ProjectPlan
→ UI, Memory and Export
```

The configured model is `qwen3-30b-a3b-instruct-2507`.
