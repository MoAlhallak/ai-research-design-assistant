"""Create the clean Moodle archive for the final project delivery."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = PROJECT_ROOT / "release"
ARCHIVE_PATH = RELEASE_DIR / "AI_Research_Design_Assistant_Final.zip"

EXCLUDED_DIRECTORIES = {
    ".agents",
    ".git",
    ".idea",
    ".mypy_cache",
    ".pytest-tmp",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "dist",
    "env",
    "exports",
    "outputs",
    "release",
    "render",
    "renders",
    "screenshots",
    "temp",
    "tmp",
    "venv",
}
EXCLUDED_FILE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "credentials.json",
    "secrets.toml",
}
EXCLUDED_SUFFIXES = {
    ".key",
    ".p12",
    ".pem",
    ".pfx",
    ".pyc",
    ".pyo",
}


def should_exclude(relative_path: Path) -> bool:
    """Return True when a path must not be included in the submission."""
    parts = relative_path.parts
    if any(part in EXCLUDED_DIRECTORIES or part.endswith(".egg-info") for part in parts):
        return True

    name = relative_path.name
    if name in EXCLUDED_FILE_NAMES or relative_path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True

    if name == ".env":
        return True
    if name.startswith(".env.") and name != ".env.example":
        return True

    return False


def iter_submission_files() -> list[Path]:
    """Collect project files in stable archive order."""
    files = []
    for path in PROJECT_ROOT.rglob("*"):
        relative_path = path.relative_to(PROJECT_ROOT)
        if path.is_symlink() or should_exclude(relative_path):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda path: path.relative_to(PROJECT_ROOT).as_posix().lower())


def create_archive() -> Path:
    """Write and return the final-delivery ZIP path."""
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    files = iter_submission_files()

    with ZipFile(ARCHIVE_PATH, mode="w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, arcname=path.relative_to(PROJECT_ROOT).as_posix())

    return ARCHIVE_PATH


def main() -> None:
    archive_path = create_archive()
    relative_archive = archive_path.relative_to(PROJECT_ROOT)
    print(f"Created {relative_archive} with {len(iter_submission_files())} project files.")


if __name__ == "__main__":
    main()
