from __future__ import annotations

from ai_research_design_assistant.agent import plan
from ai_research_design_assistant.memory import (
    default_plan_title,
    delete_project_plan,
    load_project_plans,
    rename_project_plan,
    save_project_plan,
    search_project_plans,
)


def _make_plan(idea: str):
    return plan(idea)


def test_save_assigns_id_and_title(tmp_path) -> None:
    project_plan = _make_plan("Agentic AI Security Tool Usage Evaluation Prototype")

    save_project_plan(project_plan, memory_dir=tmp_path)

    assert project_plan.plan_id
    assert project_plan.title == default_plan_title(project_plan)


def test_load_returns_saved_plan_with_identity(tmp_path) -> None:
    project_plan = _make_plan("Agentic AI Security Tool Usage Evaluation Prototype")
    save_project_plan(project_plan, memory_dir=tmp_path)

    loaded = load_project_plans(memory_dir=tmp_path)

    assert len(loaded) == 1
    assert loaded[0].plan_id == project_plan.plan_id
    assert loaded[0].title


def test_rename_updates_title_and_persists(tmp_path) -> None:
    project_plan = _make_plan("Agentic AI Security Tool Usage Evaluation Prototype")
    save_project_plan(project_plan, memory_dir=tmp_path)

    ok = rename_project_plan(project_plan.plan_id, "My renamed research plan", memory_dir=tmp_path)

    assert ok is True
    reloaded = load_project_plans(memory_dir=tmp_path)
    assert reloaded[0].title == "My renamed research plan"
    # Content is preserved, only the title changed.
    assert reloaded[0].idea == project_plan.idea
    assert reloaded[0].research_questions == project_plan.research_questions


def test_rename_missing_plan_returns_false(tmp_path) -> None:
    assert rename_project_plan("does-not-exist", "New title", memory_dir=tmp_path) is False


def test_rename_empty_title_returns_false(tmp_path) -> None:
    project_plan = _make_plan("Agentic AI Security Tool Usage Evaluation Prototype")
    save_project_plan(project_plan, memory_dir=tmp_path)

    assert rename_project_plan(project_plan.plan_id, "   ", memory_dir=tmp_path) is False


def test_search_finds_plan_after_rename(tmp_path) -> None:
    project_plan = _make_plan("Agentic AI Security Tool Usage Evaluation Prototype")
    save_project_plan(project_plan, memory_dir=tmp_path)
    rename_project_plan(project_plan.plan_id, "Security prototype plan", memory_dir=tmp_path)

    results = search_project_plans("security prototype", memory_dir=tmp_path)

    assert results
    assert results[0].plan_id == project_plan.plan_id


def test_delete_removes_only_target_plan(tmp_path) -> None:
    first = _make_plan("Agentic AI Security Tool Usage Evaluation Prototype")
    save_project_plan(first, memory_dir=tmp_path)
    second = _make_plan("Research design methodology for education technology")
    save_project_plan(second, memory_dir=tmp_path)

    ok = delete_project_plan(first.plan_id, memory_dir=tmp_path)

    assert ok is True
    remaining = load_project_plans(memory_dir=tmp_path)
    remaining_ids = {p.plan_id for p in remaining}
    assert first.plan_id not in remaining_ids
    assert second.plan_id in remaining_ids


def test_delete_missing_plan_returns_false(tmp_path) -> None:
    assert delete_project_plan("does-not-exist", memory_dir=tmp_path) is False


def test_delete_does_not_touch_other_plans(tmp_path) -> None:
    plans = [
        _make_plan("Agentic AI Security Tool Usage Evaluation Prototype"),
        _make_plan("Prompt injection risks in tool-using agents"),
        _make_plan("Evaluation criteria for research planning agents"),
    ]
    for project_plan in plans:
        save_project_plan(project_plan, memory_dir=tmp_path)

    delete_project_plan(plans[1].plan_id, memory_dir=tmp_path)

    remaining = load_project_plans(memory_dir=tmp_path)
    assert len(remaining) == 2
