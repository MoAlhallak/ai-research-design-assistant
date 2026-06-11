from __future__ import annotations

from datetime import datetime
import hashlib
import math
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from ai_research_design_assistant.models import ProjectPlan
from ai_research_design_assistant.text import keyword_overlap


DEFAULT_MEMORY_DIR = Path("outputs/project-memory")
DEFAULT_CHROMA_MEMORY_DIR = Path("outputs/chroma-memory")
DEFAULT_MEMORY_COLLECTION = "project_plan_memory"


class HashEmbeddings(Embeddings):
    """Deterministic local embeddings for the prototype memory."""

    def __init__(self, dimensions: int = 384) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def save_project_plan(
    plan: ProjectPlan,
    memory_dir: Path = DEFAULT_MEMORY_DIR,
) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = memory_dir / f"project-plan-{timestamp}.json"
    path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    _index_project_plan(plan, path)
    return path


def load_project_plans(memory_dir: Path = DEFAULT_MEMORY_DIR) -> list[ProjectPlan]:
    if not memory_dir.exists():
        return []

    plans: list[ProjectPlan] = []
    for path in sorted(memory_dir.glob("project-plan-*.json"), reverse=True):
        try:
            plans.append(ProjectPlan.model_validate_json(path.read_text(encoding="utf-8")))
        except ValueError:
            continue
    return plans


def find_similar_project_plans(
    idea: str,
    memory_dir: Path = DEFAULT_MEMORY_DIR,
    limit: int = 3,
) -> list[ProjectPlan]:
    chroma_results = _find_similar_with_chroma(idea, limit=limit)
    if chroma_results:
        return chroma_results

    scored = []
    for plan in load_project_plans(memory_dir):
        text = (
            f"{plan.idea} "
            f"{plan.topic_analysis.refined_topic} "
            f"{' '.join(plan.topic_analysis.detected_focus_areas)}"
        )
        scored.append((keyword_overlap(idea, text), plan))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [plan for score, plan in scored[:limit] if score > 0]


def _index_project_plan(plan: ProjectPlan, json_path: Path) -> None:
    try:
        vector_store = _chroma_memory()
        vector_store.add_documents(
            [
                Document(
                    page_content=_plan_memory_text(plan),
                    metadata={"json_path": str(json_path)},
                )
            ]
        )
    except Exception:
        return


def _find_similar_with_chroma(idea: str, limit: int) -> list[ProjectPlan]:
    try:
        documents = _chroma_memory().similarity_search(idea, k=limit)
    except Exception:
        return []

    plans: list[ProjectPlan] = []
    for document in documents:
        path = Path(str(document.metadata.get("json_path", "")))
        if not path.exists():
            continue
        try:
            plans.append(ProjectPlan.model_validate_json(path.read_text(encoding="utf-8")))
        except ValueError:
            continue
    return plans


def _plan_memory_text(plan: ProjectPlan) -> str:
    questions = " ".join(question.question for question in plan.research_questions)
    methodology = f"{plan.methodology.name} {' '.join(plan.methodology.steps)}"
    return (
        f"{plan.idea} "
        f"{plan.topic_analysis.refined_topic} "
        f"{' '.join(plan.topic_analysis.detected_focus_areas)} "
        f"{questions} "
        f"{methodology}"
    )


def _chroma_memory():
    from langchain_chroma import Chroma

    DEFAULT_CHROMA_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=DEFAULT_MEMORY_COLLECTION,
        embedding_function=HashEmbeddings(),
        persist_directory=str(DEFAULT_CHROMA_MEMORY_DIR),
    )
