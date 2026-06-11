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
    testability: str
    scope: str
    feasibility: str
    improvement_suggestion: str


class MethodologyRecommendation(BaseModel):
    name: str
    fit: str
    steps: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)


class EvaluationCriterion(BaseModel):
    name: str
    description: str
    measurement: str


class ProjectRisk(BaseModel):
    risk: str
    mitigation: str


class ProjectPlan(BaseModel):
    idea: str
    topic_analysis: TopicAnalysis
    research_questions: list[ResearchQuestion]
    question_validations: list[ResearchQuestionValidation] = Field(default_factory=list)
    methodology: MethodologyRecommendation
    prototype: list[str] = Field(default_factory=list)
    evaluation_criteria: list[EvaluationCriterion] = Field(default_factory=list)
    risks: list[ProjectRisk] = Field(default_factory=list)
    checklist: dict[str, bool]
    sprint_plan: list[str] = Field(default_factory=list)
