from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx

from ai_research_design_assistant.models import ProjectPlan

DEFAULT_BASE_URL = "https://chat-ai.academiccloud.de/v1"
DEFAULT_MODEL = "qwen3-30b-a3b-instruct-2507"
DEFAULT_TIMEOUT_SECONDS = 180.0


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


async def generate_project_plan_with_llm(
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
    timeout_seconds = _read_timeout_seconds()
    payload = {
        "model": selected_model,
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a research design agent for student projects. You output a "
                    "single complete research plan as valid JSON that exactly matches the "
                    "given schema. Keep the topic realistic and measurable for a small "
                    "prototype. Do not add unsupported claims and do not add or remove keys."
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

    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        response = await client.post(
            f"{selected_base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        completion = response.json()

    content = completion["choices"][0]["message"]["content"]
    return ProjectPlan.model_validate(_parse_json_object(content))


def _read_timeout_seconds() -> float:
    raw = os.getenv("ACADEMIC_CLOUD_TIMEOUT")
    if not raw:
        return DEFAULT_TIMEOUT_SECONDS
    try:
        return float(raw)
    except ValueError:
        return DEFAULT_TIMEOUT_SECONDS


def _project_plan_prompt(plan: ProjectPlan) -> str:
    return f"""
Create the best possible structured research plan for this student project idea.

Idea:
{plan.idea}

Use the JSON below as the required schema and starting point. Return a JSON object with
exactly the same keys and nesting. Rewrite and improve every field so it genuinely fits
the idea: sharpen the refined topic, research questions, methodology, evaluation criteria
and risks. Keep the plan concise, realistic, measurable and suitable for a small student
prototype. Keep the "plan_id" and "title" values as given. Do not add or remove keys.

Structure JSON:
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
