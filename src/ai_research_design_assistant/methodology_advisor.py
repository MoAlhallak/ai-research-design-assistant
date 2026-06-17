from __future__ import annotations

from ai_research_design_assistant.models import MethodologyAdvice, ResearchQuestion, TopicAnalysis


def advise_methodologies(
    analysis: TopicAnalysis,
    research_questions: list[ResearchQuestion],
    project_type: str,
) -> list[MethodologyAdvice]:
    focus = set(analysis.detected_focus_areas)
    question_text = " ".join(question.question.lower() for question in research_questions)
    candidates = [
        _literature_review(),
        _prototype(),
        _experiment(),
        _comparison(),
        _case_study(),
        _evaluation_checklist(),
    ]
    scored = [
        (_method_score(method, focus, question_text, project_type), method)
        for method in candidates
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [method for score, method in scored if score > 0][:4]
    return selected or [_evaluation_checklist(), _literature_review()]


def _method_score(
    method: MethodologyAdvice,
    focus: set[str],
    question_text: str,
    project_type: str,
) -> int:
    name = method.method_name.lower()
    score = 0
    if "prototype" in name and ("Prototype" in focus or "tool" in question_text):
        score += 4
    if "experiment" in name and ("Evaluation" in focus or "test" in question_text):
        score += 3
    if "comparison" in name and ("compare" in question_text or "criteria" in question_text):
        score += 3
    if "case study" in name and ("Security" in focus or "agentic" in question_text):
        score += 2
    if "checklist" in name and ("Evaluation" in focus or "rubric" in question_text):
        score += 4
    if "literature" in name and ("Research Design" in focus or "methodology" in question_text):
        score += 2
    if project_type.lower() in name:
        score += 2
    return score


def _literature_review() -> MethodologyAdvice:
    return MethodologyAdvice(
        method_name="Literature Review",
        description="Structured review of concepts, related systems and evaluation approaches.",
        fit_reason="Useful for grounding the project in existing research before building or evaluating.",
        required_steps=[
            "Define search terms and inclusion criteria.",
            "Collect a small set of relevant academic and technical sources.",
            "Extract concepts, methods, risks and evaluation criteria.",
            "Summarize findings into design requirements for the project.",
        ],
        required_data_or_artifacts=["Search terms", "source list", "extraction table"],
        limitations=[
            "Coverage may be incomplete in a short student project.",
            "Quality depends on source selection and documentation.",
        ],
    )


def _prototype() -> MethodologyAdvice:
    return MethodologyAdvice(
        method_name="Prototype",
        description="Build a small working artefact to demonstrate and evaluate the planning workflow.",
        fit_reason="Fits projects that study an assistant, workflow, tool-use scenario or generated output.",
        required_steps=[
            "Define the minimum workflow and user input.",
            "Implement the smallest useful assistant behavior.",
            "Generate plans for representative example topics.",
            "Document assumptions, limits and observed behavior.",
        ],
        required_data_or_artifacts=["Prototype app", "example inputs", "generated plans", "logs"],
        limitations=[
            "A prototype does not prove general effectiveness.",
            "Results depend on the selected example topics.",
        ],
    )


def _experiment() -> MethodologyAdvice:
    return MethodologyAdvice(
        method_name="Experiment",
        description="Run controlled test scenarios and compare outputs against predefined criteria.",
        fit_reason="Useful when research questions ask whether a change improves quality or reliability.",
        required_steps=[
            "Define test scenarios and expected observations.",
            "Run the assistant on each scenario.",
            "Score outputs with the same rubric.",
            "Compare results and document patterns.",
        ],
        required_data_or_artifacts=["test scenarios", "rubric", "output set", "score sheet"],
        limitations=[
            "Small experiments may not generalize.",
            "Rubric scoring can be subjective without multiple raters.",
        ],
    )


def _comparison() -> MethodologyAdvice:
    return MethodologyAdvice(
        method_name="Comparison",
        description="Compare plans, methods or outputs across examples, versions or baselines.",
        fit_reason="Fits projects that need to show differences between generated plans or approaches.",
        required_steps=[
            "Define comparison dimensions.",
            "Select baseline or previous plans.",
            "Compare focus areas, questions, method and evaluation criteria.",
            "Summarize differences and implications.",
        ],
        required_data_or_artifacts=["baseline plan", "current plan", "comparison table"],
        limitations=[
            "Comparison quality depends on fair criteria.",
            "Differences may be descriptive rather than causal.",
        ],
    )


def _case_study() -> MethodologyAdvice:
    return MethodologyAdvice(
        method_name="Case Study",
        description="Analyze one realistic project scenario in depth.",
        fit_reason="Useful when the topic is specific, contextual or security-oriented.",
        required_steps=[
            "Select one realistic case.",
            "Describe context, assumptions and constraints.",
            "Apply the assistant workflow to the case.",
            "Evaluate strengths, weaknesses and transferability.",
        ],
        required_data_or_artifacts=["case description", "generated plan", "evaluation notes"],
        limitations=[
            "One case is not representative of all contexts.",
            "Findings must be framed as contextual insights.",
        ],
    )


def _evaluation_checklist() -> MethodologyAdvice:
    return MethodologyAdvice(
        method_name="Evaluation Checklist",
        description="Use a structured checklist to judge plan quality and completeness.",
        fit_reason="Fits research-planning tools because outputs can be checked against explicit criteria.",
        required_steps=[
            "Define checklist criteria.",
            "Apply criteria to each generated plan.",
            "Record pass/fail or quality ratings.",
            "Identify recurring weaknesses and improvements.",
        ],
        required_data_or_artifacts=["checklist", "generated plans", "ratings"],
        limitations=[
            "Checklist criteria must be justified.",
            "Checklist results may miss nuanced qualitative issues.",
        ],
    )
