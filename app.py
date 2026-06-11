from __future__ import annotations

import asyncio
import html
from pathlib import Path

import streamlit as st

from ai_research_design_assistant.agent import plan as create_project_plan
from ai_research_design_assistant.exporters import (
    project_plan_to_json,
    project_plan_to_markdown,
    project_plan_to_pdf,
)
from ai_research_design_assistant.llm import llm_is_configured, refine_project_plan_with_fallback
from ai_research_design_assistant.memory import (
    find_similar_project_plans,
    load_project_plans,
    save_project_plan,
)
from ai_research_design_assistant.models import ProjectPlan, ResearchQuestion


OUTPUT_DIR = Path("outputs/student-project-plan")
DEFAULT_IDEA = (
    "I want to work on Agentic AI Security and Tool Usage "
    "and turn it into a realistic research project."
)


def main() -> None:
    st.set_page_config(
        page_title="Research Plan Assistant",
        page_icon="RP",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    _apply_theme()

    st.markdown(
        """
        <section class="hero">
            <div>
                <p class="eyebrow">AI Research Design Assistant</p>
                <h1>Turn a rough idea into a clear research plan.</h1>
                <p>
                    Enter a project idea. The assistant creates a focused topic, research
                    questions, methodology, evaluation criteria, risks and a working plan.
                </p>
            </div>
            <div class="hero-steps">
                <span>01 Topic</span>
                <span>02 Questions</span>
                <span>03 Method</span>
                <span>04 Export</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([0.92, 1.38], gap="large")

    with left:
        _render_input_panel()

    if st.session_state.get("generate_plan"):
        st.session_state["generate_plan"] = False
        _generate_plan()

    with right:
        plan = st.session_state.get("project_plan")
        if plan:
            _render_plan(plan)
        else:
            _render_empty_state()


def _render_input_panel() -> None:
    st.markdown(
        """
        <div class="panel-heading">
            <span>Input</span>
            <h2>Project Idea</h2>
            <p>A short description is enough for the first plan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "idea_input" not in st.session_state:
        st.session_state["idea_input"] = DEFAULT_IDEA

    st.text_area(
        "Project Idea",
        key="idea_input",
        height=190,
        label_visibility="collapsed",
    )

    col_example, col_generate = st.columns([0.42, 0.58], gap="small")
    with col_example:
        if st.button("Use example input", use_container_width=True):
            st.session_state["idea_input"] = DEFAULT_IDEA
            st.rerun()
    with col_generate:
        if st.button("Generate Plan", type="primary", use_container_width=True):
            st.session_state["generate_plan"] = True
            st.rerun()

    with st.expander("Optional LLM Improvement", expanded=False):
        if llm_is_configured():
            st.markdown(_status_badges(["LLM configured"]), unsafe_allow_html=True)
            st.caption(
                "The assistant will try to refine the generated plan with the configured "
                "Academic Cloud / SAIA model. If it fails, the local fallback is used."
            )
        else:
            st.markdown(_status_badges(["Local fallback active"]), unsafe_allow_html=True)
            st.caption(
                "No LLM configuration was found. The assistant still works offline with "
                "templates, rules and local memory."
            )

    previous_plans = load_project_plans()
    with st.expander("Memory", expanded=False):
        if previous_plans:
            selected = st.selectbox(
                "Load previous plan",
                options=list(range(len(previous_plans))),
                format_func=lambda index: previous_plans[index].topic_analysis.refined_topic,
            )
            if st.button("Load from Memory", use_container_width=True):
                st.session_state["project_plan"] = previous_plans[selected]
                st.session_state["similar_plans"] = []
                st.session_state["plan_status"] = "loaded"
                st.session_state["llm_warning"] = ""
                st.rerun()
        else:
            st.caption("No saved plans yet. Generated plans are saved locally after creation.")


def _generate_plan() -> None:
    idea = st.session_state.get("idea_input", "").strip()
    if not idea:
        st.error("Please enter a project idea first.")
        return

    with st.spinner("Generating research plan..."):
        project_plan = create_project_plan(idea)
        if llm_is_configured():
            project_plan, llm_ok, _ = asyncio.run(refine_project_plan_with_fallback(project_plan))
            st.session_state["llm_warning"] = (
                "" if llm_ok else "LLM unavailable or invalid response. Using local template fallback."
            )
        else:
            st.session_state["llm_warning"] = ""

        st.session_state["project_plan"] = project_plan
        _write_outputs(project_plan)
        st.session_state["similar_plans"] = find_similar_project_plans(idea)
        save_project_plan(project_plan)
        st.session_state["plan_status"] = "saved"


def _render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-state">
            <p class="eyebrow">Final Output</p>
            <h2>No plan generated yet</h2>
            <p>
                After clicking <strong>Generate Plan</strong>, the structured research plan
                will appear here.
            </p>
            <div class="preview-grid">
                <span>Topic Analysis</span>
                <span>Research Questions</span>
                <span>Question Validation</span>
                <span>Methodology</span>
                <span>Evaluation</span>
                <span>Export</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_plan(plan: ProjectPlan) -> None:
    similar_plans = st.session_state.get("similar_plans") or []
    plan_status = st.session_state.get("plan_status")
    llm_warning = st.session_state.get("llm_warning")
    statuses = ["Plan generated", "Export ready"]
    statuses.append("Loaded from memory" if plan_status == "loaded" else "Saved to memory")
    if llm_warning:
        statuses.append("LLM fallback used")
    if plan_status != "loaded" and similar_plans:
        statuses.append(f"{len(similar_plans)} similar plan(s)")

    st.markdown(
        """
        <div class="result-header">
            <div>
                <p class="eyebrow">Final Output</p>
                <h2>Research Plan</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(_status_badges(statuses), unsafe_allow_html=True)
    if llm_warning:
        st.warning(llm_warning)

    overview_tab, questions_tab, validation_tab, methodology_tab, export_tab = st.tabs(
        ["Overview", "Questions", "Validation", "Methodology", "Export"]
    )

    with overview_tab:
        st.markdown('<div class="section-title">Topic Analysis</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="topic-card">
                <span>Focused Topic</span>
                <h3>{_escape_html(plan.topic_analysis.refined_topic)}</h3>
                <p>{_escape_html(plan.topic_analysis.scope_assessment)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-title">Focus Areas</div>', unsafe_allow_html=True)
        st.markdown(_badge_row(plan.topic_analysis.detected_focus_areas), unsafe_allow_html=True)
        st.markdown('<div class="section-title">Working Plan</div>', unsafe_allow_html=True)
        st.markdown(_check_list(plan.sprint_plan), unsafe_allow_html=True)

    with questions_tab:
        st.markdown('<div class="section-title">Research Questions</div>', unsafe_allow_html=True)
        for index, question in enumerate(plan.research_questions, start=1):
            st.markdown(_question_card(index, question), unsafe_allow_html=True)

    with validation_tab:
        st.markdown('<div class="section-title">Question Validation</div>', unsafe_allow_html=True)
        if plan.question_validations:
            st.table(_validation_rows(plan))
        else:
            st.info("No question validation available for this plan.")

    with methodology_tab:
        st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="info-card">
                <span>Recommended Approach</span>
                <h3>{_escape_html(plan.methodology.name)}</h3>
                <p>{_escape_html(plan.methodology.fit)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-title">Methodology Steps</div>', unsafe_allow_html=True)
        st.markdown(_check_list(plan.methodology.steps), unsafe_allow_html=True)
        st.markdown('<div class="section-title">Evaluation</div>', unsafe_allow_html=True)
        st.markdown(
            _key_value_list(
                [(criterion.name, criterion.description) for criterion in plan.evaluation_criteria]
            ),
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-title">Risks</div>', unsafe_allow_html=True)
        st.markdown(
            _key_value_list([(risk.risk, risk.mitigation) for risk in plan.risks]),
            unsafe_allow_html=True,
        )

    with export_tab:
        _render_export_section(plan)


def _render_export_section(plan: ProjectPlan) -> None:
    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="export-card">
            <span>Export ready</span>
            <h3>Download your generated research plan</h3>
            <p>Use these files for documentation, submission drafts or further review.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    markdown_text = project_plan_to_markdown(plan)
    json_text = project_plan_to_json(plan)
    pdf_bytes = project_plan_to_pdf(plan)
    col_a, col_b, col_c = st.columns(3)
    col_a.download_button(
        "Markdown",
        data=markdown_text.encode("utf-8"),
        file_name="research-plan.md",
        mime="text/markdown",
        use_container_width=True,
    )
    col_b.download_button(
        "JSON",
        data=json_text.encode("utf-8"),
        file_name="research-plan.json",
        mime="application/json",
        use_container_width=True,
    )
    col_c.download_button(
        "PDF",
        data=pdf_bytes,
        file_name="research-plan.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


def _write_outputs(plan: ProjectPlan) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "research-plan.md").write_text(project_plan_to_markdown(plan), encoding="utf-8")
    (OUTPUT_DIR / "research-plan.json").write_text(project_plan_to_json(plan), encoding="utf-8")
    (OUTPUT_DIR / "research-plan.pdf").write_bytes(project_plan_to_pdf(plan))


def _question_card(index: int, question: ResearchQuestion) -> str:
    return f"""
    <div class="question-card">
        <div class="question-card-header">
            <span>RQ{index}</span>
            <h3>{_escape_html(question.question)}</h3>
        </div>
        <div class="question-grid">
            <div>
                <strong>Reason</strong>
                <p>{_escape_html(question.rationale)}</p>
            </div>
            <div>
                <strong>Measurable Outcome</strong>
                <p>{_escape_html(question.measurable_outcome)}</p>
            </div>
        </div>
    </div>
    """


def _validation_rows(plan: ProjectPlan) -> list[dict[str, str]]:
    return [
        {
            "RQ": f"RQ{index}",
            "Clarity": validation.clarity,
            "Testability": validation.testability,
            "Scope": validation.scope,
            "Feasibility": validation.feasibility,
            "Improvement suggestion": validation.improvement_suggestion,
        }
        for index, validation in enumerate(plan.question_validations, start=1)
    ]


def _status_badges(items: list[str]) -> str:
    return (
        '<div class="status-row">'
        + "".join(f"<span>{_escape_html(item)}</span>" for item in items)
        + "</div>"
    )


def _badge_row(items: list[str]) -> str:
    return (
        '<div class="badges">'
        + "".join(f"<span>{_escape_html(item)}</span>" for item in items)
        + "</div>"
    )


def _check_list(items: list[str]) -> str:
    return (
        '<div class="clean-list">'
        + "".join(f"<div><span></span><p>{_escape_html(item)}</p></div>" for item in items)
        + "</div>"
    )


def _key_value_list(items: list[tuple[str, str]]) -> str:
    return (
        '<div class="kv-list">'
        + "".join(
            f"<div><strong>{_escape_html(key)}</strong><p>{_escape_html(value)}</p></div>"
            for key, value in items
        )
        + "</div>"
    )


def _escape_html(value: str) -> str:
    return html.escape(value, quote=True)


def _apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f5f7fb;
            --surface: #ffffff;
            --ink: #1f2933;
            --muted: #667085;
            --accent: #0f766e;
            --accent-dark: #134e4a;
            --line: #e3e8ef;
            --soft: #e9f7f5;
            --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            --shadow-soft: 0 10px 25px rgba(15, 23, 42, 0.06);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15,118,110,0.12), transparent 34rem),
                radial-gradient(circle at top right, rgba(37,99,235,0.10), transparent 30rem),
                var(--bg);
            color: var(--ink);
        }

        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        .hero,
        .panel-heading,
        .empty-state,
        .result-header,
        .topic-card,
        .info-card,
        .question-card,
        .export-card {
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.92);
            box-shadow: var(--shadow-soft);
        }

        .hero {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 1.5rem;
            padding: 1.75rem 1.9rem;
            margin-bottom: 1.35rem;
            border-radius: 18px;
            box-shadow: var(--shadow);
        }

        .hero h1 {
            max-width: 760px;
            margin: 0.15rem 0 0.5rem 0;
            font-size: 2.2rem;
            line-height: 1.14;
            letter-spacing: 0;
        }

        .hero p,
        .panel-heading p,
        .topic-card p,
        .info-card p,
        .export-card p,
        .question-card p,
        .kv-list p,
        .clean-list p {
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.55;
        }

        .hero-steps {
            display: grid;
            grid-template-columns: repeat(2, minmax(108px, 1fr));
            gap: 0.55rem;
            min-width: 250px;
        }

        .hero-steps span,
        .preview-grid span,
        .badges span,
        .status-row span,
        .question-card-header span {
            display: inline-flex;
            align-items: center;
            border: 1px solid var(--line);
            background: var(--soft);
            color: var(--accent-dark);
            font-weight: 800;
        }

        .hero-steps span {
            padding: 0.75rem 0.85rem;
            border-radius: 14px;
        }

        .eyebrow,
        .panel-heading span,
        .topic-card span,
        .info-card span,
        .export-card span {
            margin: 0;
            color: var(--accent-dark) !important;
            font-size: 0.78rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .panel-heading {
            margin-bottom: 0.75rem;
            padding: 1rem 1.05rem;
            border-radius: 14px;
        }

        .panel-heading h2 {
            margin: 0.15rem 0 0.2rem 0;
            font-size: 1.25rem;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 14px;
            border-color: var(--line);
            background: var(--surface);
            font-size: 1rem;
            line-height: 1.5;
            box-shadow: var(--shadow-soft);
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 14px;
            border: 1px solid var(--accent);
            font-weight: 750;
            min-height: 2.85rem;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--accent), #0d9488);
            border-color: var(--accent);
            box-shadow: 0 10px 22px rgba(15,118,110,0.24);
        }

        .empty-state {
            min-height: 430px;
            border-radius: 16px;
            padding: 1.35rem;
        }

        .empty-state h2,
        .result-header h2,
        .topic-card h3,
        .info-card h3,
        .export-card h3 {
            color: var(--ink);
            letter-spacing: 0;
        }

        .preview-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.6rem;
            margin-top: 1rem;
        }

        .preview-grid span,
        .badges span,
        .status-row span {
            border-radius: 999px;
            padding: 0.45rem 0.7rem;
        }

        .result-header {
            border-radius: 16px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.65rem;
        }

        .result-header h2 {
            margin: 0.1rem 0 0 0;
            font-size: 1.35rem;
        }

        .status-row,
        .badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.55rem 0 1rem 0;
        }

        .topic-card,
        .info-card,
        .export-card,
        .question-card {
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.85rem;
        }

        .topic-card {
            background:
                linear-gradient(135deg, rgba(15,118,110,0.10), rgba(255,255,255,0.96)),
                var(--surface);
        }

        .topic-card h3,
        .info-card h3,
        .export-card h3 {
            margin: 0.35rem 0 0.45rem 0;
            font-size: 1.12rem;
            line-height: 1.3;
        }

        .section-title {
            margin: 1rem 0 0.55rem 0;
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 850;
        }

        .question-card-header {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            margin-bottom: 0.8rem;
        }

        .question-card-header span {
            border-radius: 999px;
            padding: 0.35rem 0.58rem;
            flex: 0 0 auto;
            font-size: 0.86rem;
        }

        .question-card-header h3 {
            margin: 0;
            color: var(--ink);
            font-size: 1rem;
            line-height: 1.45;
        }

        .question-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.65rem;
        }

        .question-grid div,
        .clean-list div,
        .kv-list div {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: rgba(255,255,255,0.86);
        }

        .question-grid div {
            padding: 0.75rem;
        }

        .question-grid strong,
        .kv-list strong {
            display: block;
            margin-bottom: 0.25rem;
            color: var(--ink);
        }

        .clean-list,
        .kv-list {
            display: grid;
            gap: 0.55rem;
            margin-bottom: 0.85rem;
        }

        .clean-list div {
            display: flex;
            gap: 0.7rem;
            align-items: flex-start;
            padding: 0.72rem 0.8rem;
        }

        .clean-list span {
            width: 0.55rem;
            height: 0.55rem;
            margin-top: 0.45rem;
            border-radius: 999px;
            background: var(--accent);
            flex: 0 0 auto;
        }

        .kv-list div {
            padding: 0.82rem 0.9rem;
        }

        div[data-testid="stExpander"] {
            border-radius: 14px;
            border-color: var(--line);
            background: var(--surface);
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
            margin-bottom: 0.7rem;
        }

        div[data-testid="stTabs"] button {
            font-size: 0.95rem;
            font-weight: 750;
        }

        div[data-testid="stTable"] {
            font-size: 0.96rem;
        }

        @media (max-width: 760px) {
            .hero {
                flex-direction: column;
                align-items: stretch;
            }
            .hero h1 {
                font-size: 1.55rem;
            }
            .hero-steps,
            .question-grid,
            .preview-grid {
                grid-template-columns: 1fr;
                min-width: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
