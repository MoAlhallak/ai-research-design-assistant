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
- Suggests suitable methodology types with required steps, artifacts and limitations
- Builds concrete evaluation criteria with measurement and expected evidence
- Creates a structured risk matrix with probability, impact and mitigation
- Saves, searches, loads and compares previous plans in local memory
- Shows saved project conversations in a searchable left history sidebar
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

The left `Plan History` sidebar works like a lightweight chat history. Every
saved project idea and its generated response can be reopened. `New Plan` clears
the current workspace without deleting saved plans.

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
    |-- test_sprint_2.py
    `-- test_sprint_3.py
```

## Documentation

- [Project structure](docs/project-structure.md)
- [Sprint 1 preparation](docs/sprint-1-preparation.md)
- [Sprint 2 description](docs/sprint-2-description.md)
- [Sprint 3 description](docs/sprint-3-description.md)

## Important Boundary

This system is a planning aid. It does not replace academic supervision,
scientific judgment, course requirements or the student's own verification of
the generated research plan.
