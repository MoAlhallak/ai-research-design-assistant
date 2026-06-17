# Sprint 3 Description

Sprint 3 extends the existing AI Research Design Assistant from a research
question planning prototype into a stronger methodology and evaluation planning
assistant. The original planning pipeline, Streamlit app structure and offline
fallback behavior remain intact.

## Methodology Advisor

The Methodology Advisor suggests suitable research methods based on topic
analysis, focus areas, research questions and project type.

Supported method types:

- Literature Review
- Prototype
- Experiment
- Comparison
- Case Study
- Evaluation Checklist

Each method suggestion includes:

- method name
- short description
- why it fits the project
- required steps
- required data or artifacts
- possible limitations

The output is represented with Pydantic models and is included in the UI and
exports.

## Evaluation Builder

The Evaluation Builder creates concrete evaluation criteria connected to the
research questions and methodology.

Each criterion includes:

- criterion name
- description
- how to measure it
- expected evidence
- priority: high, medium or low

Example criteria include functional correctness, usability, security,
performance, completeness, reproducibility and quality of the generated research
plan.

## Risk Matrix

The risk section was upgraded from a simple list into a structured risk matrix.

Each risk includes:

- risk title
- description
- probability: low, medium or high
- impact: low, medium or high
- mitigation strategy

The Streamlit app shows the matrix as a readable table.

## Improved Memory

Memory now supports more than saving and loading plans.

Implemented improvements:

- show recent saved plans
- search saved plans by keyword
- load a saved plan
- compare a current plan with one previous saved plan

The comparison highlights same focus areas, different focus areas, methodology
similarity, changed research questions and a short recommendation.

## Updated Streamlit UI

The Streamlit interface keeps the existing modern card design and adds clearer
Sprint 3 tabs:

- Overview
- Questions
- Methodology Advisor
- Evaluation Builder
- Risk Matrix
- Memory
- Export

Method cards explain fit, steps, artifacts and limitations. Evaluation criteria
and risks are shown as tables. Memory search, recent plans and plan comparison
are available in the Memory tab.

## Updated Exports

Markdown, JSON and PDF exports now include:

- methodology advisor output
- evaluation criteria
- risk matrix
- memory comparison summary when available

## Tests

Sprint 3 adds tests for:

- methodology advisor output
- method explanation, steps and limitations
- measurable evaluation criteria
- risk matrix probability, impact and mitigation
- memory search
- export sections for Sprint 3
