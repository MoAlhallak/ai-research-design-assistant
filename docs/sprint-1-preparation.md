# Sprint 1 Preparation: Research Planning Agent

## 1. Sprint-1-Ziel

Ziel von Sprint 1 ist ein stabiler MVP des Research Planning Agents. Der Agent soll eine einfache Projektidee entgegennehmen, daraus einen strukturierten Forschungsplan erzeugen und diesen lokal speichern oder exportieren können.

Der Fokus liegt nicht auf perfekter KI-Qualität, sondern auf einem funktionierenden, präsentierbaren Workflow:

- Nutzer gibt eine Projektidee ein.
- Agent analysiert Thema, Fokus und Problem.
- Agent grenzt das Thema ein.
- Agent erstellt Forschungsfragen.
- Agent empfiehlt Methodik, Evaluation und Risiken.
- Agent erstellt einen einfachen Sprintplan.
- Ergebnis wird als Markdown und JSON exportiert.
- Erste einfache Memory-Funktion speichert frühere Pläne lokal.

## 2. Sprint-1-MVP

Sprint 1 legte die lokale Planungslogik und das `ProjectPlan`-Schema an. In der
Final-Delivery-Version dient diese Pipeline als Scaffold; der finale Plan wird
verpflichtend über Academic Cloud / SAIA erzeugt.

### Muss-Funktionen

- Eingabefeld für eine Projektidee
- Button zum Generieren eines Forschungsplans
- Themenanalyse mit Keywords und Fokusbereichen
- Eingrenzung des Themas
- mindestens drei Forschungsfragen
- Methodikvorschlag
- Evaluationskriterien
- Risiken mit Gegenmaßnahmen
- Sprintplan
- Export als Markdown
- Export als JSON
- einfache lokale Speicherung früherer Pläne

### Kann-Funktionen

- Anzeige früherer Projektpläne
- Button `Save to Memory`
- Button `Show Previous Plans`
- einfache Suche in gespeicherten Plänen
- spätere ChromaDB-Anbindung für semantische Memory
- strukturierte Finalgenerierung über Academic Cloud / SAIA

## 3. Was macht der Agent genau?

Der Agent arbeitet mit einer einfachen Nutzereingabe.

Beispiel:

```text
Ich möchte zu Agentic AI Security und Tool-Nutzung arbeiten.
```

Danach führt der Agent mehrere Schritte aus.

### Schritt 1: Projektidee verstehen

Der Agent analysiert die Eingabe und erkennt Thema, Keywords und Forschungsbereich.

Beispiel:

```text
Thema: Agentic AI Security
Fokus: Tool-Nutzung
Problem: Risiken bei autonomen KI-Agenten
Mögliche Richtung: Sicherheitsanalyse oder Prototyp
```

### Schritt 2: Thema eingrenzen

Viele Themen sind am Anfang zu groß. Deshalb macht der Agent das Thema konkreter und realistischer.

Aus:

```text
Agentic AI Security
```

wird zum Beispiel:

```text
Sicherheitsrisiken bei der Tool-Nutzung von KI-Agenten in kleinen Prototyp-Systemen.
```

Das ist besser, weil es konkreter, messbarer und für ein studentisches Projekt realistischer ist.

### Schritt 3: Forschungsfragen vorschlagen

Der Agent erstellt passende Forschungsfragen.

Beispiel:

```text
RQ1: Welche Risiken entstehen, wenn KI-Agenten externe Tools nutzen?
RQ2: Wie können diese Risiken bewertet werden?
RQ3: Welche Schutzmaßnahmen passen für einen kleinen Prototyp?
```

Diese Fragen sind konkreter als nur `Agentic AI Security` und können später evaluiert werden.

### Schritt 4: Methodik empfehlen

Der Agent schlägt eine passende Vorgehensweise vor.

Beispiele:

- strukturierter Vergleich
- kleiner Prototyp
- Testszenarien
- Evaluations-Checkliste
- Risikoanalyse

Das Ziel ist, dass der Student nicht nur ein Thema hat, sondern auch weiß, wie das Thema bearbeitet werden kann.

### Schritt 5: Evaluation planen

Der Agent schlägt Kriterien vor, mit denen das Ergebnis später bewertet werden kann.

Beispiele:

- Korrektheit
- Security-Abdeckung
- Nutzbarkeit
- Reproduzierbarkeit
- Grenzen
- Verständlichkeit
- Vergleichbarkeit

Das ist wichtig, weil ein Forschungsprojekt nicht nur gebaut, sondern auch bewertet werden muss.

### Schritt 6: Risiken und Grenzen erkennen

Der Agent zeigt mögliche Risiken und Grenzen.

Beispiele:

- Thema ist noch zu breit.
- Forschungsfrage ist nicht messbar.
- Methodik passt nicht genau.
- LLM kann falsche oder zu allgemeine Vorschläge machen.
- Nutzer gibt zu wenig Kontext ein.

Dazu schlägt der Agent Gegenmaßnahmen vor, zum Beispiel Checklisten, Templates oder Rückfragen.

### Schritt 7: Sprintplan erstellen

Der Agent erstellt einen einfachen Sprintplan.

Beispiel:

```text
Sprint 1: Architektur, MVP und Templates
Sprint 2: Themenanalyse und Forschungsfragen
Sprint 3: Methodik, Evaluation und Risiken
Sprint 4: Demo, Export, Tests und Dokumentation
```

## 4. Memory: Warum ist der Agent persönlich?

Ein wichtiger Teil des Projekts ist die Memory-Funktion.

Der Agent soll nicht jedes Mal bei null anfangen. Er soll frühere Projektideen und Pläne speichern können. Dadurch wirkt er mehr wie ein persönlicher Research Assistant und weniger wie ein normaler Chatbot.

Beispiel:

Beim ersten Mal gibt der Nutzer ein:

```text
Ich möchte über Agentic AI Security arbeiten.
```

Der Agent erstellt einen Plan und speichert:

- Projektidee
- Thema
- Fokus
- Forschungsfragen
- Methodik
- Evaluation
- Risiken
- Sprintplan

Beim nächsten Mal fragt der Nutzer:

```text
Kannst du meinen Plan verbessern?
```

Dann kann der Agent auf den alten Plan zugreifen und antworten:

```text
Dein letzter Fokus war Tool-Nutzung bei Agentic AI Security.
Ich würde die Forschungsfrage noch enger machen und die Evaluation klarer definieren.
```

Das ist der Unterschied zu einem normalen Chatbot. Ein normaler Chatbot vergisst oft den Kontext. Der Agent soll mit Memory arbeiten und frühere Projektstände wiederverwenden.

## 5. Memory in Sprint 1

In Sprint 1 reicht eine einfache Memory. Die semantische Memory mit ChromaDB kann vorbereitet, aber noch nicht voll ausgebaut werden.

### Einfache Sprint-1-Memory

Die erste Version kann Projektpläne lokal speichern, zum Beispiel als JSON-Dateien:

```text
outputs/project-memory/
  plan-001.json
  plan-002.json
  plan-003.json
```

Gespeichert werden:

- Originalidee
- eingegrenztes Thema
- Fokusbereiche
- Forschungsfragen
- Methodik
- Evaluation
- Risiken
- Sprintplan

### Spätere semantische Memory mit ChromaDB

Für eine spätere Version ist ChromaDB geplant.

ChromaDB ist eine lokale Vektordatenbank. Sie speichert Texte als Embeddings. Dadurch kann der Agent ähnliche Inhalte wiederfinden, auch wenn der Nutzer andere Wörter benutzt.

Beispiel:

Gespeichert wurde:

```text
Agentic AI Security und Tool-Nutzung
```

Später sucht der Nutzer:

```text
KI-Agenten mit externen Tools absichern
```

ChromaDB kann erkennen, dass beide Themen ähnlich sind.

## 6. Technischer Workflow

Der lokale Sprint-1-Workflow bildet heute den ersten Teil der
Final-Delivery-Architektur:

```text
User Input
→ Local Planning Scaffold
→ Structured SAIA Request
→ LLM JSON Response
→ Pydantic Validation
→ ProjectPlan
→ UI, Memory and Export
```

Einfach erklärt:

Der Nutzer gibt eine Idee ein. Die lokale Pipeline analysiert sie und erzeugt
die vollständige technische Struktur. SAIA formuliert daraus den finalen Inhalt
als JSON. Nur ein erfolgreich als `ProjectPlan` validierter Plan wird angezeigt,
gespeichert oder exportiert.

## 7. API-Key

Für die Erzeugung eines finalen Plans ist
`ACADEMIC_CLOUD_API_KEY` erforderlich. Das verwendete Modell ist
`qwen3-30b-a3b-instruct-2507`.

Fehlt der Key, ist die API nicht erreichbar oder liefert das Modell kein
gültiges `ProjectPlan`-JSON, zeigt die Anwendung einen klaren Fehler. Das lokale
Scaffold wird nicht als fertiger Plan zurückgegeben. Bereits gespeicherte Pläne
sowie lokale History-Funktionen wie Suche, Umbenennen und Löschen bleiben
verfügbar.

Der API-Key darf nicht fest im Code stehen. Er wird ausschließlich über eine
lokale `.env`-Datei oder eine Runtime-Umgebungsvariable bereitgestellt.

Beispiel:

```text
ACADEMIC_CLOUD_API_KEY=dein_api_key
```

Die lokale `.env` ist durch Git und Docker ausgeschlossen und darf nicht nach
GitHub hochgeladen werden.

## 8. Verwendete Tools

### Python

Python ist die Hauptsprache des Projekts.

Python wird genutzt für:

- Agentenlogik
- Verarbeitung der Nutzereingabe
- Erstellung des Forschungsplans
- Export-Funktionen
- Verbindung zu APIs
- Memory-Logik

### Streamlit

Streamlit wird für die Benutzeroberfläche genutzt.

Die Sprint-1-Demo kann folgende Elemente enthalten:

- Eingabefeld für Projektidee
- Button `Generate Research Plan`
- Ausgabe des Forschungsplans
- Button `Save to Memory`
- Button `Show Previous Plans`
- Button `Export as Markdown`

Streamlit eignet sich für Sprint 1, weil man schnell eine einfache Web-App zeigen kann.

### ChromaDB

ChromaDB ist für die spätere Memory geplant.

Sie kann speichern:

- frühere Projektideen
- Forschungsfragen
- Methodik-Vorschläge
- Templates
- Beispiele
- später Dokumente oder Regeln

Der Vorteil ist, dass der Agent ähnliche frühere Projekte wiederfinden kann.

### LangChain

LangChain verbindet die einzelnen Schritte des Workflows.

Beispiel:

```text
Input -> Analyse -> Memory Search -> Structured Output -> Export
```

LangChain ist also nicht die KI selbst, sondern die Steuerung des Agenten-Workflows.

### LLM / SAIA API

Academic Cloud / SAIA erzeugt verpflichtend den finalen Inhalt des Plans aus dem
lokalen Scaffold.

Das LLM kann erzeugen:

- Forschungsfragen
- Methodikempfehlungen
- Risikoerklärungen
- Sprintpläne
- bessere Formulierungen

Ohne erfolgreiche SAIA-Antwort gibt die Final-Delivery-Version keinen
unvollständigen Plan zurück.

### Pydantic / Structured Output

Pydantic prüft, ob die LLM-Antwort die erforderlichen Felder, Verschachtelungen
und Datentypen des `ProjectPlan`-Schemas besitzt. Diese technische Validierung
beweist nicht, dass der Inhalt wissenschaftlich korrekt ist.

Beispiel:

```json
{
  "topic": "Agentic AI Security",
  "research_questions": [
    "Welche Risiken entstehen bei Tool-Nutzung?"
  ],
  "methodology": "Prototyp + Testszenarien",
  "evaluation": [
    "Korrektheit",
    "Nutzbarkeit",
    "Security-Abdeckung"
  ],
  "risks": [
    "zu breite Fragestellung",
    "Halluzination"
  ]
}
```

Das ist wichtig, weil die Ergebnisse später exportiert oder weiterverarbeitet werden können.

### Markdown / JSON / PDF Export

Der Agent soll Ergebnisse exportieren können.

Geplante Outputs:

```text
research_plan.md
sprint_plan.md
evaluation_checklist.json
risks.md
eventuell PDF
```

In Sprint 1 reichen Markdown und JSON.

## 9. Sprint-1-Demo-Ablauf

Ein möglicher Demo-Ablauf:

1. Streamlit-App starten.
2. Projektidee eingeben:

```text
Ich möchte zu Agentic AI Security und Tool-Nutzung arbeiten.
```

3. Button `Generate Project Plan` klicken.
4. Agent zeigt:

- eingegrenztes Thema
- Forschungsfragen
- Methodik
- Evaluation
- Risiken
- Sprintplan

5. Plan als Markdown oder JSON exportieren.
6. Plan lokal speichern.
7. Frühere Pläne anzeigen.

## 10. Sprint-1-Backlog

### Aufgabe 1: MVP-Workflow prüfen

Akzeptanzkriterien:

- Eine Projektidee kann eingegeben werden.
- Ein strukturierter Plan wird erzeugt.
- Der Plan enthält Thema, Forschungsfragen, Methodik, Evaluation, Risiken und Sprintplan.

### Aufgabe 2: Streamlit-Oberfläche vorbereiten

Akzeptanzkriterien:

- Es gibt ein Eingabefeld.
- Es gibt einen Generate-Button.
- Der generierte Plan wird sichtbar angezeigt.
- Download von Markdown und JSON ist möglich.

### Aufgabe 3: Lokale Memory vorbereiten

Akzeptanzkriterien:

- Ein generierter Plan kann lokal gespeichert werden.
- Gespeicherte Pläne können wieder angezeigt werden.
- Die Struktur ist später für ChromaDB erweiterbar.

### Aufgabe 4: Export prüfen

Akzeptanzkriterien:

- Markdown-Export funktioniert.
- JSON-Export funktioniert.
- Dateinamen und Ordnerstruktur sind klar.

### Aufgabe 5: Präsentationsbeispiel vorbereiten

Akzeptanzkriterien:

- Beispielinput ist vorbereitet.
- Beispieloutput ist vorhanden.
- Demo erzeugt mit einem lokal konfigurierten `ACADEMIC_CLOUD_API_KEY` einen
  validierten finalen Plan.

## 11. Sprint-1-Ergebnis

Am Ende von Sprint 1 soll ein präsentierbarer MVP existieren:

```text
Ein Nutzer gibt eine Forschungsprojektidee ein.
Der Agent erstellt daraus einen strukturierten Forschungsplan.
Der Plan kann exportiert und lokal gespeichert werden.
Die Memory ist einfach vorbereitet und kann später mit ChromaDB erweitert werden.
```

Damit ist die Grundlage für Sprint 2 gelegt, in dem Themenanalyse, Forschungsfragen und Memory intelligenter gemacht werden können.
