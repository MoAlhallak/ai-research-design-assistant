# AI Research Design Assistant

AI Research Design Assistant is a student-facing prototype that turns a rough
research idea into a structured research plan. The focus is research planning,
not paper search.

The assistant can run fully offline with templates and local rules. If an
Academic Cloud / SAIA API key is configured in the local environment, generated
plans can also be refined internally with an LLM while keeping a robust local
fallback.

## Final Prototype Features

This is a finished prototype, not a temporary demo. The key capabilities are:

- One-click generation of a structured research plan from a rough idea
- An assistant-style **Plan History** sidebar with search
- **Rename** and **delete** for saved plans/chats, persisted locally
- A **Demo Example** to show the full flow instantly
- Methodology Advisor, Evaluation Builder and Risk Matrix planning views
- Quality Check for research questions with transparent reasons
- Markdown, JSON and PDF export
- Local run and Docker run

## Features

- Generates a focused research topic from a broad idea
- Detects useful focus areas in German and English input
- Creates concrete research questions with rationale and measurable outcomes
- Validates research questions for clarity, testability, scope and feasibility
- Suggests suitable methodology types with required steps, artifacts and limitations
- Builds concrete evaluation criteria with measurement and expected evidence
- Creates a structured risk matrix with probability, impact and mitigation
- Saves, searches, loads and compares previous plans in local memory
- Shows saved project conversations in a searchable left history sidebar
- Renames and deletes saved plans directly from the history sidebar
- Supports ChromaDB-based prototype memory with JSON fallback
- Exports generated plans as Markdown, JSON and PDF, including methodology,
  evaluation, risk and memory-comparison sections
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

## Docker Run

The app also runs in Docker with Docker Compose:

```powershell
docker compose build
docker compose up
```

Then open `http://localhost:8501`. Saved plans, memory and exports are stored in
the mounted `outputs/` folder, so they persist across container restarts. The
app runs fully offline by default; set `ACADEMIC_CLOUD_API_KEY` in your
environment (or an `.env` file) to enable optional LLM refinement.

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

The Memory tab shows recent saved plans, supports keyword search, can load an
older plan and can compare the current plan with a previous one. The comparison
highlights shared focus areas, changed focus areas, methodology similarity,
changed research questions and a short recommendation.

## Plan History

The left `Plan History` sidebar works like a lightweight chat history. A "chat"
is one saved project idea together with its generated research plan. Every entry
has a readable title and can be reopened with a single click to restore the full
plan. `New Plan` starts a clean, empty input without deleting saved plans, and
the search box filters saved plans by keyword. Newly generated plans appear in
the history immediately, and an empty-state message is shown when no plans exist
yet.

## Rename and Delete Plans

Each saved plan can be renamed or deleted directly in the Plan History sidebar:

- Click the rename icon next to a plan, enter a new title and save it. The new
  title appears immediately and the plan content is left unchanged.
- Click the delete icon and confirm to remove a single plan. Deleting one plan
  never affects the others, and if the deleted plan is currently open the main
  area resets to a new empty plan.

Both actions update the local memory files, so renames and deletions persist
after the app is restarted.

## Methodology and Evaluation Planning

The assistant includes three planning components that make the generated plan
more useful for research design:

- `Methodology Advisor`: suggests suitable method types such as Literature
  Review, Prototype, Experiment, Comparison, Case Study and Evaluation
  Checklist. Each suggestion explains why it fits, which steps are required,
  which data or artifacts are needed and which limitations should be considered.
- `Evaluation Builder`: creates measurable evaluation criteria such as
  functional correctness, usability, security, performance, completeness,
  reproducibility and quality of the generated research plan.
- `Risk Matrix`: structures risks by probability, impact and mitigation
  strategy instead of showing only a simple risk list.

## Validation Logic

Research-question validation is local, rule-based and transparent. It does not
depend on an external AI service. For every question, the assistant checks:

- whether the wording is specific and understandable
- whether a measurable outcome or comparison is available
- whether the scope is narrow enough for one research project
- whether the required work is realistic for a student project

Each rating includes a short reason and an improvement suggestion. The UI shows
the compact ratings in a table and the explanations in expandable sections.
The same reasons are included in Markdown, JSON and PDF exports.

## Worked Example

Example input:

```text
I want to work on Agentic AI Security and Tool Usage.
```

The local planning pipeline detects `Agentic AI`, `Security` and `Tool Usage`
as focus areas. It generates three research questions about a security-aware
planning agent, suitable methodology and evaluation criteria, and project risks.
The Methodology Advisor recommends a prototype-oriented approach. The Evaluation
Builder creates criteria for plan quality, functional correctness,
reproducibility, security, usability and completeness. The Risk Matrix covers
generic recommendations, project scope, evaluation evidence, threat modeling and
prototype bias. A detailed walkthrough is available in the
[Sprint 3 description](docs/sprint-3-description.md#worked-example).

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

## Demo Day Checklist

A short manual checklist for verifying the app before a live demo, covering
startup, the core flow, Plan History, rename/delete, exports and quality checks,
is available in [docs/demo-day-checklist.md](docs/demo-day-checklist.md).

## Project Structure

```text
.
|-- .env.example
|-- .gitignore
|-- app.py
|-- CONTRIBUTING.md
|-- Dockerfile
|-- docker-compose.yml
|-- docs/
|   |-- demo-day-checklist.md
|   |-- project-structure.md
|   |-- sprint-1-preparation.md
|   |-- sprint-2-description.md
|   `-- sprint-3-description.md
|-- LICENSE
|-- pyproject.toml
|-- README.md
|-- src/ai_research_design_assistant/
|   |-- __init__.py
|   |-- agent.py
|   |-- cli.py
|   |-- evaluation.py
|   |-- exporters.py
|   |-- llm.py
|   |-- methodology_advisor.py
|   |-- memory.py
|   |-- models.py
|   |-- planning.py
|   |-- risks.py
|   |-- templates.py
|   |-- text.py
|   `-- validation.py
`-- tests/
    |-- test_memory.py
    |-- test_sprint_2.py
    `-- test_sprint_3.py
```

## Documentation

- [Demo Day checklist](docs/demo-day-checklist.md)
- [Project structure](docs/project-structure.md)
- [Sprint 1 preparation](docs/sprint-1-preparation.md)
- [Sprint 2 description](docs/sprint-2-description.md)
- [Sprint 3 description](docs/sprint-3-description.md)

## Important Boundary

This system is a planning aid. It does not replace academic supervision,
scientific judgment, course requirements or the student's own verification of
the generated research plan.
