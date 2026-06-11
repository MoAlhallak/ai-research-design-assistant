from __future__ import annotations

import re
from typing import Any

from langchain_core.runnables import RunnableLambda

from ai_research_design_assistant.models import (
    MethodologyRecommendation,
    ProjectPlan,
    ProjectRisk,
    ResearchQuestion,
    TopicAnalysis,
)
from ai_research_design_assistant.templates import DEFAULT_EVALUATION, METHODOLOGY_KNOWLEDGE
from ai_research_design_assistant.text import normalize_text, tokenize, top_keywords
from ai_research_design_assistant.validation import build_plan_checklist, validate_research_questions


def build_project_planning_chain():
    """LangChain orchestration for idea analysis, planning and checklist validation."""

    return (
        RunnableLambda(_analyze_topic)
        | RunnableLambda(_create_research_questions)
        | RunnableLambda(_recommend_methodology)
        | RunnableLambda(_add_evaluation_and_risks)
        | RunnableLambda(_validate_project_plan)
    )


def plan_project(idea: str) -> ProjectPlan:
    if not idea.strip():
        raise ValueError("Project idea must not be empty.")
    return build_project_planning_chain().invoke({"idea": idea.strip()})["plan"]


def _analyze_topic(state: dict[str, Any]) -> dict[str, Any]:
    idea = state["idea"]
    keywords = top_keywords(idea, limit=8)
    focus_areas = _focus_areas(idea, keywords)
    broadness = _broadness_score(idea, keywords)
    scope_assessment = (
        "Too broad for one student project; narrow the artefact, context and evaluation."
        if broadness >= 3
        else "Focused enough for a first prototype if the evaluation remains small."
    )
    refined_topic = _refined_topic(idea, focus_areas)
    analysis = TopicAnalysis(
        original_idea=idea,
        refined_topic=refined_topic,
        scope_assessment=scope_assessment,
        detected_focus_areas=focus_areas,
        narrowing_suggestions=_narrowing_suggestions(focus_areas),
    )
    return {**state, "keywords": keywords, "analysis": analysis}


def _create_research_questions(state: dict[str, Any]) -> dict[str, Any]:
    analysis: TopicAnalysis = state["analysis"]
    artefact = _artefact_name(analysis)
    context = _context_name(analysis)
    questions = [
        ResearchQuestion(
            question=f"How can a {artefact} transform a broad project idea into a focused research plan for {context}?",
            rationale="This checks whether the system solves the central planning problem.",
            measurable_outcome="Quality score of generated plans using a fixed planning rubric.",
        ),
        ResearchQuestion(
            question=f"Which methodology and evaluation criteria are most suitable for {analysis.refined_topic}?",
            rationale="This connects the topic to concrete research design decisions.",
            measurable_outcome="Agreement between agent recommendations and a template-based expert checklist.",
        ),
        ResearchQuestion(
            question=f"What risks and limitations appear when using an agent to support planning for {context}?",
            rationale="This keeps the project academically cautious and avoids overclaiming.",
            measurable_outcome="Number and severity of identified risks across representative example ideas.",
        ),
    ]
    return {**state, "research_questions": questions}


def _recommend_methodology(state: dict[str, Any]) -> dict[str, Any]:
    idea_tokens = set(_tokens(state["idea"]))
    selected = max(
        METHODOLOGY_KNOWLEDGE,
        key=lambda item: len(idea_tokens & item["keywords"]),
    )
    methodology = MethodologyRecommendation(
        name=selected["name"],
        fit=selected["fit"],
        steps=list(selected["steps"]),
        tools=list(selected["tools"]),
    )
    return {**state, "methodology": methodology}


def _add_evaluation_and_risks(state: dict[str, Any]) -> dict[str, Any]:
    prototype = [
        "Streamlit input form for project ideas",
        "Template and memory lookup from a small knowledge base",
        "Planning agent that outputs questions, methods, evaluation and risks",
        "Markdown, JSON and PDF export for the final project plan",
    ]
    risks = [
        ProjectRisk(
            risk="Suggestions can be too generic.",
            mitigation="Use topic-specific templates and require measurable outcomes in every question.",
        ),
        ProjectRisk(
            risk="The agent can sound certain even when evidence is missing.",
            mitigation="Show assumptions, checklist results and explicit limitations in the export.",
        ),
        ProjectRisk(
            risk="The project scope can grow beyond a student prototype.",
            mitigation="Limit the demo to a small knowledge base, a few scenarios and rubric-based evaluation.",
        ),
    ]
    return {
        **state,
        "prototype": prototype,
        "evaluation_criteria": DEFAULT_EVALUATION,
        "risks": risks,
        "sprint_plan": [
            "Sprint 1: architecture, templates and example knowledge base",
            "Sprint 2: topic analysis and research-question generation",
            "Sprint 3: methodology advisor, evaluation criteria and risk analysis",
            "Sprint 4: Streamlit demo, export functions, tests and documentation",
        ],
    }


def _validate_project_plan(state: dict[str, Any]) -> dict[str, Any]:
    questions: list[ResearchQuestion] = state["research_questions"]
    analysis: TopicAnalysis = state["analysis"]
    checklist = build_plan_checklist(
        analysis=analysis,
        questions=questions,
        methodology_steps=state["methodology"].steps,
        evaluation_count=len(state["evaluation_criteria"]),
        risks=state["risks"],
    )
    question_validations = validate_research_questions(questions)
    plan = ProjectPlan(
        idea=state["idea"],
        topic_analysis=analysis,
        research_questions=questions,
        question_validations=question_validations,
        methodology=state["methodology"],
        prototype=state["prototype"],
        evaluation_criteria=state["evaluation_criteria"],
        risks=state["risks"],
        checklist=checklist,
        sprint_plan=state["sprint_plan"],
    )
    return {**state, "plan": plan}


def _focus_areas(idea: str, keywords: list[str]) -> list[str]:
    text_tokens = set(_tokens(idea))
    areas = []
    matched_mapping_tokens = set()
    mappings = [
        ("Agentic AI", {"agentic", "ai", "agent", "agents"}),
        ("Security", {"security", "risk", "risks", "safety", "attack"}),
        ("Tool Usage", {"tool", "tools", "api", "function", "usage", "nutzung"}),
        ("Evaluation", {"evaluation", "evaluate", "test", "tests", "criteria", "measure"}),
        ("Prototype", {"prototype", "prototyp", "demo", "mvp"}),
        ("Research Design", {"research", "planung", "planning", "methodology", "methodik", "design"}),
        ("Memory and templates", {"memory", "chroma", "templates", "examples"}),
    ]
    for label, tokens in mappings:
        if tokens & text_tokens:
            areas.append(label)
            matched_mapping_tokens.update(tokens)
    for keyword in keywords:
        if keyword in _STOP_FOCUS_WORDS or keyword in matched_mapping_tokens:
            continue
        label = keyword.title()
        if label not in areas and len(areas) < 5:
            areas.append(label)
    return areas[:5] or ["Research planning"]


def _broadness_score(idea: str, keywords: list[str]) -> int:
    broad_terms = {"ai", "agentic", "security", "education", "research", "planning", "system"}
    score = len(set(keywords) & broad_terms)
    if len(idea.split()) < 8:
        score += 1
    normalized = normalize_text(idea)
    if not re.search(r"\b(evaluate|measure|prototype|compare|students|tool|scenario)\b", normalized):
        score += 1
    return score


def _refined_topic(idea: str, focus_areas: list[str]) -> str:
    if "Security" in focus_areas:
        return "Evaluation of security risks in a small agentic AI tool-use prototype"
    if "Research Design" in focus_areas:
        return "Template-supported agent for generating realistic student research plans"
    return f"Focused prototype and evaluation plan for: {idea}"


def _narrowing_suggestions(focus_areas: list[str]) -> list[str]:
    suggestions = [
        "Define one target user group, for example bachelor or master students.",
        "Limit the prototype to one workflow: idea analysis to project-plan export.",
        "Use three to five example topics for evaluation instead of many domains.",
    ]
    if "Security" in focus_areas:
        suggestions.insert(0, "Choose one threat model, such as unsafe tool calls or prompt injection.")
    if "Memory and templates" in focus_areas:
        suggestions.append("Keep the knowledge base small and cite which template informed each suggestion.")
    return suggestions


def _artefact_name(analysis: TopicAnalysis) -> str:
    if "Security" in analysis.detected_focus_areas:
        return "security-aware planning agent"
    return "research planning agent"


def _context_name(analysis: TopicAnalysis) -> str:
    if "Security" in analysis.detected_focus_areas:
        return "agentic AI security projects"
    return "student research projects"


def _tokens(text: str) -> list[str]:
    return tokenize(text)


_STOP_FOCUS_WORDS = {
    "and",
    "about",
    "der",
    "die",
    "das",
    "den",
    "ein",
    "eine",
    "einen",
    "ich",
    "i",
    "like",
    "moechte",
    "mit",
    "want",
    "would",
    "und",
    "ueber",
    "zu",
    "zur",
    "will",
    "wuerde",
}
