from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

from ai_research_design_assistant.models import ProjectPlan


def export_project_plan(plan: ProjectPlan, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "research-plan.md").write_text(project_plan_to_markdown(plan), encoding="utf-8")
    (out_dir / "research-plan.json").write_text(project_plan_to_json(plan), encoding="utf-8")
    (out_dir / "research-plan.pdf").write_bytes(project_plan_to_pdf(plan))


def project_plan_to_markdown(plan: ProjectPlan) -> str:
    lines = [
        f"# Research Plan: {plan.topic_analysis.refined_topic}",
        "",
        "## Original Idea",
        "",
        plan.idea,
        "",
        "## Topic Analysis",
        "",
        f"- Refined topic: {plan.topic_analysis.refined_topic}",
        f"- Scope assessment: {plan.topic_analysis.scope_assessment}",
        "- Focus areas: " + ", ".join(plan.topic_analysis.detected_focus_areas),
        "",
        "### Narrowing Suggestions",
        "",
        *[f"- {item}" for item in plan.topic_analysis.narrowing_suggestions],
        "",
        "## Research Questions",
        "",
    ]
    for index, question in enumerate(plan.research_questions, start=1):
        lines.extend(
            [
                f"### RQ{index}: {question.question}",
                "",
                f"- Rationale: {question.rationale}",
                f"- Measurable outcome: {question.measurable_outcome}",
                "",
            ]
        )

    if plan.question_validations:
        lines.extend(["## Research Question Validation", ""])
        for index, validation in enumerate(plan.question_validations, start=1):
            lines.extend(
                [
                    f"### RQ{index} Validation",
                    "",
                    f"- Clarity: {validation.clarity}",
                    f"- Testability: {validation.testability}",
                    f"- Scope: {validation.scope}",
                    f"- Feasibility: {validation.feasibility}",
                    f"- Improvement suggestion: {validation.improvement_suggestion}",
                    "",
                ]
            )

    lines.extend(
        [
            "## Methodology",
            "",
            f"- Recommendation: {plan.methodology.name}",
            f"- Fit: {plan.methodology.fit}",
            "",
            "### Steps",
            "",
            *[f"- {step}" for step in plan.methodology.steps],
            "",
            "### Tools",
            "",
            *[f"- {tool}" for tool in plan.methodology.tools],
            "",
            "## Prototype",
            "",
            *[f"- {item}" for item in plan.prototype],
            "",
            "## Evaluation Criteria",
            "",
        ]
    )
    for criterion in plan.evaluation_criteria:
        lines.extend(
            [
                f"### {criterion.name}",
                "",
                f"- Description: {criterion.description}",
                f"- Measurement: {criterion.measurement}",
                "",
            ]
        )

    lines.extend(["## Risks", ""])
    for risk in plan.risks:
        lines.extend([f"- {risk.risk}", f"  Mitigation: {risk.mitigation}"])

    lines.extend(["", "## Checklist", ""])
    for item, passed in plan.checklist.items():
        marker = "x" if passed else " "
        lines.append(f"- [{marker}] {item.replace('_', ' ')}")

    lines.extend(["", "## Working Plan", ""])
    lines.extend(f"- {item}" for item in plan.sprint_plan)
    lines.extend(
        [
            "",
            "## Important Boundary",
            "",
            (
                "This output is a planning aid. It should be checked against course "
                "requirements, available time, data access and supervisor feedback."
            ),
        ]
    )
    return "\n".join(lines).strip() + "\n"


def project_plan_to_json(plan: ProjectPlan) -> str:
    return json.dumps(plan.model_dump(mode="json"), indent=2, ensure_ascii=False)


def project_plan_to_pdf(plan: ProjectPlan) -> bytes:
    lines = _pdf_lines(project_plan_to_markdown(plan))
    pages = [lines[index : index + 42] for index in range(0, len(lines), 42)] or [[]]
    objects: list[bytes] = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    page_refs = []
    next_object = 3

    for page_lines in pages:
        page_id = next_object
        content_id = next_object + 1
        next_object += 2
        page_refs.append(f"{page_id} 0 R")
        stream = _pdf_page_stream(page_lines)
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 "
                f"/BaseFont /Helvetica >> >> >> /Contents {content_id} 0 R >>"
            ).encode("latin-1")
        )
        objects.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
            + stream
            + b"\nendstream"
        )

    page_tree = f"<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {len(page_refs)} >>"
    objects.insert(1, page_tree.encode("latin-1"))
    return _build_pdf(objects)


def _pdf_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    for raw_line in markdown.splitlines():
        clean = re.sub(r"^#{1,6}\s*", "", raw_line)
        clean = clean.replace("**", "").replace("`", "")
        if not clean.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(clean, width=88) or [""])
    return lines


def _pdf_page_stream(lines: list[str]) -> bytes:
    commands = ["BT", "/F1 10 Tf", "50 800 Td", "14 TL"]
    for line in lines:
        commands.append(f"({_escape_pdf_text(line)}) Tj")
        commands.append("T*")
    commands.append("ET")
    return "\n".join(commands).encode("latin-1", errors="replace")


def _escape_pdf_text(text: str) -> str:
    return (
        text.encode("latin-1", errors="replace")
        .decode("latin-1")
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def _build_pdf(objects: list[bytes]) -> bytes:
    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, body in enumerate(objects, start=1):
        offsets.append(len(result))
        result.extend(f"{index} 0 obj\n".encode("latin-1"))
        result.extend(body)
        result.extend(b"\nendobj\n")

    xref_offset = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    result.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    result.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("latin-1")
    )
    return bytes(result)
