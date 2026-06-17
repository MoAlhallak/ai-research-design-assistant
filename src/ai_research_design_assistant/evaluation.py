from __future__ import annotations

from ai_research_design_assistant.models import (
    EvaluationCriterion,
    MethodologyAdvice,
    ResearchQuestion,
    TopicAnalysis,
)


def build_evaluation_criteria(
    analysis: TopicAnalysis,
    questions: list[ResearchQuestion],
    methodology_advice: list[MethodologyAdvice],
) -> list[EvaluationCriterion]:
    focus = set(analysis.detected_focus_areas)
    question_text = " ".join(question.question.lower() for question in questions)
    method_names = " ".join(method.method_name.lower() for method in methodology_advice)
    criteria = [
        EvaluationCriterion(
            name="Quality of generated research plan",
            description="The plan is coherent, focused and useful for a student research project.",
            measurement="Rate topic fit, question quality, method fit and completeness on a fixed rubric.",
            expected_evidence="Completed rubric for each generated plan.",
            priority="high",
        ),
        EvaluationCriterion(
            name="Functional correctness",
            description="The assistant produces all required sections without invalid or missing data.",
            measurement="Check whether topic, questions, methodology, evaluation, risks and export are present.",
            expected_evidence="Checklist results and generated output files.",
            priority="high",
        ),
        EvaluationCriterion(
            name="Reproducibility",
            description="The plan can be regenerated and reviewed with documented inputs and criteria.",
            measurement="Record input prompt, generated plan and evaluation rubric for each test case.",
            expected_evidence="Saved JSON plans and documented test inputs.",
            priority="medium",
        ),
    ]
    if "Security" in focus or "security" in question_text:
        criteria.append(
            EvaluationCriterion(
                name="Security",
                description="The plan identifies relevant security risks and realistic mitigations.",
                measurement="Count identified risks and rate mitigation relevance with a security checklist.",
                expected_evidence="Risk matrix and mitigation notes.",
                priority="high",
            )
        )
    if "Prototype" in focus or "prototype" in method_names:
        criteria.append(
            EvaluationCriterion(
                name="Usability",
                description="The prototype workflow is understandable and efficient for students.",
                measurement="Collect short user feedback or expert review on clarity and usefulness.",
                expected_evidence="Feedback form, notes or usability ratings.",
                priority="medium",
            )
        )
    if "experiment" in method_names:
        criteria.append(
            EvaluationCriterion(
                name="Performance",
                description="The assistant responds fast enough for an interactive planning workflow.",
                measurement="Measure generation time across representative example inputs.",
                expected_evidence="Timing table for test scenarios.",
                priority="low",
            )
        )
    criteria.append(
        EvaluationCriterion(
            name="Completeness",
            description="The output covers all expected research-planning components.",
            measurement="Check all required sections against the project checklist.",
            expected_evidence="Checklist pass rate and missing-section notes.",
            priority="high",
        )
    )
    return criteria
