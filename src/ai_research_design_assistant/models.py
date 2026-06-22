from __future__ import annotations

from pydantic import BaseModel, Field


class TopicAnalysis(BaseModel):
    original_idea: str
    refined_topic: str
    scope_assessment: str
    detected_focus_areas: list[str] = Field(default_factory=list)
    narrowing_suggestions: list[str] = Field(default_factory=list)


class ResearchQuestion(BaseModel):
    question: str
    rationale: str
    measurable_outcome: str


class ResearchQuestionValidation(BaseModel):
    question: str
    clarity: str
    clarity_reason: str = ""
    testability: str
    testability_reason: str = ""
    scope: str
    scope_reason: str = ""
    feasibility: str
    feasibility_reason: str = ""
    improvement_suggestion: str


class MethodologyRecommendation(BaseModel):
    name: str
    fit: str
    steps: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)


class MethodologyAdvice(BaseModel):
    method_name: str
    description: str
    fit_reason: str
    required_steps: list[str] = Field(default_factory=list)
    required_data_or_artifacts: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class EvaluationCriterion(BaseModel):
    name: str
    description: str
    measurement: str
    expected_evidence: str = ""
    priority: str = "medium"


class ProjectRisk(BaseModel):
    risk: str
    mitigation: str


class RiskMatrixItem(BaseModel):
    risk_title: str
    description: str
    probability: str
    impact: str
    mitigation_strategy: str


class MemoryComparison(BaseModel):
    same_focus_areas: list[str] = Field(default_factory=list)
    different_focus_areas: list[str] = Field(default_factory=list)
    similar_methodology: str = "unclear"
    changed_research_questions: list[str] = Field(default_factory=list)
    recommendation: str = ""


class ProjectPlan(BaseModel):
    idea: str
    topic_analysis: TopicAnalysis
    research_questions: list[ResearchQuestion]
    question_validations: list[ResearchQuestionValidation] = Field(default_factory=list)
    methodology: MethodologyRecommendation
    methodology_advice: list[MethodologyAdvice] = Field(default_factory=list)
    prototype: list[str] = Field(default_factory=list)
    evaluation_criteria: list[EvaluationCriterion] = Field(default_factory=list)
    risk_matrix: list[RiskMatrixItem] = Field(default_factory=list)
    risks: list[ProjectRisk] = Field(default_factory=list)
    memory_comparison: MemoryComparison | None = None
    checklist: dict[str, bool]
    sprint_plan: list[str] = Field(default_factory=list)
