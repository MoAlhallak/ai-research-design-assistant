from __future__ import annotations

import asyncio
import json

from ai_research_design_assistant.agent import plan
from ai_research_design_assistant.exporters import export_project_plan
from ai_research_design_assistant.llm import refine_project_plan_with_fallback
from ai_research_design_assistant.memory import load_project_plans, save_project_plan
from ai_research_design_assistant.validation import validate_research_questions


def test_topic_analysis_filters_german_stopwords() -> None:
    project_plan = plan(
        "Ich moechte gerne ueber Agentic AI Security und Tool-Nutzung arbeiten."
    )

    focus_areas = {area.lower() for area in project_plan.topic_analysis.detected_focus_areas}

    assert "moechte" not in focus_areas
    assert "gerne" not in focus_areas
    assert "ueber" not in focus_areas
    assert "Security" in project_plan.topic_analysis.detected_focus_areas
    assert "Tool Usage" in project_plan.topic_analysis.detected_focus_areas


def test_research_questions_are_generated() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    assert len(project_plan.research_questions) >= 3
    assert all(question.question for question in project_plan.research_questions)


def test_question_validation_returns_expected_fields() -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    validations = validate_research_questions(project_plan.research_questions)

    assert validations
    first = validations[0].model_dump()
    assert {"clarity", "testability", "scope", "feasibility"} <= set(first)
    assert first["improvement_suggestion"]


def test_memory_save_load_json_fallback(tmp_path) -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    save_project_plan(project_plan, memory_dir=tmp_path)
    loaded = load_project_plans(memory_dir=tmp_path)

    assert len(loaded) == 1
    assert loaded[0].topic_analysis.refined_topic == project_plan.topic_analysis.refined_topic


def test_markdown_and_json_export_create_files(tmp_path) -> None:
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    export_project_plan(project_plan, tmp_path)

    markdown_path = tmp_path / "research-plan.md"
    json_path = tmp_path / "research-plan.json"
    assert markdown_path.exists()
    assert json_path.exists()
    assert "Research Question Validation" in markdown_path.read_text(encoding="utf-8")
    assert json.loads(json_path.read_text(encoding="utf-8"))["research_questions"]


def test_llm_fallback_does_not_crash_without_api_key(monkeypatch) -> None:
    monkeypatch.setenv("ACADEMIC_CLOUD_API_KEY", "")
    project_plan = plan("Agentic AI Security Tool Usage Evaluation Prototype")

    fallback_plan, llm_ok, error = asyncio.run(refine_project_plan_with_fallback(project_plan))

    assert fallback_plan == project_plan
    assert llm_ok is False
    assert error
