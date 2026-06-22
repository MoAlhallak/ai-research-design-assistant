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

- show saved project conversations in a left history sidebar
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

## Worked Example

The reviewer demo uses this input:

```text
I want to work on Agentic AI Security and Tool Usage.
```

### Detected Focus Areas

- Agentic AI
- Security
- Tool Usage

Weak intent words such as `I`, `want` and `work` are filtered and do not appear
as focus areas.

### Generated Research Questions

1. How can a security-aware planning agent transform a broad project idea into
   a focused research plan for agentic AI security projects?
2. Which methodology and evaluation criteria are most suitable for evaluation
   of security risks in a small agentic AI tool-use prototype?
3. What risks and limitations appear when using an agent to support planning for
   agentic AI security projects?

### Validation Results

| RQ | Clarity | Testability | Scope | Feasibility |
|---|---|---|---|---|
| RQ1 | good | good | too broad | realistic |
| RQ2 | good | good | focused | realistic |
| RQ3 | good | medium | too broad | realistic |

Every rating includes a rule-based reason. For example, RQ2 is focused because
it limits the work to a small prototype and a concrete evaluation context. Broad
questions receive a recommendation to narrow the artifact, target group,
dataset or evaluation setting.

### Methodology Suggestion

The Methodology Advisor suggests `Prototype` as the primary method because the
topic concerns a concrete tool-use artifact that can be implemented and tested
with representative scenarios.

### Evaluation Criteria

- Quality of generated research plan
- Functional correctness
- Reproducibility
- Security
- Usability
- Completeness

### Risk Matrix

- Generic recommendations
- Over-scoped project
- Weak evaluation evidence
- Incomplete threat model
- Prototype bias

Each risk also contains probability, impact and a mitigation strategy.

## Changes after Sprint 2 feedback

- added a concrete worked example for the reviewer demo
- made validation logic transparent with a reason for every rating
- clarified that local rule-based planning is the stable core and AI refinement
  remains optional and internal
- improved demo value through clean focus areas and expandable validation details
