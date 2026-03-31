# TRR-Flow – Anleitung: Lokaler Speicher-Server

## Übersicht

Da Browser aus Sicherheitsgründen keine Dateien direkt in beliebige Ordner schreiben dürfen, übernimmt ein kleines Python-Skript (`server.py`) diese Aufgabe. Es erfüllt dabei **zwei Funktionen gleichzeitig**:

1. **HTML ausliefern** — die Fragebögen werden über `http://localhost:5050` geöffnet, nicht per Doppelklick. Das ist technisch notwendig, damit die Speicherfunktion funktioniert.
2. **JSON speichern** — ausgefüllte Fragebögen werden automatisch unter `json/<VP-ID>.json` im selben Ordner abgelegt.

> ⚠ **Wichtig:** Die HTML-Datei darf **nicht** per Doppelklick geöffnet werden. Browser blockieren in diesem Fall (`file://`-Protokoll) alle Speicheranfragen an den Server. Immer über die URL `http://localhost:5050/Fragebögen.html` öffnen — der Server erledigt das beim Start automatisch.

---

## Voraussetzungen

- **Python 3.7 oder neuer** muss installiert sein.
  Prüfen im Terminal: `python --version` oder `python3 --version`
- Keine zusätzlichen Pakete notwendig — nur die Python-Standardbibliothek wird verwendet.

---

## Ordnerstruktur

Beide Dateien müssen im **selben Ordner** liegen:

```
studie/
├── server.py
├── Fragebögen.html
└── json/              ← wird automatisch angelegt beim ersten Speichern
```

---

## Server starten

### Windows
```
python server.py
```
oder Doppelklick auf `server.py` (falls Python mit `.py`-Dateien verknüpft ist).

### macOS / Linux
```
python3 server.py
```

Der Server startet, öffnet den Browser **automatisch** mit dem Fragebogen und zeigt folgende Meldung im Terminal:

```
╔══════════════════════════════════════════════════════════╗
║   TRR-Flow Speicher-Server                              ║
║                                                         ║
║   Fragebogen öffnen:                                    ║
║   http://localhost:5050/Fragebögen.html                 ║
║                                                         ║
║   JSON-Zielordner: /pfad/zum/ordner/json                ║
║   Beenden mit Strg+C                                    ║
╚══════════════════════════════════════════════════════════╝
```

Das Terminal-Fenster muss während der gesamten Datenerhebung **offen bleiben**.

### Alternativer Port (optional)
Falls Port 5050 bereits belegt ist:
```
python3 server.py 8080
```
> ⚠ Wenn Sie den Port ändern, muss auch in `Fragebögen.html` die Zeile
> `const SERVER = 'http://localhost:5050/save';`
> auf den neuen Port angepasst werden.

---

## Fragebogen öffnen

Der Browser öffnet sich beim Serverstart automatisch. Falls nicht, die URL manuell eingeben:

```
http://localhost:5050/Fragebögen.html
```

> ⚠ Niemals `Fragebögen.html` per Doppelklick oder Drag & Drop in den Browser ziehen — das verhindert das Speichern.

---

## Ablauf pro Versuchsperson

1. Server starten — Browser öffnet sich automatisch.
2. **VP-ID** oben im Fragebogen eintragen (z. B. `VP01`).
3. Fragebogen mit der Versuchsperson ausfüllen.
4. Auf **„Als JSON exportieren"** klicken.

Bei Erfolg erscheint ein grüner Toast im Browser:
```
✓ Gespeichert: json/VP01.json
```

Im Terminal ist gleichzeitig zu sehen:
```
[14:32:07]  ✓  Gespeichert → /pfad/zum/ordner/json/VP01.json
```

---

## Dateinamen-Schema

Die JSON-Datei wird automatisch nach der **VP-ID** benannt, die im Feld *VP-ID* oben im Fragebogen eingetragen wurde:

| VP-ID im Formular | Gespeicherte Datei        |
|-------------------|---------------------------|
| `VP01`            | `json/VP01.json`          |
| `VP12`            | `json/VP12.json`          |
| *(leer)*          | `json/unbekannt.json`     |

> ⚠ Wird dieselbe VP-ID zweimal verwendet, überschreibt die neue Datei die alte. Immer eine eindeutige ID vergeben.

---

## Fallback: Server nicht erreichbar

Falls der Server nicht läuft oder die HTML-Datei versehentlich per Doppelklick geöffnet wurde, löst der Fragebogen automatisch einen **Browser-Download** ins Downloads-Verzeichnis aus. Ein orangener Hinweis erscheint:

```
⚠ Server nicht erreichbar – in Downloads gespeichert
```

In diesem Fall: Datei manuell in den `json/`-Ordner verschieben und beim nächsten Mal die HTML über `http://localhost:5050/Fragebögen.html` öffnen.

---

## Server beenden

Im Terminal-Fenster nach Abschluss der Datenerhebung: **Strg + C**

```
^C
Server beendet.
```

---

## Häufige Probleme

| Problem | Mögliche Ursache | Lösung |
|---|---|---|
| Orangener Toast, Fallback auf Download | HTML per Doppelklick geöffnet (`file://`) | Browser schließen, Server starten, URL `http://localhost:5050/Fragebögen.html` verwenden |
| Orangener Toast, Fallback auf Download | Server läuft nicht | `server.py` starten, Seite neu laden, erneut speichern |
| Browser öffnet sich nicht automatisch | Systemeinstellung | URL manuell eingeben: `http://localhost:5050/Fragebögen.html` |
| `python: command not found` | Falscher Befehl für das System | `python3 server.py` versuchen |
| `Address already in use` | Port 5050 belegt | `python3 server.py 8080` und HTML anpassen |
| Datei wird überschrieben | Doppelte VP-ID | Eindeutige VP-IDs vergeben |
| `json/`-Ordner fehlt | Erster Start | Wird automatisch angelegt — kein Handlungsbedarf |
