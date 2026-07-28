# Project Structure

```text
.
|-- .env.example
|-- .gitignore
|-- app.py
|-- CONTRIBUTING.md
|-- docs/
|   |-- assets/
|   |-- index.html
|   |-- project-structure.md
|   |-- sprint-1-preparation.md
|   |-- sprint-2-description.md
|   |-- styles.css
|   `-- sprint-3-description.md
|-- LICENSE
|-- pyproject.toml
|-- README.md
|-- scripts/
|   `-- create_final_zip.py
|-- src/ai_research_design_assistant/
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
|   |-- validation.py
|   `-- __init__.py
`-- tests/
    |-- test_sprint_2.py
    `-- test_sprint_3.py
```

## Core Modules

- `agent.py`: public entry point for generating a research plan.
- `planning.py`: LangChain workflow for topic analysis, research questions, methodology, evaluation and risks.
- `methodology_advisor.py`: Sprint-3 method suggestions with fit, steps, artifacts and limitations.
- `evaluation.py`: Sprint-3 evaluation criteria builder with measurable evidence.
- `risks.py`: Sprint-3 risk matrix builder with probability, impact and mitigation.
- `templates.py`: methodology templates and default evaluation criteria.
- `validation.py`: checklist validation and Sprint-2 research-question validation.
- `memory.py`: ChromaDB-backed memory with local JSON fallback, keyword search and plan comparison.
- `models.py`: Pydantic models for structured output.
- `exporters.py`: Markdown, JSON and PDF exports.
- `llm.py`: required SAIA / Academic Cloud generation of the final plan from
  the local scaffold, including JSON parsing and Pydantic validation.
- `cli.py`: developer command-line interface for the deterministic local
  scaffold.
- `text.py`: German/English keyword normalization and text helpers.

## Final Generation Architecture

```text
User Input
→ Local Planning Scaffold
→ Structured SAIA Request
→ LLM JSON Response
→ Pydantic Validation
→ ProjectPlan
→ UI, Memory and Export
```

The Streamlit generation workflow requires `ACADEMIC_CLOUD_API_KEY`. If SAIA is
unavailable or its response cannot be validated as a `ProjectPlan`, the UI shows
an error instead of returning the scaffold as a final result. Pydantic validates
the response structure and data types, not the scientific correctness of its
content.

Local Plan History operations—including loading, searching, renaming and
deleting existing plans—do not require an API call.

## Project Website

`docs/index.html` and `docs/styles.css` form the static GitHub Pages portfolio.
No build step is required. `docs/assets/` is reserved for delivery media such as
the pitch deck and product video when those files become available.

## Cleaned Files

The duplicate `sprint_1/` source snapshot and generated folders such as
`outputs/`, caches, `__pycache__/` and `*.egg-info/` were removed from the active
submission structure. Sprint-1 planning notes are kept in
`docs/sprint-1-preparation.md`. Sprint-2 implementation notes are kept in
`docs/sprint-2-description.md`. Sprint-3 implementation notes are kept in
`docs/sprint-3-description.md`.

`scripts/create_final_zip.py` creates the ignored Moodle submission archive
under `release/` while excluding secrets, environments, runtime outputs and
caches.

## Scope

The current core prototype is focused on research project planning. Paper search,
PDF retrieval and citation-network analysis are outside the cleaned project
scope and can be treated as possible future extensions.
