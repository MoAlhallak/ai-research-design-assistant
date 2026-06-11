from __future__ import annotations

from ai_research_design_assistant.models import ProjectPlan
from ai_research_design_assistant.planning import plan_project


def plan(idea: str) -> ProjectPlan:
    return plan_project(idea)
