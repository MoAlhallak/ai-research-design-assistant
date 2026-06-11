# Project Structure

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
|   |-- agent.py
|   |-- cli.py
|   |-- exporters.py
|   |-- llm.py
|   |-- memory.py
|   |-- models.py
|   |-- planning.py
|   |-- templates.py
|   |-- text.py
|   |-- validation.py
|   `-- __init__.py
`-- tests/
    `-- test_sprint_2.py
```

## Core Modules

- `agent.py`: public entry point for generating a research plan.
- `planning.py`: LangChain workflow for topic analysis, research questions, methodology, evaluation and risks.
- `templates.py`: methodology templates and default evaluation criteria.
- `validation.py`: checklist validation and Sprint-2 research-question validation.
- `memory.py`: ChromaDB-backed memory with local JSON fallback.
- `models.py`: Pydantic models for structured output.
- `exporters.py`: Markdown, JSON and PDF exports.
- `llm.py`: optional SAIA / Academic Cloud plan refinement with local fallback.
- `cli.py`: command-line interface.
- `text.py`: German/English keyword normalization and text helpers.

## Cleaned Files

The duplicate `sprint_1/` source snapshot and generated folders such as
`outputs/`, caches, `__pycache__/` and `*.egg-info/` were removed from the active
submission structure. Sprint-1 planning notes are kept in
`docs/sprint-1-preparation.md`. Sprint-2 implementation notes are kept in
`docs/sprint-2-description.md`.

## Scope

The current core prototype is focused on research project planning. Paper search,
PDF retrieval and citation-network analysis are outside the cleaned project
scope and can be treated as possible future extensions.
