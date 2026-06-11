from __future__ import annotations

from ai_research_design_assistant.models import EvaluationCriterion


METHODOLOGY_KNOWLEDGE = [
    {
        "keywords": {"security", "risk", "risks", "safety", "agentic", "tool", "tools"},
        "name": "Prototype-based security evaluation",
        "fit": (
            "Useful when the project studies how an agent behaves under realistic tool-use "
            "or safety-critical scenarios."
        ),
        "steps": [
            "Define a narrow threat model and the agent capabilities in scope.",
            "Build or configure a small agent prototype with controlled tools.",
            "Create benign and adversarial test scenarios.",
            "Log tool calls, decisions, failures and recovery behavior.",
            "Compare results against explicit safety and correctness criteria.",
        ],
        "tools": ["Python", "LangChain", "Streamlit", "ChromaDB", "evaluation rubric"],
    },
    {
        "keywords": {"education", "students", "learning", "study", "planning", "assistant"},
        "name": "Design science with user-oriented evaluation",
        "fit": (
            "Useful when the project builds an artefact that supports students or users in a "
            "structured academic workflow."
        ),
        "steps": [
            "Collect user needs and define the planning problem.",
            "Design templates and checklists for the artefact.",
            "Implement a small working prototype.",
            "Evaluate plan quality with example tasks and user feedback.",
            "Refine limitations and usage boundaries.",
        ],
        "tools": ["Python", "Streamlit", "Pydantic", "ChromaDB", "questionnaire"],
    },
    {
        "keywords": {"memory", "template", "templates", "methodology", "methodik", "planning"},
        "name": "Template-supported planning evaluation",
        "fit": (
            "Useful when the system uses structured templates and saved examples to turn broad "
            "ideas into realistic research plans."
        ),
        "steps": [
            "Define a small set of planning templates.",
            "Generate plans for representative student ideas.",
            "Check each plan against measurability and scope criteria.",
            "Compare generated plans with a manually prepared reference checklist.",
            "Document limitations and cases where user feedback is needed.",
        ],
        "tools": ["Python", "LangChain", "Pydantic", "ChromaDB", "Markdown/PDF export"],
    },
]


DEFAULT_EVALUATION = [
    EvaluationCriterion(
        name="Correctness",
        description="The plan answers the user's idea without changing the intended topic.",
        measurement="Expert or rubric rating from 1 to 5 for topic fit and factual plausibility.",
    ),
    EvaluationCriterion(
        name="Measurability",
        description="Research questions and evaluation criteria can be tested in a small project.",
        measurement="Count how many proposed questions include variables, artefacts or criteria.",
    ),
    EvaluationCriterion(
        name="Usefulness",
        description="The output helps a student move from a broad idea to an actionable plan.",
        measurement="Short user feedback questionnaire after completing a planning task.",
    ),
    EvaluationCriterion(
        name="Boundaries",
        description="The plan states assumptions, risks and limits instead of overclaiming.",
        measurement="Checklist pass rate for scope, risks, data needs and evaluation limits.",
    ),
]
