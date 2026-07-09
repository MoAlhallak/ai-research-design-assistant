from __future__ import annotations

# ruff: noqa: E402

import asyncio
import html
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ai_research_design_assistant.agent import plan as create_project_plan  # noqa: E402
from ai_research_design_assistant.exporters import (
    project_plan_to_json,
    project_plan_to_markdown,
    project_plan_to_pdf,
)  # noqa: E402
from ai_research_design_assistant.llm import (  # noqa: E402
    generate_project_plan_with_llm,
)
from ai_research_design_assistant.memory import (
    compare_project_plans,
    delete_project_plan,
    find_similar_project_plans,
    load_project_plans,
    rename_project_plan,
    save_project_plan,
    search_project_plans,
)  # noqa: E402
from ai_research_design_assistant.models import (  # noqa: E402
    MethodologyAdvice,
    ProjectPlan,
    ResearchQuestion,
)


OUTPUT_DIR = Path("outputs/student-project-plan")
EXAMPLE_IDEAS = {
    "Deutsch": (
        "Ich möchte zu Agentic AI Security und Tool-Nutzung arbeiten "
        "und daraus ein realistisches Forschungsprojekt machen."
    ),
    "English": (
        "I want to work on Agentic AI Security and Tool Usage "
        "and turn it into a realistic research project."
    ),
}

UI_TEXT = {
    "Deutsch": {
        "app_title": "AI Research Design Assistant",
        "hero_title": "Aus einer groben Idee wird ein klarer Forschungsplan.",
        "hero_body": (
            "Gib eine Projektidee ein. Der Assistant erstellt ein eingegrenztes Thema, "
            "Forschungsfragen, Methodik, Evaluationskriterien, Risiken und einen Arbeitsplan."
        ),
        "step_topic": "01 Thema",
        "step_questions": "02 Fragen",
        "step_method": "03 Methodik",
        "step_export": "04 Export",
        "history": "Planverlauf",
        "history_caption": "Öffne eine frühere Projektidee und den kompletten Forschungsplan.",
        "language": "Sprache",
        "new_plan": "Neuer Plan",
        "search_history": "Verlauf durchsuchen",
        "search_history_placeholder": "Projektideen suchen",
        "recent_plans": "Letzte Pläne",
        "no_saved_plans": "Noch keine gespeicherten Pläne.",
        "rename": "Umbenennen",
        "delete": "Löschen",
        "rename_plan": "Plan umbenennen",
        "new_title": "Neuer Titel",
        "new_title_placeholder": "Kurzer, sprechender Titel",
        "save_rename": "Titel speichern",
        "cancel": "Abbrechen",
        "confirm_delete_question": "Diesen Plan wirklich löschen?",
        "confirm_delete": "Löschen bestätigen",
        "plan_renamed": "Plan umbenannt.",
        "plan_deleted": "Plan gelöscht.",
        "empty_title_warning": "Bitte einen Titel eingeben.",
        "input": "Eingabe",
        "project_idea": "Projektidee",
        "input_help": "Eine kurze Beschreibung reicht für den ersten Plan.",
        "use_example": "Beispiel nutzen",
        "generate_plan": "Plan erstellen",
        "empty_title": "Noch kein Plan erstellt",
        "empty_body": (
            "Nach dem Klick auf <strong>Plan erstellen</strong> erscheint hier der "
            "strukturierte Forschungsplan."
        ),
        "final_output": "Fertiger Output",
        "research_plan": "Forschungsplan",
        "topic_analysis": "Themenanalyse",
        "focus_areas": "Fokusbereiche",
        "working_plan": "Arbeitsplan",
        "questions": "Forschungsfragen",
        "question_validation": "Fragenvalidierung",
        "methodology": "Methodik",
        "methodology_advisor": "Methodik-Berater",
        "evaluation": "Evaluation",
        "evaluation_builder": "Evaluations-Builder",
        "risk_matrix": "Risikomatrix",
        "memory": "Memory",
        "export": "Export",
        "overview": "Überblick",
        "plan_generated": "Plan erstellt",
        "export_ready": "Export bereit",
        "saved_to_memory": "In Memory gespeichert",
        "loaded_from_memory": "Aus Memory geladen",
        "similar_plans": "ähnliche Pläne",
        "focused_topic": "Eingegrenztes Thema",
        "primary_recommendation": "Primäre Empfehlung",
        "reason": "Begründung",
        "measurable_outcome": "Messbares Ergebnis",
        "validation_caption": "Öffne eine Frage darunter, um die Begründung je Bewertung zu sehen.",
        "no_validation": "Keine Fragenvalidierung für diesen Plan verfügbar.",
        "validation_expander": "RQ{index} Validierung erklärt",
        "question": "Frage",
        "clarity": "Klarheit",
        "testability": "Testbarkeit",
        "scope": "Umfang",
        "feasibility": "Machbarkeit",
        "improvement": "Verbesserungsvorschlag",
        "criterion": "Kriterium",
        "description": "Beschreibung",
        "how_to_measure": "Messung",
        "expected_evidence": "Erwarteter Nachweis",
        "priority": "Priorität",
        "risk": "Risiko",
        "probability": "Wahrscheinlichkeit",
        "impact": "Auswirkung",
        "mitigation": "Gegenmaßnahme",
        "export_title": "Forschungsplan herunterladen",
        "export_body": "Nutze diese Dateien für Dokumentation, Abgabeentwurf oder Review.",
        "local_memory": "Lokale Projekt-Memory",
        "memory_title": "Frühere Pläne suchen, laden und vergleichen",
        "memory_body": "Memory nutzt lokale JSON-Dateien und den ChromaDB-Prototyp-Fallback.",
        "search_saved": "Gespeicherte Pläne per Keyword suchen",
        "search_saved_placeholder": "security, prototype, evaluation",
        "saved_plans": "Gespeicherte Pläne",
        "load_selected": "Ausgewählten Plan laden",
        "compare_current": "Mit aktuellem Plan vergleichen",
        "no_search_results": "Keine gespeicherten Pläne gefunden.",
        "recent_saved": "Letzte gespeicherte Pläne",
        "plan_comparison": "Planvergleich",
        "aspect": "Aspekt",
        "result": "Ergebnis",
        "same_focus": "Gleiche Fokusbereiche",
        "different_focus": "Andere Fokusbereiche",
        "similar_methodology": "Ähnliche Methodik",
        "changed_questions": "Geänderte Forschungsfragen",
        "recommendation": "Empfehlung",
        "not_specified": "Nicht angegeben.",
        "generating": "Forschungsplan wird erstellt...",
        "empty_idea": "Bitte zuerst eine Projektidee eingeben.",
        "why_it_fits": "Warum es passt",
        "required_steps": "Notwendige Schritte",
        "required_artifacts": "Notwendige Daten oder Artefakte",
        "limitations": "Mögliche Grenzen",
        "llm_error_eyebrow": "Fehler",
        "llm_error_title": "Plan konnte nicht erstellt werden",
        "llm_error_body": (
            "Das LLM (Academic Cloud / SAIA) wurde nicht erreicht. Prüfe den API-Key in "
            "der .env-Datei und die Verbindung und versuche es erneut."
        ),
    },
    "English": {
        "app_title": "AI Research Design Assistant",
        "hero_title": "Turn a rough idea into a clear research plan.",
        "hero_body": (
            "Enter a project idea. The assistant creates a focused topic, research "
            "questions, methodology, evaluation criteria, risks and a working plan."
        ),
        "step_topic": "01 Topic",
        "step_questions": "02 Questions",
        "step_method": "03 Method",
        "step_export": "04 Export",
        "history": "Plan History",
        "history_caption": "Open an earlier project idea and its complete research plan.",
        "language": "Language",
        "new_plan": "New Plan",
        "search_history": "Search history",
        "search_history_placeholder": "Search project ideas",
        "recent_plans": "Recent plans",
        "no_saved_plans": "No saved plans yet.",
        "rename": "Rename",
        "delete": "Delete",
        "rename_plan": "Rename plan",
        "new_title": "New title",
        "new_title_placeholder": "Short, readable title",
        "save_rename": "Save title",
        "cancel": "Cancel",
        "confirm_delete_question": "Delete this plan?",
        "confirm_delete": "Confirm delete",
        "plan_renamed": "Plan renamed.",
        "plan_deleted": "Plan deleted.",
        "empty_title_warning": "Please enter a title.",
        "input": "Input",
        "project_idea": "Project Idea",
        "input_help": "A short description is enough for the first plan.",
        "use_example": "Use example input",
        "generate_plan": "Generate Plan",
        "empty_title": "No plan generated yet",
        "empty_body": (
            "After clicking <strong>Generate Plan</strong>, the structured research plan "
            "will appear here."
        ),
        "final_output": "Final Output",
        "research_plan": "Research Plan",
        "topic_analysis": "Topic Analysis",
        "focus_areas": "Focus Areas",
        "working_plan": "Working Plan",
        "questions": "Research Questions",
        "question_validation": "Question Validation",
        "methodology": "Methodology",
        "methodology_advisor": "Methodology Advisor",
        "evaluation": "Evaluation",
        "evaluation_builder": "Evaluation Builder",
        "risk_matrix": "Risk Matrix",
        "memory": "Memory",
        "export": "Export",
        "overview": "Overview",
        "plan_generated": "Plan generated",
        "export_ready": "Export ready",
        "saved_to_memory": "Saved to memory",
        "loaded_from_memory": "Loaded from memory",
        "similar_plans": "similar plan(s)",
        "focused_topic": "Focused Topic",
        "primary_recommendation": "Primary recommendation",
        "reason": "Reason",
        "measurable_outcome": "Measurable Outcome",
        "validation_caption": "Open a question below to see why each rating was assigned.",
        "no_validation": "No question validation available for this plan.",
        "validation_expander": "RQ{index} validation explanation",
        "question": "Question",
        "clarity": "Clarity",
        "testability": "Testability",
        "scope": "Scope",
        "feasibility": "Feasibility",
        "improvement": "Improvement suggestion",
        "criterion": "Criterion",
        "description": "Description",
        "how_to_measure": "How to measure",
        "expected_evidence": "Expected evidence",
        "priority": "Priority",
        "risk": "Risk",
        "probability": "Probability",
        "impact": "Impact",
        "mitigation": "Mitigation",
        "export_title": "Download your generated research plan",
        "export_body": "Use these files for documentation, submission drafts or further review.",
        "local_memory": "Local project memory",
        "memory_title": "Search, load and compare previous plans",
        "memory_body": "Memory uses local JSON files and the ChromaDB prototype fallback.",
        "search_saved": "Search saved plans by keyword",
        "search_saved_placeholder": "security, prototype, evaluation",
        "saved_plans": "Saved plans",
        "load_selected": "Load selected plan",
        "compare_current": "Compare with current plan",
        "no_search_results": "No saved plans found yet.",
        "recent_saved": "Recent saved plans",
        "plan_comparison": "Plan Comparison",
        "aspect": "Aspect",
        "result": "Result",
        "same_focus": "Same focus areas",
        "different_focus": "Different focus areas",
        "similar_methodology": "Similar methodology",
        "changed_questions": "Changed research questions",
        "recommendation": "Recommendation",
        "not_specified": "Not specified.",
        "generating": "Generating research plan...",
        "empty_idea": "Please enter a project idea first.",
        "why_it_fits": "Why it fits",
        "required_steps": "Required steps",
        "required_artifacts": "Required data or artifacts",
        "limitations": "Possible limitations",
        "llm_error_eyebrow": "Error",
        "llm_error_title": "Plan could not be generated",
        "llm_error_body": (
            "The LLM (Academic Cloud / SAIA) could not be reached. Check the API key in "
            "the .env file and your connection, then try again."
        ),
    },
}


def _current_language() -> str:
    return st.session_state.get("ui_language", "Deutsch")


def _t(key: str, language: str | None = None) -> str:
    selected_language = language or _current_language()
    return UI_TEXT.get(selected_language, UI_TEXT["Deutsch"]).get(key, key)


def main() -> None:
    st.set_page_config(
        page_title="AI Research Design Assistant",
        page_icon="🧭",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _apply_theme()
    _render_history_sidebar()

    st.markdown(
        """
        <section class="hero">
            <div>
                <p class="eyebrow">{app_title}</p>
                <h1>{hero_title}</h1>
                <p>
                    {hero_body}
                </p>
            </div>
            <div class="hero-steps">
                <span>{step_topic}</span>
                <span>{step_questions}</span>
                <span>{step_method}</span>
                <span>{step_export}</span>
            </div>
        </section>
        """.format(
            app_title=_escape_html(_t("app_title")),
            hero_title=_escape_html(_t("hero_title")),
            hero_body=_escape_html(_t("hero_body")),
            step_topic=_escape_html(_t("step_topic")),
            step_questions=_escape_html(_t("step_questions")),
            step_method=_escape_html(_t("step_method")),
            step_export=_escape_html(_t("step_export")),
        ),
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
        elif st.session_state.get("plan_error"):
            _render_error_state(st.session_state["plan_error"])
        else:
            _render_empty_state()


def _reset_workspace() -> None:
    for key in ("project_plan", "similar_plans", "plan_status", "memory_comparison", "plan_error"):
        st.session_state.pop(key, None)
    st.session_state["idea_input"] = ""


def _render_history_sidebar() -> None:
    with st.sidebar:
        language = st.selectbox(
            "Sprache / Language",
            options=["Deutsch", "English"],
            key="ui_language",
        )
        st.markdown(f"## {_t('history', language)}")
        st.caption(_t("history_caption", language))

        flash = st.session_state.pop("history_flash", None)
        if flash:
            st.success(flash)

        if st.button(_t("new_plan", language), type="primary", use_container_width=True):
            _reset_workspace()
            st.session_state.pop("rename_target", None)
            st.session_state.pop("delete_target", None)
            st.rerun()

        query = st.text_input(
            _t("search_history", language),
            key="history_search",
            placeholder=_t("search_history_placeholder", language),
        )
        history = search_project_plans(query, limit=20) if query else load_project_plans()[:20]

        if not history:
            st.info(_t("no_saved_plans", language))
            return

        st.markdown(
            f'<p class="history-heading">{_escape_html(_t("recent_plans", language))}</p>',
            unsafe_allow_html=True,
        )
        for saved_plan in history:
            _render_history_entry(saved_plan, language)


def _render_history_entry(saved_plan: ProjectPlan, language: str) -> None:
    plan_id = saved_plan.plan_id
    title = saved_plan.title or _history_title(saved_plan.idea)

    open_col, rename_col, delete_col = st.columns([0.7, 0.15, 0.15])
    if open_col.button(
        _history_title(title),
        key=f"open_{plan_id}",
        help=saved_plan.topic_analysis.refined_topic,
        use_container_width=True,
    ):
        st.session_state["project_plan"] = saved_plan
        st.session_state["idea_input"] = saved_plan.idea
        st.session_state["similar_plans"] = []
        st.session_state["plan_status"] = "loaded"
        st.session_state["memory_comparison"] = None
        st.session_state.pop("plan_error", None)
        st.session_state.pop("rename_target", None)
        st.session_state.pop("delete_target", None)
        st.rerun()
    if rename_col.button("✏️", key=f"rename_btn_{plan_id}", help=_t("rename", language)):
        toggled = None if st.session_state.get("rename_target") == plan_id else plan_id
        st.session_state["rename_target"] = toggled
        st.session_state.pop("delete_target", None)
        st.rerun()
    if delete_col.button("🗑️", key=f"delete_btn_{plan_id}", help=_t("delete", language)):
        toggled = None if st.session_state.get("delete_target") == plan_id else plan_id
        st.session_state["delete_target"] = toggled
        st.session_state.pop("rename_target", None)
        st.rerun()

    if st.session_state.get("rename_target") == plan_id:
        _render_rename_form(saved_plan, language)
    if st.session_state.get("delete_target") == plan_id:
        _render_delete_confirm(saved_plan, language)


def _render_rename_form(saved_plan: ProjectPlan, language: str) -> None:
    plan_id = saved_plan.plan_id
    new_title = st.text_input(
        _t("new_title", language),
        value=saved_plan.title,
        key=f"rename_input_{plan_id}",
        placeholder=_t("new_title_placeholder", language),
    )
    save_col, cancel_col = st.columns(2)
    if save_col.button(_t("save_rename", language), key=f"rename_save_{plan_id}", use_container_width=True):
        if not new_title.strip():
            st.warning(_t("empty_title_warning", language))
        elif rename_project_plan(plan_id, new_title):
            open_plan = st.session_state.get("project_plan")
            if open_plan is not None and getattr(open_plan, "plan_id", "") == plan_id:
                open_plan.title = " ".join(new_title.split())
            st.session_state.pop("rename_target", None)
            st.session_state["history_flash"] = _t("plan_renamed", language)
            st.rerun()
    if cancel_col.button(_t("cancel", language), key=f"rename_cancel_{plan_id}", use_container_width=True):
        st.session_state.pop("rename_target", None)
        st.rerun()


def _render_delete_confirm(saved_plan: ProjectPlan, language: str) -> None:
    plan_id = saved_plan.plan_id
    st.warning(_t("confirm_delete_question", language))
    confirm_col, cancel_col = st.columns(2)
    if confirm_col.button(
        _t("confirm_delete", language),
        key=f"delete_confirm_{plan_id}",
        type="primary",
        use_container_width=True,
    ):
        if delete_project_plan(plan_id):
            open_plan = st.session_state.get("project_plan")
            if open_plan is not None and getattr(open_plan, "plan_id", "") == plan_id:
                _reset_workspace()
            st.session_state.pop("delete_target", None)
            st.session_state["history_flash"] = _t("plan_deleted", language)
            st.rerun()
    if cancel_col.button(_t("cancel", language), key=f"delete_cancel_{plan_id}", use_container_width=True):
        st.session_state.pop("delete_target", None)
        st.rerun()


def _render_input_panel() -> None:
    st.markdown(
        f"""
        <div class="panel-heading">
            <span>{_escape_html(_t("input"))}</span>
            <h2>{_escape_html(_t("project_idea"))}</h2>
            <p>{_escape_html(_t("input_help"))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "idea_input" not in st.session_state:
        st.session_state["idea_input"] = EXAMPLE_IDEAS[_current_language()]

    st.text_area(
        _t("project_idea"),
        key="idea_input",
        height=190,
        label_visibility="collapsed",
    )

    col_example, col_generate = st.columns([0.42, 0.58], gap="small")
    with col_example:
        st.button(
            _t("use_example"),
            on_click=_use_example_input,
            use_container_width=True,
        )
    with col_generate:
        if st.button(_t("generate_plan"), type="primary", use_container_width=True):
            st.session_state["generate_plan"] = True
            st.rerun()


def _use_example_input() -> None:
    st.session_state["idea_input"] = EXAMPLE_IDEAS[_current_language()]


def _generate_plan() -> None:
    idea = st.session_state.get("idea_input", "").strip()
    if not idea:
        st.error(_t("empty_idea"))
        return

    with st.spinner(_t("generating")):
        scaffold = create_project_plan(idea)
        try:
            project_plan = asyncio.run(generate_project_plan_with_llm(scaffold))
        except Exception as exc:  # noqa: BLE001
            st.session_state["plan_error"] = str(exc)
            st.session_state.pop("project_plan", None)
            st.session_state.pop("similar_plans", None)
            st.session_state.pop("plan_status", None)
            st.rerun()
            return

        st.session_state.pop("plan_error", None)
        st.session_state["project_plan"] = project_plan
        _write_outputs(project_plan)
        st.session_state["similar_plans"] = find_similar_project_plans(idea)
        save_project_plan(project_plan)
        st.session_state["plan_status"] = "saved"
        st.rerun()


def _render_empty_state() -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <p class="eyebrow">{_escape_html(_t("final_output"))}</p>
            <h2>{_escape_html(_t("empty_title"))}</h2>
            <p>
                {_t("empty_body")}
            </p>
            <div class="preview-grid">
                <span>{_escape_html(_t("topic_analysis"))}</span>
                <span>{_escape_html(_t("questions"))}</span>
                <span>{_escape_html(_t("question_validation"))}</span>
                <span>{_escape_html(_t("methodology"))}</span>
                <span>{_escape_html(_t("evaluation"))}</span>
                <span>{_escape_html(_t("export"))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_error_state(error: str) -> None:
    st.markdown(
        f"""
        <div class="error-state">
            <p class="eyebrow">{_escape_html(_t("llm_error_eyebrow"))}</p>
            <h2>{_escape_html(_t("llm_error_title"))}</h2>
            <p>{_escape_html(_t("llm_error_body"))}</p>
            <pre>{_escape_html(error)}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_plan(plan: ProjectPlan) -> None:
    similar_plans = st.session_state.get("similar_plans") or []
    plan_status = st.session_state.get("plan_status")
    statuses = [_t("plan_generated"), _t("export_ready")]
    statuses.append(_t("loaded_from_memory") if plan_status == "loaded" else _t("saved_to_memory"))
    if plan_status != "loaded" and similar_plans:
        statuses.append(f"{len(similar_plans)} {_t('similar_plans')}")

    st.markdown(
        f"""
        <div class="result-header">
            <div>
                <p class="eyebrow">{_escape_html(_t("final_output"))}</p>
                <h2>{_escape_html(_t("research_plan"))}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(_status_badges(statuses), unsafe_allow_html=True)

    (
        overview_tab,
        questions_tab,
        methodology_advisor_tab,
        evaluation_builder_tab,
        risk_matrix_tab,
        memory_tab,
        export_tab,
    ) = st.tabs(
        [
            _t("overview"),
            _t("questions"),
            _t("methodology_advisor"),
            _t("evaluation_builder"),
            _t("risk_matrix"),
            _t("memory"),
            _t("export"),
        ]
    )

    with overview_tab:
        st.markdown(_section_title("topic_analysis"), unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="topic-card">
                <span>{_escape_html(_t("focused_topic"))}</span>
                <h3>{_escape_html(plan.topic_analysis.refined_topic)}</h3>
                <p>{_escape_html(plan.topic_analysis.scope_assessment)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(_section_title("focus_areas"), unsafe_allow_html=True)
        st.markdown(_badge_row(plan.topic_analysis.detected_focus_areas), unsafe_allow_html=True)
        st.markdown(_section_title("working_plan"), unsafe_allow_html=True)
        st.markdown(_check_list(plan.sprint_plan), unsafe_allow_html=True)

    with questions_tab:
        st.markdown(_section_title("questions"), unsafe_allow_html=True)
        for index, question in enumerate(plan.research_questions, start=1):
            st.markdown(_question_card(index, question), unsafe_allow_html=True)
        st.markdown(_section_title("question_validation"), unsafe_allow_html=True)
        if plan.question_validations:
            st.table(_validation_rows(plan))
            st.caption(_t("validation_caption"))
            _render_validation_explanations(plan)
        else:
            st.info(_t("no_validation"))

    with methodology_advisor_tab:
        st.markdown(_section_title("methodology_advisor"), unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="info-card">
                <span>{_escape_html(_t("primary_recommendation"))}</span>
                <h3>{_escape_html(plan.methodology.name)}</h3>
                <p>{_escape_html(plan.methodology.fit)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for method in plan.methodology_advice:
            st.markdown(_method_card(method), unsafe_allow_html=True)

    with evaluation_builder_tab:
        st.markdown(_section_title("evaluation_builder"), unsafe_allow_html=True)
        st.table(_evaluation_rows(plan))

    with risk_matrix_tab:
        st.markdown(_section_title("risk_matrix"), unsafe_allow_html=True)
        st.table(_risk_rows(plan))

    with memory_tab:
        _render_memory_tab(plan)

    with export_tab:
        _render_export_section(plan)


def _render_export_section(plan: ProjectPlan) -> None:
    export_plan = plan
    comparison = st.session_state.get("memory_comparison")
    if comparison:
        export_plan = plan.model_copy(update={"memory_comparison": comparison})
    st.markdown(_section_title("export"), unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="export-card">
            <span>{_escape_html(_t("export_ready"))}</span>
            <h3>{_escape_html(_t("export_title"))}</h3>
            <p>{_escape_html(_t("export_body"))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    markdown_text = project_plan_to_markdown(export_plan)
    json_text = project_plan_to_json(export_plan)
    pdf_bytes = project_plan_to_pdf(export_plan)
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
                <strong>{_escape_html(_t("reason"))}</strong>
                <p>{_escape_html(question.rationale)}</p>
            </div>
            <div>
                <strong>{_escape_html(_t("measurable_outcome"))}</strong>
                <p>{_escape_html(question.measurable_outcome)}</p>
            </div>
        </div>
    </div>
    """


def _method_card(method: MethodologyAdvice) -> str:
    return f"""
    <div class="method-card">
        <div class="method-card-header">
            <span>{_escape_html(method.method_name)}</span>
            <p>{_escape_html(method.description)}</p>
        </div>
        {_key_value_list([
            (_t("why_it_fits"), method.fit_reason),
            (_t("required_steps"), _join_items(method.required_steps)),
            (_t("required_artifacts"), _join_items(method.required_data_or_artifacts)),
            (_t("limitations"), _join_items(method.limitations)),
        ])}
    </div>
    """


def _evaluation_rows(plan: ProjectPlan) -> list[dict[str, str]]:
    return [
        {
            _t("criterion"): criterion.name,
            _t("description"): criterion.description,
            _t("how_to_measure"): criterion.measurement,
            _t("expected_evidence"): criterion.expected_evidence,
            _t("priority"): criterion.priority,
        }
        for criterion in plan.evaluation_criteria
    ]


def _risk_rows(plan: ProjectPlan) -> list[dict[str, str]]:
    return [
        {
            _t("risk"): risk.risk_title,
            _t("description"): risk.description,
            _t("probability"): risk.probability,
            _t("impact"): risk.impact,
            _t("mitigation"): risk.mitigation_strategy,
        }
        for risk in plan.risk_matrix
    ]


def _render_memory_tab(plan: ProjectPlan) -> None:
    st.markdown(_section_title("memory"), unsafe_allow_html=True)
    recent_plans = load_project_plans()
    st.markdown(
        f"""
        <div class="info-card">
            <span>{_escape_html(_t("local_memory"))}</span>
            <h3>{_escape_html(_t("memory_title"))}</h3>
            <p>{_escape_html(_t("memory_body"))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_input(_t("search_saved"), placeholder=_t("search_saved_placeholder"))
    search_results = search_project_plans(query) if query else recent_plans[:5]
    if not search_results:
        st.info(_t("no_search_results"))
        return

    selected_index = st.selectbox(
        _t("saved_plans"),
        options=list(range(len(search_results))),
        format_func=lambda index: search_results[index].topic_analysis.refined_topic,
    )
    selected_plan = search_results[selected_index]

    col_load, col_compare = st.columns(2)
    with col_load:
        if st.button(_t("load_selected"), use_container_width=True):
            st.session_state["project_plan"] = selected_plan
            st.session_state["plan_status"] = "loaded"
            st.session_state["memory_comparison"] = None
            st.session_state.pop("plan_error", None)
            st.rerun()
    with col_compare:
        if st.button(_t("compare_current"), use_container_width=True):
            comparison = compare_project_plans(plan, selected_plan)
            st.session_state["memory_comparison"] = comparison
            st.rerun()

    st.markdown(_section_title("recent_saved"), unsafe_allow_html=True)
    for saved_plan in recent_plans[:3]:
        st.markdown(
            f"""
            <div class="memory-card">
                <strong>{_escape_html(saved_plan.topic_analysis.refined_topic)}</strong>
                <p>{_escape_html(", ".join(saved_plan.topic_analysis.detected_focus_areas))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    comparison = st.session_state.get("memory_comparison")
    if comparison:
        st.markdown(_section_title("plan_comparison"), unsafe_allow_html=True)
        st.table(
            [
                {
                    _t("aspect"): _t("same_focus"),
                    _t("result"): _join_items(comparison.same_focus_areas),
                },
                {
                    _t("aspect"): _t("different_focus"),
                    _t("result"): _join_items(comparison.different_focus_areas),
                },
                {
                    _t("aspect"): _t("similar_methodology"),
                    _t("result"): comparison.similar_methodology,
                },
                {
                    _t("aspect"): _t("changed_questions"),
                    _t("result"): _join_items(comparison.changed_research_questions),
                },
                {_t("aspect"): _t("recommendation"), _t("result"): comparison.recommendation},
            ]
        )


def _validation_rows(plan: ProjectPlan) -> list[dict[str, str]]:
    return [
        {
            "RQ": f"RQ{index}",
            _t("clarity"): validation.clarity,
            _t("testability"): validation.testability,
            _t("scope"): validation.scope,
            _t("feasibility"): validation.feasibility,
        }
        for index, validation in enumerate(plan.question_validations, start=1)
    ]


def _render_validation_explanations(plan: ProjectPlan) -> None:
    for index, validation in enumerate(plan.question_validations, start=1):
        with st.expander(_t("validation_expander").format(index=index), expanded=False):
            st.markdown(f"**{_t('question')}:** {validation.question}")
            st.markdown(
                _key_value_list(
                    [
                        (f"{_t('clarity')}: {validation.clarity}", validation.clarity_reason),
                        (
                            f"{_t('testability')}: {validation.testability}",
                            validation.testability_reason,
                        ),
                        (f"{_t('scope')}: {validation.scope}", validation.scope_reason),
                        (
                            f"{_t('feasibility')}: {validation.feasibility}",
                            validation.feasibility_reason,
                        ),
                        (_t("improvement"), validation.improvement_suggestion),
                    ]
                ),
                unsafe_allow_html=True,
            )


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


def _join_items(items: list[str]) -> str:
    return "; ".join(items) if items else _t("not_specified")


def _section_title(key: str) -> str:
    return f'<div class="section-title">{_escape_html(_t(key))}</div>'


def _history_title(idea: str, limit: int = 42) -> str:
    clean = " ".join(idea.split())
    return clean if len(clean) <= limit else f"{clean[: limit - 3]}..."


def _escape_html(value: str) -> str:
    return html.escape(value, quote=True)


def _apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f5f7fb;
            --surface: #ffffff;
            --card: rgba(255,255,255,0.94);
            --nested-card: rgba(255,255,255,0.86);
            --ink: #1f2933;
            --muted: #667085;
            --accent: #0f766e;
            --accent-dark: #134e4a;
            --line: #e3e8ef;
            --soft: #e9f7f5;
            --input-bg: #ffffff;
            --input-text: #111827;
            --secondary-button-bg: #ffffff;
            --table-bg: #ffffff;
            --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            --shadow-soft: 0 10px 25px rgba(15, 23, 42, 0.06);
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0f1720;
                --surface: #151c28;
                --card: rgba(21, 28, 40, 0.96);
                --nested-card: rgba(24, 33, 47, 0.96);
                --ink: #f8fafc;
                --muted: #cbd5e1;
                --accent: #14b8a6;
                --accent-dark: #99f6e4;
                --line: #334155;
                --soft: #143a3a;
                --input-bg: #111827;
                --input-text: #f8fafc;
                --secondary-button-bg: #111827;
                --table-bg: #111827;
                --shadow: 0 18px 45px rgba(0, 0, 0, 0.28);
                --shadow-soft: 0 10px 25px rgba(0, 0, 0, 0.22);
            }
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15,118,110,0.12), transparent 34rem),
                radial-gradient(circle at top right, rgba(37,99,235,0.10), transparent 30rem),
                var(--bg);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--line);
            background: var(--surface);
            color: var(--ink);
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 1rem;
        }

        [data-testid="stSidebar"] .stButton > button {
            justify-content: flex-start;
            min-height: 2.65rem;
            border-color: var(--line);
            background: var(--secondary-button-bg);
            color: var(--ink);
            text-align: left;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            justify-content: center;
            border-color: var(--accent);
            background: var(--accent);
            color: #ffffff;
        }

        .history-heading {
            margin: 1rem 0 0.4rem;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
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
        .method-card,
        .memory-card,
        .question-card,
        .export-card {
            border: 1px solid var(--line);
            background: var(--card);
            box-shadow: var(--shadow-soft);
            color: var(--ink);
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
            background: var(--input-bg);
            color: var(--input-text);
            font-size: 1rem;
            line-height: 1.5;
            box-shadow: var(--shadow-soft);
        }

        div[data-testid="stTextArea"] textarea::placeholder,
        div[data-testid="stTextInput"] input::placeholder {
            color: color-mix(in srgb, var(--muted) 78%, transparent);
        }

        div[data-testid="stTextInput"] input,
        div[data-baseweb="select"] > div {
            border-color: var(--line);
            background: var(--input-bg);
            color: var(--input-text);
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 14px;
            border: 1px solid var(--accent);
            font-weight: 750;
            min-height: 2.85rem;
            background: var(--secondary-button-bg);
            color: var(--ink);
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

        .error-state {
            min-height: 430px;
            border-radius: 16px;
            padding: 1.35rem;
            border: 1px solid #f1a9a0;
            background: linear-gradient(135deg, rgba(220,38,38,0.10), var(--card)), var(--surface);
            box-shadow: var(--shadow-soft);
            color: var(--ink);
        }

        .error-state .eyebrow {
            color: #dc2626 !important;
        }

        .error-state h2 {
            margin: 0.35rem 0 0.5rem 0;
            color: var(--ink);
        }

        .error-state pre {
            margin-top: 1rem;
            padding: 0.85rem 1rem;
            border-radius: 12px;
            border: 1px solid var(--line);
            background: var(--nested-card);
            color: var(--muted);
            font-size: 0.86rem;
            white-space: pre-wrap;
            word-break: break-word;
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
        .method-card,
        .memory-card,
        .question-card {
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.85rem;
        }

        .topic-card {
            background:
                linear-gradient(135deg, rgba(15,118,110,0.16), var(--card)),
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

        .method-card-header {
            display: grid;
            gap: 0.45rem;
            margin-bottom: 0.75rem;
        }

        .method-card-header span {
            width: fit-content;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: var(--soft);
            color: var(--accent-dark);
            padding: 0.35rem 0.62rem;
            font-weight: 850;
        }

        .method-card-header p,
        .memory-card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.5;
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
            background: var(--nested-card);
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
            color: var(--ink);
        }

        div[data-testid="stTabs"] button {
            font-size: 0.95rem;
            font-weight: 750;
        }

        div[data-testid="stTable"] {
            font-size: 0.96rem;
        }

        div[data-testid="stTable"] table,
        div[data-testid="stTable"] thead,
        div[data-testid="stTable"] tbody,
        div[data-testid="stTable"] tr,
        div[data-testid="stTable"] th,
        div[data-testid="stTable"] td {
            background: var(--table-bg) !important;
            color: var(--ink) !important;
            border-color: var(--line) !important;
        }

        .stMarkdown,
        .stCaption,
        label,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--ink);
        }

        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--ink) !important;
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
