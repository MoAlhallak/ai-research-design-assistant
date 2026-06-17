from __future__ import annotations

from ai_research_design_assistant.models import MethodologyAdvice, RiskMatrixItem, TopicAnalysis


def build_risk_matrix(
    analysis: TopicAnalysis,
    methodology_advice: list[MethodologyAdvice],
) -> list[RiskMatrixItem]:
    focus = set(analysis.detected_focus_areas)
    method_names = {method.method_name for method in methodology_advice}
    risks = [
        RiskMatrixItem(
            risk_title="Generic recommendations",
            description="The assistant may suggest methods or criteria that are too broad for the project.",
            probability="medium",
            impact="medium",
            mitigation_strategy="Use focus-area-specific templates and require measurable outcomes.",
        ),
        RiskMatrixItem(
            risk_title="Over-scoped project",
            description="The research plan may include too many goals for a student prototype.",
            probability="medium",
            impact="high",
            mitigation_strategy="Limit the project to one workflow, small examples and a clear evaluation rubric.",
        ),
        RiskMatrixItem(
            risk_title="Weak evaluation evidence",
            description="Evaluation may rely on subjective judgments without documented criteria.",
            probability="medium",
            impact="high",
            mitigation_strategy="Use a checklist, saved outputs and explicit evidence for every criterion.",
        ),
    ]
    if "Security" in focus:
        risks.append(
            RiskMatrixItem(
                risk_title="Incomplete threat model",
                description="Security-related plans may miss relevant attack paths or unsafe tool-use cases.",
                probability="medium",
                impact="high",
                mitigation_strategy="Define one narrow threat model and document excluded risks.",
            )
        )
    if "Prototype" in focus or "Prototype" in method_names:
        risks.append(
            RiskMatrixItem(
                risk_title="Prototype bias",
                description="Results may reflect the small prototype setup rather than general assistant quality.",
                probability="high",
                impact="medium",
                mitigation_strategy="Frame findings as prototype evidence and test several representative inputs.",
            )
        )
    return risks
