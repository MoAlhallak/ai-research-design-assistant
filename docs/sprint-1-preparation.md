# Sprint 1 Preparation: Research Planning Agent

## 1. Sprint-1-Ziel

Ziel von Sprint 1 ist ein stabiler MVP des Research Planning Agents. Der Agent soll eine einfache Projektidee entgegennehmen, daraus einen strukturierten Forschungsplan erzeugen und diesen lokal speichern oder exportieren koennen.

Der Fokus liegt nicht auf perfekter KI-Qualitaet, sondern auf einem funktionierenden, praesentierbaren Workflow:

- Nutzer gibt eine Projektidee ein.
- Agent analysiert Thema, Fokus und Problem.
- Agent grenzt das Thema ein.
- Agent erstellt Forschungsfragen.
- Agent empfiehlt Methodik, Evaluation und Risiken.
- Agent erstellt einen einfachen Sprintplan.
- Ergebnis wird als Markdown und JSON exportiert.
- Erste einfache Memory-Funktion speichert fruehere Plaene lokal.

## 2. Sprint-1-MVP

Der MVP soll ohne externen API-Key funktionieren. Dadurch ist die Demo stabil und unabhaengig von Internet, Rate Limits oder API-Problemen.

### Muss-Funktionen

- Eingabefeld fuer eine Projektidee
- Button zum Generieren eines Forschungsplans
- Themenanalyse mit Keywords und Fokusbereichen
- Eingrenzung des Themas
- mindestens drei Forschungsfragen
- Methodikvorschlag
- Evaluationskriterien
- Risiken mit Gegenmassnahmen
- Sprintplan
- Export als Markdown
- Export als JSON
- einfache lokale Speicherung frueherer Plaene

### Kann-Funktionen

- Anzeige frueherer Projektplaene
- Button `Save to Memory`
- Button `Show Previous Plans`
- einfache Suche in gespeicherten Plaenen
- spaetere ChromaDB-Anbindung fuer semantische Memory
- optionale LLM-Verbesserung ueber API-Key

## 3. Was macht der Agent genau?

Der Agent arbeitet mit einer einfachen Nutzereingabe.

Beispiel:

```text
Ich moechte zu Agentic AI Security und Tool-Nutzung arbeiten.
```

Danach fuehrt der Agent mehrere Schritte aus.

### Schritt 1: Projektidee verstehen

Der Agent analysiert die Eingabe und erkennt Thema, Keywords und Forschungsbereich.

Beispiel:

```text
Thema: Agentic AI Security
Fokus: Tool-Nutzung
Problem: Risiken bei autonomen KI-Agenten
Moegliche Richtung: Sicherheitsanalyse oder Prototyp
```

### Schritt 2: Thema eingrenzen

Viele Themen sind am Anfang zu gross. Deshalb macht der Agent das Thema konkreter und realistischer.

Aus:

```text
Agentic AI Security
```

wird zum Beispiel:

```text
Sicherheitsrisiken bei der Tool-Nutzung von KI-Agenten in kleinen Prototyp-Systemen.
```

Das ist besser, weil es konkreter, messbarer und fuer ein studentisches Projekt realistischer ist.

### Schritt 3: Forschungsfragen vorschlagen

Der Agent erstellt passende Forschungsfragen.

Beispiel:

```text
RQ1: Welche Risiken entstehen, wenn KI-Agenten externe Tools nutzen?
RQ2: Wie koennen diese Risiken bewertet werden?
RQ3: Welche Schutzmassnahmen passen fuer einen kleinen Prototyp?
```

Diese Fragen sind konkreter als nur `Agentic AI Security` und koennen spaeter evaluiert werden.

### Schritt 4: Methodik empfehlen

Der Agent schlaegt eine passende Vorgehensweise vor.

Beispiele:

- strukturierter Vergleich
- kleiner Prototyp
- Testszenarien
- Evaluations-Checkliste
- Risikoanalyse

Das Ziel ist, dass der Student nicht nur ein Thema hat, sondern auch weiss, wie das Thema bearbeitet werden kann.

### Schritt 5: Evaluation planen

Der Agent schlaegt Kriterien vor, mit denen das Ergebnis spaeter bewertet werden kann.

Beispiele:

- Korrektheit
- Security-Abdeckung
- Nutzbarkeit
- Reproduzierbarkeit
- Grenzen
- Verstaendlichkeit
- Vergleichbarkeit

Das ist wichtig, weil ein Forschungsprojekt nicht nur gebaut, sondern auch bewertet werden muss.

### Schritt 6: Risiken und Grenzen erkennen

Der Agent zeigt moegliche Risiken und Grenzen.

Beispiele:

- Thema ist noch zu breit.
- Forschungsfrage ist nicht messbar.
- Methodik passt nicht genau.
- LLM kann falsche oder zu allgemeine Vorschlaege machen.
- Nutzer gibt zu wenig Kontext ein.

Dazu schlaegt der Agent Gegenmassnahmen vor, zum Beispiel Checklisten, Templates oder Rueckfragen.

### Schritt 7: Sprintplan erstellen

Der Agent erstellt einen einfachen Sprintplan.

Beispiel:

```text
Sprint 1: Architektur, MVP und Templates
Sprint 2: Themenanalyse und Forschungsfragen
Sprint 3: Methodik, Evaluation und Risiken
Sprint 4: Demo, Export, Tests und Dokumentation
```

## 4. Memory: Warum ist der Agent persoenlich?

Ein wichtiger Teil des Projekts ist die Memory-Funktion.

Der Agent soll nicht jedes Mal bei null anfangen. Er soll fruehere Projektideen und Plaene speichern koennen. Dadurch wirkt er mehr wie ein persoenlicher Research Assistant und weniger wie ein normaler Chatbot.

Beispiel:

Beim ersten Mal gibt der Nutzer ein:

```text
Ich moechte ueber Agentic AI Security arbeiten.
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

Beim naechsten Mal fragt der Nutzer:

```text
Kannst du meinen Plan verbessern?
```

Dann kann der Agent auf den alten Plan zugreifen und antworten:

```text
Dein letzter Fokus war Tool-Nutzung bei Agentic AI Security.
Ich wuerde die Forschungsfrage noch enger machen und die Evaluation klarer definieren.
```

Das ist der Unterschied zu einem normalen Chatbot. Ein normaler Chatbot vergisst oft den Kontext. Der Agent soll mit Memory arbeiten und fruehere Projektstaende wiederverwenden.

## 5. Memory in Sprint 1

In Sprint 1 reicht eine einfache Memory. Die semantische Memory mit ChromaDB kann vorbereitet, aber noch nicht voll ausgebaut werden.

### Einfache Sprint-1-Memory

Die erste Version kann Projektplaene lokal speichern, zum Beispiel als JSON-Dateien:

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

### Spaetere semantische Memory mit ChromaDB

Fuer eine spaetere Version ist ChromaDB geplant.

ChromaDB ist eine lokale Vektordatenbank. Sie speichert Texte als Embeddings. Dadurch kann der Agent aehnliche Inhalte wiederfinden, auch wenn der Nutzer andere Woerter benutzt.

Beispiel:

Gespeichert wurde:

```text
Agentic AI Security und Tool-Nutzung
```

Spaeter sucht der Nutzer:

```text
KI-Agenten mit externen Tools absichern
```

ChromaDB kann erkennen, dass beide Themen aehnlich sind.

## 6. Technischer Workflow

Der Workflow sieht so aus:

```text
Nutzer-Eingabe
-> Themenanalyse
-> Memory / Knowledge Base durchsuchen
-> Forschungsfragen generieren
-> Methodik vorschlagen
-> Evaluation planen
-> Risiken erkennen
-> Sprintplan erstellen
-> Checkliste pruefen
-> Export als Markdown / JSON
```

Einfach erklaert:

Der Nutzer gibt eine Idee ein. Der Agent analysiert die Idee. Danach nutzt er gespeicherte Templates, Beispiele und Methodik-Wissen. Anschliessend erstellt er einen Forschungsplan. Am Ende kann der Plan gespeichert oder exportiert werden.

## 7. API-Key

Der Agent kann in zwei Varianten arbeiten.

### Variante 1: Ohne API-Key

Fuer Sprint 1 soll der MVP ohne echten API-Key laufen.

Dann arbeitet der Agent mit:

- gespeicherten Beispieldaten
- festen Templates
- einfachen Regeln
- lokaler Memory

Das ist gut fuer die Praesentation, weil der Agent stabil funktioniert.

### Variante 2: Mit API-Key

Spaeter kann ein LLM ueber eine API genutzt werden, zum Beispiel:

- SAIA API / Academic Cloud
- OpenAI API
- anderes LLM-System der Hochschule

Der API-Key wird gebraucht, damit der Agent Anfragen an ein Sprachmodell schicken kann.

Das LLM kann dann helfen bei:

- besseren Forschungsfragen
- besseren Methodik-Vorschlaegen
- besserer Risikobewertung
- besserer Formulierung des Forschungsplans
- besserer Zusammenfassung der Nutzeridee

Der API-Key darf nicht fest im Code gespeichert werden.

Sichere Varianten:

- Eingabe ueber die Streamlit-Oberflaeche
- Speicherung in einer `.env`-Datei
- Nutzung als Environment Variable

Beispiel:

```text
SAIA_API_KEY=dein_api_key
```

Wichtig: Der API-Key soll nicht in GitHub hochgeladen werden.

## 8. Verwendete Tools

### Python

Python ist die Hauptsprache des Projekts.

Python wird genutzt fuer:

- Agentenlogik
- Verarbeitung der Nutzereingabe
- Erstellung des Forschungsplans
- Export-Funktionen
- Verbindung zu APIs
- Memory-Logik

### Streamlit

Streamlit wird fuer die Benutzeroberflaeche genutzt.

Die Sprint-1-Demo kann folgende Elemente enthalten:

- Eingabefeld fuer Projektidee
- Button `Generate Research Plan`
- Ausgabe des Forschungsplans
- Button `Save to Memory`
- Button `Show Previous Plans`
- Button `Export as Markdown`

Streamlit eignet sich fuer Sprint 1, weil man schnell eine einfache Web-App zeigen kann.

### ChromaDB

ChromaDB ist fuer die spaetere Memory geplant.

Sie kann speichern:

- fruehere Projektideen
- Forschungsfragen
- Methodik-Vorschlaege
- Templates
- Beispiele
- spaeter Dokumente oder Regeln

Der Vorteil ist, dass der Agent aehnliche fruehere Projekte wiederfinden kann.

### LangChain

LangChain verbindet die einzelnen Schritte des Workflows.

Beispiel:

```text
Input -> Analyse -> Memory Search -> Structured Output -> Export
```

LangChain ist also nicht die KI selbst, sondern die Steuerung des Agenten-Workflows.

### LLM / SAIA API

Ein LLM kann optional genutzt werden.

Das LLM kann erzeugen:

- Forschungsfragen
- Methodikempfehlungen
- Risikoerklaerungen
- Sprintplaene
- bessere Formulierungen

Fuer Sprint 1 ist das optional. Der MVP soll auch ohne LLM funktionieren.

### Pydantic / Structured Output

Pydantic sorgt dafuer, dass der Agent strukturierte Ergebnisse erzeugt und nicht nur freien Text.

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

Das ist wichtig, weil die Ergebnisse spaeter exportiert oder weiterverarbeitet werden koennen.

### Markdown / JSON / PDF Export

Der Agent soll Ergebnisse exportieren koennen.

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

Ein moeglicher Demo-Ablauf:

1. Streamlit-App starten.
2. Projektidee eingeben:

```text
Ich moechte zu Agentic AI Security und Tool-Nutzung arbeiten.
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
7. Fruehere Plaene anzeigen.

## 10. Sprint-1-Backlog

### Aufgabe 1: MVP-Workflow pruefen

Akzeptanzkriterien:

- Eine Projektidee kann eingegeben werden.
- Ein strukturierter Plan wird erzeugt.
- Der Plan enthaelt Thema, Forschungsfragen, Methodik, Evaluation, Risiken und Sprintplan.

### Aufgabe 2: Streamlit-Oberflaeche vorbereiten

Akzeptanzkriterien:

- Es gibt ein Eingabefeld.
- Es gibt einen Generate-Button.
- Der generierte Plan wird sichtbar angezeigt.
- Download von Markdown und JSON ist moeglich.

### Aufgabe 3: Lokale Memory vorbereiten

Akzeptanzkriterien:

- Ein generierter Plan kann lokal gespeichert werden.
- Gespeicherte Plaene koennen wieder angezeigt werden.
- Die Struktur ist spaeter fuer ChromaDB erweiterbar.

### Aufgabe 4: Export pruefen

Akzeptanzkriterien:

- Markdown-Export funktioniert.
- JSON-Export funktioniert.
- Dateinamen und Ordnerstruktur sind klar.

### Aufgabe 5: Praesentationsbeispiel vorbereiten

Akzeptanzkriterien:

- Beispielinput ist vorbereitet.
- Beispieloutput ist vorhanden.
- Demo kann ohne API-Key durchgefuehrt werden.

## 11. Sprint-1-Ergebnis

Am Ende von Sprint 1 soll ein praesentierbarer MVP existieren:

```text
Ein Nutzer gibt eine Forschungsprojektidee ein.
Der Agent erstellt daraus einen strukturierten Forschungsplan.
Der Plan kann exportiert und lokal gespeichert werden.
Die Memory ist einfach vorbereitet und kann spaeter mit ChromaDB erweitert werden.
```

Damit ist die Grundlage fuer Sprint 2 gelegt, in dem Themenanalyse, Forschungsfragen und Memory intelligenter gemacht werden koennen.
