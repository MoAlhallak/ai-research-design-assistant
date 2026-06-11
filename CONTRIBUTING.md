# Contributing

This is a small portfolio project for the AI Research Design Assistant.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Quality checks

```powershell
python -m ruff check .
python -m compileall src app.py
```

## Notes

- Do not commit API keys or `.env` files.
- Generated plans and memory files belong in `outputs/`.
- The assistant is a planning aid. Its output should always be checked by the student.
