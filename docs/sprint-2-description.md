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

## 3. More Robust Fallback Behavior

The local template-based planner remains the stable core of the application. If
LLM refinement is configured, the assistant can use it internally. If anything
goes wrong, the app continues with the local plan.

Handled fallback cases:

- missing API key
- unreachable API
- invalid JSON response
- incomplete response data

Result: the demo remains stable even without internet access or a working LLM
configuration.

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
- fallback behavior does not crash without an API key

The project also uses `ruff` and `compileall` as lightweight quality checks.

## 6. Repository Cleanup

The project structure was cleaned for GitHub submission:

- generated output folders are ignored
- local `.env` files are ignored
- virtual environments are ignored
- Python cache files are ignored
- the old duplicate Sprint-1 source snapshot was removed
- Sprint-1 preparation notes were kept under `docs/`
