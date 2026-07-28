# Demo Day Checklist

A short manual checklist to confirm the AI Research Design Assistant is stable
before a live demo. Work through it top to bottom.

## Startup

- [ ] A local `.env` exists and contains the real `ACADEMIC_CLOUD_API_KEY`
- [ ] App starts locally: `python -m streamlit run app.py`
- [ ] App opens at `http://localhost:8501` without errors in the terminal
- [ ] App starts in Docker: `docker compose up --build`
- [ ] Docker app is reachable at `http://localhost:8501`
- [ ] Docker health endpoint returns `ok` at
      `http://localhost:8501/_stcore/health`

## Core flow

- [ ] Demo example loads (click **Use example input**)
- [ ] Plan generation works (click **Generate Plan**)
- [ ] A missing key, unavailable API or invalid response produces a clear error
      and no incomplete plan
- [ ] Overview, Questions, Methodology Advisor, Evaluation Builder, Risk Matrix,
      Memory and Export tabs all render
- [ ] Switching tabs and opening expanders does not reset the plan

## Plan History

- [ ] New generated plans appear immediately in the Plan History sidebar
- [ ] History loads old plans (click a saved plan to reopen it)
- [ ] Search filters saved plans
- [ ] **New Plan** starts a clean empty input without deleting saved plans
- [ ] Empty-state message shows when no plans exist

## Rename and delete

- [ ] Rename plan works (pencil icon, edit title, **Save title**)
- [ ] Renamed title appears immediately in the history
- [ ] Rename persists after restarting the app
- [ ] Rename and delete still work while a search filter is active
- [ ] Delete plan works (trash icon, **Confirm delete**)
- [ ] Deleting one plan does not remove the others
- [ ] Deleting the currently open plan resets the main area to an empty state
- [ ] Delete persists after restarting the app

## Exports

- [ ] Export Markdown downloads a valid `.md` file
- [ ] Export JSON downloads a valid `.json` file
- [ ] Export PDF downloads a valid `.pdf` file

## Quality

- [ ] Tests pass: `python -m pytest`
- [ ] Lint passes: `python -m ruff check .`
- [ ] Compile check passes: `python -m compileall src app.py`
- [ ] Docker configuration passes: `docker compose config --quiet`
- [ ] No "Sprint" wording is visible anywhere in the GUI
