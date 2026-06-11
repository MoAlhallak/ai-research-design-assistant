# AI Research Design Assistant

AI Research Design Assistant is a student-facing prototype that turns a rough
research idea into a structured research plan. The focus is research planning,
not paper search.

The assistant can run fully offline with templates and local rules. If an
Academic Cloud / SAIA API key is configured in the local environment, generated
plans can also be refined internally with an LLM while keeping a robust local
fallback.

## Features

- Generates a focused research topic from a broad idea
- Detects useful focus areas in German and English input
- Creates concrete research questions with rationale and measurable outcomes
- Validates research questions for clarity, testability, scope and feasibility
- Suggests methodology, evaluation criteria, risks and countermeasures
- Saves previous plans in local memory
- Supports ChromaDB-based prototype memory with JSON fallback
- Exports generated plans as Markdown, JSON and PDF
- Provides both a Streamlit UI and a CLI
- Includes tests and lightweight quality checks

## Tech Stack

- `Python` for the application logic
- `Streamlit` for the web interface
- `LangChain` for workflow orchestration
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

## Configuration

The assistant works without an API key. Without an API key it uses local
templates, rule-based topic analysis, local memory and export functions.

To enable LLM refinement, create a local `.env` file based on `.env.example`:

```text
ACADEMIC_CLOUD_API_KEY=your_api_key_here
ACADEMIC_CLOUD_BASE_URL=https://chat-ai.academiccloud.de/v1
ACADEMIC_CLOUD_MODEL=qwen3.5-122b-a10b
```

The API key is never hardcoded. The `.env` file is ignored by Git and must not be
uploaded to GitHub.

## Memory and Exports

Generated plans and memory files are stored locally under:

```text
outputs/project-memory/
outputs/chroma-memory/
outputs/student-project-plan/
```

These folders are generated at runtime and are ignored by Git.

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
|   |-- sprint-1-preparation.md
|   `-- sprint-2-description.md
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

## Documentation

- [Project structure](docs/project-structure.md)
- [Sprint 1 preparation](docs/sprint-1-preparation.md)
- [Sprint 2 description](docs/sprint-2-description.md)

## Important Boundary

This system is a planning aid. It does not replace academic supervision,
scientific judgment, course requirements or the student's own verification of
the generated research plan.
