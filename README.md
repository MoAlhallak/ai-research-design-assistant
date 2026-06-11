# AI Research Design Assistant

Das Projekt ist ein agentischer Prototyp fuer Studierende. Der Assistant hilft,
aus einer groben Forschungsidee einen strukturierten Forschungsplan zu erstellen.

Der Fokus liegt auf Forschungsplanung, nicht auf Paper-Suche. Der Agent erstellt
ein eingegrenztes Thema, Forschungsfragen, Methodik, Evaluation, Risiken,
naechste Schritte und Exporte.

## Was der Agent macht

Der Nutzer gibt eine Projektidee ein, zum Beispiel:

```text
Ich moechte zu Agentic AI Security und Tool-Nutzung arbeiten.
```

Der Agent erstellt daraus:

- ein eingegrenztes Forschungsthema
- Fokusbereiche
- konkrete und pruefbare Forschungsfragen
- Methodikvorschlag mit Vorgehensweise und Tools
- Evaluationskriterien
- Risiken und Gegenmassnahmen
- einen Arbeitsplan mit naechsten Schritten
- Export als Markdown, JSON und PDF

## Technischer Ansatz

- `Python`: Hauptsprache fuer Logik, Datenverarbeitung und Prototyp.
- `Streamlit`: moderne Weboberflaeche fuer Studierende.
- `LangChain`: verbindet die Planungsschritte vom Input bis zum strukturierten Output.
- `Pydantic`: definiert den strukturierten Output des Forschungsplans.
- `ChromaDB`: ist fuer semantische Memory angebunden.
- `SAIA / Academic Cloud`: kann ueber `.env` konfiguriert werden, um Plaene intern mit einem LLM zu verbessern.

## Sprint 2 Verbesserungen

Sprint 2 verbessert den bestehenden MVP, ohne die Projektstruktur neu zu bauen.

- Deutsch- und Englisch-Erkennung wurde geschaerft.
- Deutsche Umlaute werden normalisiert: `ae`, `oe`, `ue`, `ss`.
- Schwache Eingabewoerter wie `ich`, `moechte`, `gerne`, `ueber`, `want`,
  `would`, `like`, `about` werden aus Keywords und Fokusbereichen entfernt.
- Wichtige Themenbegriffe wie `Agentic AI`, `Security`, `Tool Usage`,
  `Evaluation`, `Prototype` und `Research Design` bleiben als Fokusbereiche
  sichtbar.
- Forschungsfragen bekommen eine explizite Validierung fuer Klarheit,
  Testbarkeit, Scope, Machbarkeit und eine Verbesserungsempfehlung.
- Die Streamlit-App zeigt diese Fragenvalidierung direkt im Ergebnis an.
- Die LLM-Verbesserung nutzt einen robusten Fallback. Wenn kein
  API-Key vorhanden ist, die API nicht erreichbar ist oder die Antwort kein
  gueltiges vollstaendiges JSON enthaelt, wird der lokale Template-Plan weiter
  genutzt.
- Eine kleine `pytest`-Testsuite prueft Keyword-Bereinigung,
  Forschungsfragen, Validierung, Memory, Export und LLM-Fallback.

## Memory

Die Memory speichert fruehere Projektideen und Forschungsplaene. Dadurch kann der
Agent spaeter alte Projektstaende laden und aehnliche Plaene wiederfinden.

Gespeichert wird lokal in:

```text
outputs/project-memory/
outputs/chroma-memory/
```

ChromaDB ist fuer semantische Suche angebunden. Wenn ChromaDB nicht verfuegbar
ist, nutzt der Agent lokale JSON-Dateien als Fallback.

Die aktuelle ChromaDB-Memory ist weiterhin ein Prototyp. Sie nutzt lokale,
deterministische Hash-Embeddings fuer stabile Offline-Demos. Fuer bessere echte
semantische Suche koennen spaeter produktive Embedding-Modelle angebunden
werden.

## API-Key

Der Agent funktioniert ohne API-Key.

Ohne API-Key nutzt er:

- Templates
- Regeln
- lokale Planungslogik
- Memory
- Exportfunktionen

Wenn ein API-Key in `.env` oder als Environment Variable konfiguriert ist, kann
der Agent intern ein LLM ueber SAIA / Academic Cloud nutzen. Das LLM verbessert
Formulierungen, Forschungsfragen, Methodik und Risikoanalyse. In der App wird
kein API-Key-Feld angezeigt.

Ohne API-Key oder bei einem API-/JSON-Fehler bleibt die App stabil und nutzt
automatisch den lokalen Template-Fallback.

Der API-Key wird nicht im Code gespeichert und soll nicht auf GitHub hochgeladen
werden.

Konfiguration kann ueber Environment Variables oder eine lokale `.env` erfolgen:

```text
ACADEMIC_CLOUD_API_KEY=dein_api_key
ACADEMIC_CLOUD_BASE_URL=https://chat-ai.academiccloud.de/v1
ACADEMIC_CLOUD_MODEL=qwen3.5-122b-a10b
```

## Starten

```powershell
cd "C:\Users\HoOooms\Desktop\Desktob\UNI\MASTER\AAI\Agentic Ai Mo"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Danach oeffnet sich die App normalerweise im Browser:

```text
http://localhost:8501
```

## CLI

```powershell
.\.venv\Scripts\python.exe -m ai_research_design_assistant.cli plan "Ich moechte zu Agentic AI Security und Tool-Nutzung arbeiten"
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Falls `pytest` lokal fehlt:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

## Projektstruktur

```text
.
|-- .env.example
|-- .gitignore
|-- app.py
|-- CONTRIBUTING.md
|-- docs/
|   |-- project-structure.md
|   `-- sprint-1-preparation.md
|-- LICENSE
|-- pyproject.toml
|-- README.md
|-- src/ai_research_design_assistant/
    |-- agent.py
    |-- cli.py
    |-- exporters.py
    |-- llm.py
    |-- memory.py
    |-- models.py
    |-- planning.py
    |-- templates.py
    |-- text.py
    |-- validation.py
    `-- __init__.py
`-- tests/
    `-- test_sprint_2.py
```

Der alte doppelte Ordner `sprint_1/` wurde fuer die Abgabe entfernt. Die aktive
Version liegt im Projekt-Root und unter `src/`. Die Sprint-1-Vorbereitung ist
als Doku-Datei in `docs/sprint-1-preparation.md` erhalten.

Generierte Dateien wie `outputs/`, `.pytest_cache/`, `.ruff_cache/`,
`__pycache__/` und `*.egg-info/` gehoeren nicht zur Abgabe und sind in
`.gitignore` ausgeschlossen.

## Wichtige Grenze

Das System unterstuetzt die Planung. Es ersetzt keine Betreuung, keine
wissenschaftliche Bewertung und keine eigene Pruefung durch den Studierenden.
