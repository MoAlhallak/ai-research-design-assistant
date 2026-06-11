# AI Research Design Assistant

AI Research Design Assistant is a student-facing prototype that turns a rough
research idea into a structured research plan. The focus is research planning,
not paper search.

The assistant can run fully offline with templates and local rules. If an
Academic Cloud / SAIA API key is configured in the local environment, the plan
can also be refined internally with an LLM while keeping a robust local
fallback.

## Features

- Generates a focused research topic from a broad idea
- Detects useful focus areas in German and English input
- Normalizes German umlauts to ASCII-friendly forms such as `ae`, `oe`, `ue`
  and `ss`
- Filters weak filler words such as `ich`, `moechte`, `gerne`, `ueber`, `want`,
  `would`, `like` and `about`
- Creates concrete research questions with rationale and measurable outcomes
- Validates each research question for clarity, testability, scope and feasibility
- Suggests methodology, evaluation criteria, risks and countermeasures
- Saves previous plans in local memory
- Supports ChromaDB-based prototype memory with JSON fallback
- Exports generated plans as Markdown, JSON and PDF
- Provides both a Streamlit UI and a CLI
- Includes a small pytest suite for Sprint 2 functionality

## Tech Stack

- `Python` for the application logic
- `Streamlit` for the web interface
- `LangChain` for the planning workflow orchestration
- `Pydantic` for structured output models
- `ChromaDB` for local prototype memory
- `Typer` and `Rich` for the command-line interface
- `pytest` and `ruff` for testing and code quality
- `httpx` for Academic Cloud / SAIA API calls

## Quick Start

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

Start the Streamlit app:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the app in your browser:

```text
http://localhost:8501
```

## CLI Usage

```powershell
.\.venv\Scripts\python.exe -m ai_research_design_assistant.cli plan "I want to work on Agentic AI Security and Tool Usage."
```

The CLI exports the generated plan to the configured output folder.

## LLM Configuration

The assistant works without an API key. Without an API key it uses:

- local templates
- rule-based topic analysis
- local planning logic
- local memory
- export functions

To enable LLM refinement, create a local `.env` file based on `.env.example`:

```text
ACADEMIC_CLOUD_API_KEY=your_api_key_here
ACADEMIC_CLOUD_BASE_URL=https://chat-ai.academiccloud.de/v1
ACADEMIC_CLOUD_MODEL=qwen3.5-122b-a10b
```

The API key is never hardcoded. The `.env` file is ignored by Git and must not be
uploaded to GitHub.

If the API key is missing, the API is unreachable, or the LLM returns invalid or
incomplete JSON, the app falls back to the local template-based plan.

## Memory

Generated plans are stored locally under:

```text
outputs/project-memory/
outputs/chroma-memory/
```

These folders are generated at runtime and are ignored by Git. ChromaDB memory is
currently a prototype using deterministic local hash embeddings. It can be
improved later with stronger semantic embedding models.

## Tests and Quality Checks

Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run linting:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Run a compile check:

```powershell
.\.venv\Scripts\python.exe -m compileall src app.py
```

## Project Structure

```text
.
|-- .env.example
|-- .gitignore
|-- app.py
|-- CONTRIBUTING.md
|-- docs/
|   |-- project-structure.md
|   `-- sprint-1-preparation.md
|-- LICENSE
|-- pyproject.toml
|-- README.md
|-- src/ai_research_design_assistant/
|   |-- __init__.py
|   |-- agent.py
|   |-- cli.py
|   |-- exporters.py
|   |-- llm.py
|   |-- memory.py
|   |-- models.py
|   |-- planning.py
|   |-- templates.py
|   |-- text.py
|   `-- validation.py
`-- tests/
    `-- test_sprint_2.py
```

## Sprint 2 Description

Sprint 2 improved the existing MVP without rebuilding the project or replacing
the original planning pipeline. The goal was to make the assistant more robust,
more transparent and easier to present in a live demo.

### 1. Better German and English input handling

In Sprint 1, some weak words from natural input could appear as focus areas, for
example `Moechte`. Sprint 2 improved the text preprocessing and keyword
detection.

Implemented improvements:

- German and English stopword filtering
- normalization of German umlauts to ASCII-friendly forms
- filtering of weak intent words such as `ich`, `moechte`, `gerne`, `ueber`,
  `want`, `would`, `like` and `about`
- cleaner focus-area labels such as `Agentic AI`, `Security`, `Tool Usage`,
  `Evaluation`, `Prototype` and `Research Design`

Result: the topic analysis is cleaner and more useful for students.

### 2. Explicit research question validation

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

### 3. More robust fallback behavior

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

### 4. Improved Streamlit UI

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

### 5. Tests and quality checks

Sprint 2 added a small pytest suite for the most important behavior:

- weak German stopwords are removed from topic analysis
- research questions are generated
- question validation returns the expected fields
- memory save/load works with JSON fallback
- Markdown and JSON export files are created
- fallback behavior does not crash without an API key

The project also uses `ruff` and `compileall` as lightweight quality checks.

### 6. Repository cleanup

The project structure was cleaned for GitHub submission:

- generated output folders are ignored
- local `.env` files are ignored
- virtual environments are ignored
- Python cache files are ignored
- the old duplicate Sprint-1 source snapshot was removed
- Sprint-1 preparation notes were kept under `docs/`

## Important Boundary

This system is a planning aid. It does not replace academic supervision,
scientific judgment, course requirements or the student's own verification of
the generated research plan.
