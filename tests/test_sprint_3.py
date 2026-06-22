from __future__ import annotations

from ai_research_design_assistant.agent import plan
from ai_research_design_assistant.exporters import project_plan_to_markdown
from ai_research_design_assistant.memory import save_project_plan, search_project_plans


def test_methodology_advisor_returns_suitable_method() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    assert project_plan.methodology_advice
    assert any(method.method_name == "Prototype" for method in project_plan.methodology_advice)


def test_methodology_advice_contains_explanation_steps_and_limitations() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    for method in project_plan.methodology_advice:
        assert method.description
        assert method.fit_reason
        assert method.required_steps
        assert method.limitations


def test_evaluation_builder_returns_measurable_criteria() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    assert project_plan.evaluation_criteria
    for criterion in project_plan.evaluation_criteria:
        assert criterion.measurement
        assert criterion.expected_evidence
        assert criterion.priority in {"high", "medium", "low"}


def test_risk_matrix_returns_probability_impact_and_mitigation() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    assert project_plan.risk_matrix
    for risk in project_plan.risk_matrix:
        assert risk.probability in {"low", "medium", "high"}
        assert risk.impact in {"low", "medium", "high"}
        assert risk.mitigation_strategy


def test_memory_search_finds_saved_plan(tmp_path) -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")
    save_project_plan(project_plan, memory_dir=tmp_path)

    results = search_project_plans("security prototype", memory_dir=tmp_path)

    assert results
    assert results[0].topic_analysis.refined_topic == project_plan.topic_analysis.refined_topic


def test_export_includes_sprint_3_sections() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    markdown = project_plan_to_markdown(project_plan)

    assert "## Methodology Advisor" in markdown
    assert "## Evaluation Builder" in markdown
    assert "## Risk Matrix" in markdown


def test_validation_returns_transparent_reasons() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    assert len(project_plan.question_validations) == len(project_plan.research_questions)
    for validation in project_plan.question_validations:
        assert validation.clarity_reason
        assert validation.testability_reason
        assert validation.scope_reason
        assert validation.feasibility_reason
        assert validation.improvement_suggestion


def test_worked_example_has_clean_focus_areas() -> None:
    project_plan = plan("I want to work on Agentic AI Security and Tool Usage.")

    focus_areas = project_plan.topic_analysis.detected_focus_areas
    assert focus_areas == ["Agentic AI", "Security", "Tool Usage"]
    assert "Work" not in focus_areas


def test_export_includes_validation_reasons() -> None:
    project_plan = plan("I want to work on Agentic AI Security and Tool Usage.")

    markdown = project_plan_to_markdown(project_plan)

    assert "Clarity reason:" in markdown
    assert "Testability reason:" in markdown
    assert "Scope reason:" in markdown
    assert "Feasibility reason:" in markdown
