from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx

from ai_research_design_assistant.models import ProjectPlan

DEFAULT_BASE_URL = "https://chat-ai.academiccloud.de/v1"
DEFAULT_MODEL = "qwen3.5-122b-a10b"


class LlmConfigError(RuntimeError):
    """Raised when LLM refinement was requested but is not configured."""


def llm_is_configured() -> bool:
    load_llm_environment()
    return bool(os.getenv("ACADEMIC_CLOUD_API_KEY"))


def load_llm_environment(env_path: str = ".env") -> None:
    if not os.path.exists(env_path):
        return
    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


async def refine_project_plan_with_llm(
    plan: ProjectPlan,
    model: str | None = None,
    base_url: str | None = None,
) -> ProjectPlan:
    load_llm_environment()
    api_key = os.getenv("ACADEMIC_CLOUD_API_KEY")
    if not api_key:
        raise LlmConfigError("ACADEMIC_CLOUD_API_KEY is not set.")

    selected_model = model or os.getenv("ACADEMIC_CLOUD_MODEL") or DEFAULT_MODEL
    selected_base_url = (base_url or os.getenv("ACADEMIC_CLOUD_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    payload = {
        "model": selected_model,
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You improve student research project plans. Return only valid JSON "
                    "matching the given schema. Keep the topic realistic and measurable. "
                    "Do not add unsupported claims."
                ),
            },
            {
                "role": "user",
                "content": _project_plan_prompt(plan),
            },
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{selected_base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        completion = response.json()

    content = completion["choices"][0]["message"]["content"]
    return ProjectPlan.model_validate(_parse_json_object(content))


async def refine_project_plan_with_fallback(
    plan: ProjectPlan,
    model: str | None = None,
    base_url: str | None = None,
) -> tuple[ProjectPlan, bool, str | None]:
    try:
        refined_plan = await refine_project_plan_with_llm(plan, model=model, base_url=base_url)
    except Exception as exc:
        return plan, False, str(exc)

    return refined_plan, True, None


def _project_plan_prompt(plan: ProjectPlan) -> str:
    return f"""
Improve this project plan for a student research prototype.

Return a JSON object with exactly the same structure as the input. Keep all keys.
Improve wording, research questions, methodology, evaluation and risks only when useful.
Keep the plan concise, realistic, measurable and suitable for a small prototype.

Input JSON:
{plan.model_dump_json(indent=2)}
""".strip()


def _parse_json_object(content: str) -> dict[str, Any]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if not match:
            raise
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object.")
    return parsed
