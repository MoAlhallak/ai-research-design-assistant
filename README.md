# AI Research Design Assistant

AI Research Design Assistant is a student-facing planning tool that turns a
rough research idea into a structured research plan. It focuses on research
design—not paper search—and combines a deterministic local planning scaffold
with structured generation through Academic Cloud / SAIA.

## Final Project Delivery

| Item | Delivery |
|---|---|
| Project Website | [GitHub Pages project website](https://moalhallak.github.io/ai-research-design-assistant/) — activate Pages after the final push |
| Code Repository | [github.com/MoAlhallak/ai-research-design-assistant](https://github.com/MoAlhallak/ai-research-design-assistant) |
| Docker Image | `ghcr.io/moalhallak/ai-research-design-assistant:latest` |
| Pitch Deck | Not included in this repository; add the final PDF when available |
| Product Video | Public video URL still required |
| Local setup | [Local setup](#local-setup) |
| Docker setup | [Docker Compose](#docker-compose) |

The project website is the portfolio and documentation page. The Streamlit
application itself runs locally or in Docker at `http://localhost:8501`.

## How Final Plan Generation Works

The local Python pipeline analyzes the idea and creates the initial
`ProjectPlan` scaffold. The application then sends that complete structure to
Academic Cloud / SAIA using the model
`qwen3-30b-a3b-instruct-2507`. The model must return JSON with the required keys
and nesting, and Pydantic validates that response as a `ProjectPlan`.

```text
User Input
→ Local Planning Scaffold
→ Structured SAIA Request
→ LLM JSON Response
→ Pydantic Validation
→ ProjectPlan
→ UI, Memory and Export
```

An `ACADEMIC_CLOUD_API_KEY` is required to generate a final plan. If the API is
unavailable or its response is invalid, the app shows a clear error and does
not return or save the incomplete local scaffold. Existing saved plans, Plan
History, search, rename and delete continue to work locally.

Pydantic validates the technical shape and data types of the returned plan. It
does not establish that the scientific claims, method choice or conclusions are
correct.

## Main Features

- One-click final plan generation from a rough project idea
- Focused topic analysis in German and English
- Research questions with rationale and measurable outcomes
- Transparent local validation for clarity, testability, scope and feasibility
- Methodology Advisor with steps, required artifacts and limitations
- Evaluation Builder with measurements, evidence and priorities
- Risk Matrix with probability, impact and mitigation
- Searchable local Plan History with load, compare, rename and delete
- Markdown, JSON and PDF export
- Streamlit interface and a developer CLI for the local planning scaffold
- Docker Compose and published container-image support
- Automated tests, linting and compile checks

## Worked Example

Example input:

```text
I want to work on Agentic AI Security and Tool Usage.
```

The local scaffold detects `Agentic AI`, `Security` and `Tool Usage`, creates
the required `ProjectPlan` structure, and supplies methodology, evaluation and
risk context. SAIA then rewrites the scaffold into the final, idea-specific JSON
plan. The returned structure is validated before the UI displays or saves it.
A detailed walkthrough is available in the
[Sprint 3 description](docs/sprint-3-description.md#worked-example).

## Architecture and Responsibilities

- `planning.py` creates the deterministic local planning scaffold.
- `llm.py` sends the structured request to Academic Cloud / SAIA and parses the
  JSON response.
- `models.py` defines the Pydantic schema used for response validation.
- `app.py` coordinates generation, errors, UI state, memory and downloads.
- `memory.py` manages local JSON/ChromaDB prototype history operations.
- `exporters.py` creates Markdown, JSON and PDF representations.

Research-question validation is local and rule-based. It explains why each
question is rated for clarity, testability, scope and feasibility, but remains
planning guidance rather than scientific peer review.

## Local Setup

Create the local configuration file:

```powershell
Copy-Item .env.example .env
```

Open `.env` locally and replace `your_api_key_here` with the real Academic Cloud
API key. Never commit `.env`.

Create the environment, install the project and start Streamlit:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Docker Compose

Create the local configuration file and add the real key locally:

```powershell
Copy-Item .env.example .env
```

Build and start:

```powershell
docker compose up --build
```

Open:

```text
http://localhost:8501
```

The Compose configuration requires `ACADEMIC_CLOUD_API_KEY` and mounts
`./outputs` at `/app/outputs` so local plan history and exports survive container
restarts.

## Published Docker Image

Published image:

```text
ghcr.io/moalhallak/ai-research-design-assistant:latest
```

After creating a local `.env` with the real key, run the image without exposing
the key on the command line:

```powershell
docker run --rm -p 8501:8501 --env-file .env ghcr.io/moalhallak/ai-research-design-assistant:latest
```

The Compose setup is recommended when persistent `outputs/` storage is needed.

## Configuration

`.env.example` documents the supported values:

```text
ACADEMIC_CLOUD_API_KEY=your_api_key_here
ACADEMIC_CLOUD_BASE_URL=https://chat-ai.academiccloud.de/v1
ACADEMIC_CLOUD_MODEL=qwen3-30b-a3b-instruct-2507
ACADEMIC_CLOUD_TIMEOUT=180
```

The real key belongs only in the ignored local `.env` file or in the runtime
environment.

## Developer Scaffold CLI

The CLI exposes the deterministic local scaffold for development and testing:

```powershell
.\.venv\Scripts\python.exe -m ai_research_design_assistant.cli plan "I want to work on Agentic AI Security and Tool Usage."
```

This command is useful for inspecting local planning logic. It does not replace
the SAIA step required by the Streamlit workflow for a final plan.

## Plan History and Exports

Runtime data is stored under ignored `outputs/` directories. The Plan History
sidebar can search and reopen existing plans, start a new empty session, rename
a plan, or delete one plan without affecting the rest.

Validated plans can be downloaded as Markdown, JSON and PDF. Validation reasons,
methodology advice, evaluation criteria and the Risk Matrix are included in the
exports.

## Tests and Quality Checks

```powershell
python -m ruff check .
python -m compileall src app.py
python -m pytest
```

Docker configuration and the Streamlit health endpoint should also be checked
before a release. See the [Demo Day checklist](docs/demo-day-checklist.md).

## Final Moodle ZIP

Create the clean local submission archive with:

```powershell
python scripts/create_final_zip.py
```

The command creates
`release/AI_Research_Design_Assistant_Final.zip`. The `release/` directory is
ignored by Git. The archive excludes Git history, secrets, environments,
runtime outputs, caches, generated exports and IDE metadata.

## Project Structure

```text
.
|-- .env.example
|-- app.py
|-- docker-compose.yml
|-- Dockerfile
|-- docs/
|   |-- assets/
|   |-- index.html
|   |-- styles.css
|   `-- sprint documentation
|-- scripts/
|   `-- create_final_zip.py
|-- src/ai_research_design_assistant/
|-- tests/
|-- CONTRIBUTING.md
|-- LICENSE
|-- pyproject.toml
`-- README.md
```

## Documentation

- [Project website source](docs/index.html)
- [Demo Day checklist](docs/demo-day-checklist.md)
- [Project structure](docs/project-structure.md)
- [Sprint 1 preparation](docs/sprint-1-preparation.md)
- [Sprint 2 description](docs/sprint-2-description.md)
- [Sprint 3 description](docs/sprint-3-description.md)

## Important Limitations

- Final plan generation depends on Academic Cloud / SAIA availability and a
  valid API key.
- LLM output can still contain weak, biased or incorrect research advice even
  when its JSON structure is valid.
- Local validation checks technical and planning heuristics; it is not a
  scientific-quality guarantee.
- Local history is designed for a single local user and is not an authenticated
  multi-user data store.
- The system does not replace academic supervision, course requirements,
  literature review, ethics review or the student's own verification.
