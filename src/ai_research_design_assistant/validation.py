from __future__ import annotations

from ai_research_design_assistant.models import (
    ProjectRisk,
    ResearchQuestion,
    ResearchQuestionValidation,
    TopicAnalysis,
)
from ai_research_design_assistant.text import tokenize


def build_plan_checklist(
    analysis: TopicAnalysis,
    questions: list[ResearchQuestion],
    methodology_steps: list[str],
    evaluation_count: int,
    risks: list[ProjectRisk],
) -> dict[str, bool]:
    return {
        "topic_is_refined": analysis.refined_topic != analysis.original_idea,
        "has_multiple_research_questions": len(questions) >= 3,
        "questions_are_measurable": all(question.measurable_outcome for question in questions),
        "methodology_has_steps": len(methodology_steps) >= 3,
        "evaluation_is_defined": evaluation_count >= 3,
        "risks_are_mitigated": all(risk.mitigation for risk in risks),
    }


def validate_research_questions(
    questions: list[ResearchQuestion],
) -> list[ResearchQuestionValidation]:
    return [_validate_research_question(question) for question in questions]


def _validate_research_question(question: ResearchQuestion) -> ResearchQuestionValidation:
    text = question.question.strip()
    tokens = tokenize(text)
    outcome_tokens = tokenize(question.measurable_outcome)

    clarity = _clarity_rating(text, tokens)
    testability = _testability_rating(text, outcome_tokens)
    scope = _scope_rating(tokens)
    feasibility = _feasibility_rating(text, question.measurable_outcome)

    return ResearchQuestionValidation(
        question=question.question,
        clarity=clarity,
        clarity_reason=_clarity_reason(text, tokens, clarity),
        testability=testability,
        testability_reason=_testability_reason(outcome_tokens, testability),
        scope=scope,
        scope_reason=_scope_reason(tokens, scope),
        feasibility=feasibility,
        feasibility_reason=_feasibility_reason(
            text,
            question.measurable_outcome,
            feasibility,
        ),
        improvement_suggestion=_improvement_suggestion(clarity, testability, scope, feasibility),
    )


def _clarity_rating(text: str, tokens: list[str]) -> str:
    if text.endswith("?") and 8 <= len(tokens) <= 28:
        return "good"
    if text.endswith("?") or len(tokens) >= 6:
        return "medium"
    return "weak"


def _clarity_reason(text: str, tokens: list[str], rating: str) -> str:
    if rating == "good":
        return "The question is phrased as one complete question with a specific, readable length."
    if rating == "medium":
        return (
            "The question is understandable, but its wording or level of detail could be more specific."
        )
    return "The question is too short or is not phrased as a complete research question."


def _testability_rating(text: str, outcome_tokens: list[str]) -> str:
    measurable_terms = {
        "measure",
        "measurable",
        "score",
        "criteria",
        "criterion",
        "rubric",
        "compare",
        "evaluation",
        "count",
        "rating",
        "test",
        "tests",
        "bewerten",
        "messbar",
        "kriterien",
    }
    combined = set(tokenize(text)) | set(outcome_tokens)
    if combined & measurable_terms and outcome_tokens:
        return "good"
    if outcome_tokens:
        return "medium"
    return "weak"


def _testability_reason(outcome_tokens: list[str], rating: str) -> str:
    if rating == "good":
        return "A measurable outcome and an explicit measurement term are available."
    if rating == "medium":
        return "An outcome is provided, but the measurement method or success threshold is not explicit."
    if outcome_tokens:
        return "The stated outcome does not define a clear measurement or comparison."
    return "No measurable outcome is attached to the question."


def _scope_rating(tokens: list[str]) -> str:
    broad_terms = {"ai", "system", "technology", "education", "security", "research"}
    narrow_terms = {"prototype", "tool", "tools", "rubric", "scenario", "student", "students"}
    token_set = set(tokens)
    if len(tokens) < 5:
        return "too narrow"
    if len(tokens) > 32 or (len(token_set & broad_terms) >= 2 and not token_set & narrow_terms):
        return "too broad"
    return "focused"


def _scope_reason(tokens: list[str], rating: str) -> str:
    if rating == "focused":
        return "The question limits the investigation to a concrete artifact, context or evaluation setting."
    if rating == "too broad":
        return "The question combines broad domains without limiting the artifact or evaluation context."
    return "The question contains too little context to connect it to the wider research goal."


def _feasibility_rating(text: str, measurable_outcome: str) -> str:
    combined = set(tokenize(f"{text} {measurable_outcome}"))
    realistic_terms = {"prototype", "rubric", "checklist", "example", "scenario", "small", "count", "rating"}
    difficult_terms = {"all", "every", "global", "complete", "perfect", "prove"}
    if combined & difficult_terms:
        return "difficult"
    if combined & realistic_terms:
        return "realistic"
    return "unclear"


def _feasibility_reason(text: str, measurable_outcome: str, rating: str) -> str:
    combined = set(tokenize(f"{text} {measurable_outcome}"))
    if rating == "realistic":
        evidence = sorted(
            combined & {"prototype", "rubric", "checklist", "example", "scenario", "small", "count", "rating"}
        )
        signal = ", ".join(evidence) if evidence else "a limited evaluation setup"
        return f"The planned work uses {signal}, which is manageable for a student project."
    if rating == "difficult":
        return "The wording implies exhaustive or absolute evidence that is difficult to produce in one project."
    return "The available question and outcome do not yet show the required effort or resource limits."


def _improvement_suggestion(
    clarity: str,
    testability: str,
    scope: str,
    feasibility: str,
) -> str:
    if clarity == "weak":
        return "Rewrite the question as one clear question with a specific artefact and context."
    if testability == "weak":
        return "Add a measurable outcome such as a rubric score, comparison, count or test scenario."
    if scope == "too broad":
        return "Narrow the question to one prototype, target group, dataset or evaluation setting."
    if scope == "too narrow":
        return "Add enough context so the question connects to the overall research goal."
    if feasibility != "realistic":
        return "Limit the evaluation to a small number of examples and explicit criteria."
    return "Question is suitable for a small student research prototype."
