# AI Research Design Assistant

AI Research Design Assistant is a student-facing application that turns a rough
research idea into a structured research plan. It combines a deterministic local
planning scaffold with structured generation through Academic Cloud / SAIA.

## Project Links

- [Project Website](https://moalhallak.github.io/ai-research-design-assistant/)
- [Pitch Deck](docs/assets/AI_Research_Design_Assistant_Demo_Day.pdf)
- Docker image: `ghcr.io/moalhallak/ai-research-design-assistant:latest`

## Main Features

- Generates a complete research plan from a rough project idea
- Narrows broad topics and detects focus areas in German and English
- Creates research questions with rationales and measurable outcomes
- Validates questions for clarity, testability, scope and feasibility
- Provides methodology recommendations with steps, artifacts and limitations
- Builds evaluation criteria with measurements, expected evidence and priorities
- Creates a Risk Matrix with probability, impact and mitigation strategies
- Maintains searchable local Plan History with load, compare, rename and delete
- Exports validated plans as Markdown, JSON and PDF
- Supports local installation, Docker Compose and a published container image

## How Final Plan Generation Works

The local Python pipeline analyzes the idea and creates the initial
`ProjectPlan` scaffold. The application sends that complete structure to
Academic Cloud / SAIA using the model
`qwen3-30b-a3b-instruct-2507`.

The model must return JSON with the required keys and nesting. Pydantic then
validates the response as a `ProjectPlan` before the application displays,
saves or exports it.

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
unavailable or its response is invalid, the application shows a clear error
instead of returning or saving the incomplete local scaffold. Existing saved
plans and local history operations continue to work without an API call.

Pydantic validates the technical structure and data types of the returned plan.
It does not establish that the scientific claims, methodology or conclusions
are correct.

## Worked Example

Example input:

```text
I want to work on Agentic AI Security and Tool Usage.
```

The local scaffold detects `Agentic AI`, `Security` and `Tool Usage`, creates
the required `ProjectPlan` structure, and supplies methodology, evaluation and
risk context. SAIA then develops the scaffold into the final, idea-specific JSON
plan. The response is validated before it becomes available in the interface,
Plan History or exports.

## Architecture and Responsibilities

- `planning.py` creates the deterministic local planning scaffold.
- `llm.py` sends the structured request to Academic Cloud / SAIA and parses the
  JSON response.
- `models.py` defines the Pydantic schema used for response validation.
- `app.py` coordinates generation, error handling, UI state, memory and
  downloads.
- `memory.py` manages local JSON and ChromaDB prototype history operations.
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

Create a virtual environment, install the project and start Streamlit:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the application:

```text
http://localhost:8501
```

## Streamlit Community Cloud

Use the following deployment settings in Streamlit Community Cloud:

- Repository: `MoAlhallak/ai-research-design-assistant`
- Branch: `main`
- Main file: `app.py`
- Recommended Python version: `3.11`

Runtime dependencies are installed from the root `requirements.txt`. Add
`ACADEMIC_CLOUD_API_KEY`, `ACADEMIC_CLOUD_BASE_URL`,
`ACADEMIC_CLOUD_MODEL` and `ACADEMIC_CLOUD_TIMEOUT` through
Streamlit Community Cloud Secrets. Never commit the real API key.

## Docker Compose

Create the local configuration file and add the real API key:

```powershell
Copy-Item .env.example .env
```

Build and start the application:

```powershell
docker compose up --build
```

Open:

```text
http://localhost:8501
```

The Compose configuration requires `ACADEMIC_CLOUD_API_KEY` and mounts
`./outputs` at `/app/outputs`, allowing Plan History and exports to persist
across container restarts.

Stop the application with:

```powershell
docker compose down
```

## Published Docker Image

Published image:

```text
ghcr.io/moalhallak/ai-research-design-assistant:latest
```

After creating a local `.env` with the real API key, run the image without
placing the key on the command line:

```powershell
docker run --rm -p 8501:8501 --env-file .env ghcr.io/moalhallak/ai-research-design-assistant:latest
```

Docker Compose is recommended when persistent `outputs/` storage is required.

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

## Plan History and Exports

Runtime data is stored under ignored `outputs/` directories. The Plan History
sidebar can search and reopen existing plans, start a new empty session, compare
plans, rename an entry or delete one plan without affecting the rest.

Validated plans can be downloaded as Markdown, JSON and PDF. The exports include
research-question validation, methodology advice, evaluation criteria and the
Risk Matrix.

## Tests and Quality Checks

Run the project checks from the repository root:

```powershell
python -m ruff check .
python -m compileall src app.py
python -m pytest
```

Validate the Docker configuration with:

```powershell
docker compose config --quiet
```

The running container exposes its Streamlit health endpoint at:

```text
http://localhost:8501/_stcore/health
```

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
|   |-- project-structure.md
|   `-- styles.css
|-- src/ai_research_design_assistant/
|-- tests/
|-- CONTRIBUTING.md
|-- LICENSE
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## Important Limitations

- Final plan generation depends on Academic Cloud / SAIA availability and a
  valid API key.
- LLM output can contain weak, biased or incorrect research advice even when
  its JSON structure is valid.
- Local validation checks technical structure and planning heuristics; it is
  not a scientific-quality guarantee.
- Local history is designed for a single local user and is not an authenticated
  multi-user data store.
- The system does not replace academic supervision, course requirements,
  literature review, ethics review or the student's own verification.
