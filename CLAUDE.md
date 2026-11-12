# CLAUDE.md – Gedächtnis für alle Chats

Diese Datei liest jeder neue Chat zuerst. Sie beschreibt, wie wir zusammenarbeiten
und welche Projekte es gibt. **Wenn sich etwas Wichtiges ändert (neue App, neues
Repo, neue Regel), diese Datei mit aktualisieren.**

## So arbeiten wir

- **Name:** Du heißt **Riff**. Antworten beginnen mit „Riff hier:“.
- **Sprache:** Deutsch, einfache und klare Sätze, keine Fachbegriffe ohne Erklärung.
  Nachrichten kommen oft per Spracheingabe vom iPhone/iPad – Tippfehler und
  falsch erkannte Wörter wohlwollend deuten.
- **Ergebnis zuerst:** Erst sagen, was fertig ist und wo man es sieht (Link), dann Details.
- **Testen:** Apps vor dem Veröffentlichen im Browser prüfen, vor allem auf
  **iPad und iPhone** (Hoch- und Querformat).
- **Barrierefreiheit ist Pflicht:** Große Knöpfe, gut lesbar, Vorlesen wo sinnvoll,
  Bedienung auch per Tastatur bzw. SoundWhacker/Taster.
- **Nachfragen statt raten**, wenn unklar ist, in welchem Repo oder an welcher App
  gearbeitet werden soll.
- **Nicht ungefragt:** Versionsgeschichte umschreiben, Force-Push auf `main`,
  Apps löschen, die nicht ausdrücklich genannt wurden.

## Meine Repositories

| Repo | Inhalt | Online |
|------|--------|--------|
| `pati2018/pati2018.github.io` | **Hauptseite „Meine Web-Apps“** mit allen Musik-Apps | https://pati2018.github.io/ |
| `pati2018/midi-player` | MIDI-Player (`index.html`) und Groove-Werkstatt (`sequenzer.html`), MIDI-Demodateien | laut README für Vercel gedacht – noch nicht auf der Übersicht |
| `pati2018/meine-app` | Beispiel/Vorlage für eine einzelne App | https://pati2018.github.io/meine-app/ |

Braucht ein Chat ein Repo, das nicht in der Sitzung ist, holt er es sich dazu
(z. B. `pati2018.github.io` für Änderungen an der Übersicht).

## Hauptseite `pati2018.github.io`

- **Veröffentlichung:** GitHub Pages direkt aus `main`. Nach dem Push ist die
  Änderung nach 1–2 Minuten online.
- **Sicherungen:** Stabile Stände liegen als eigene Branches (`stabil-v…`).
  Vor größeren Umbauen einen neuen Stand sichern.
- **Apps (je ein Ordner):**
  - `tischharfe/` – Tischharfe mit Unterlegnoten (`lieder.js` = Lieder,
    `kopf.js` = Kopfsteuerung, `aufnahme.js` = Video-Aufnahme)
  - `smart-instruments/` – Smart Instruments
  - `soundwhacker-spielen/` – SoundWhacker Smart Control
  - `miga/` – MIGA: Mimik, Gestik, Augensteuerung
  - `singen/` – Singen mit SoundWhackern
  - `atemklang/` – Atemklang
- **Neue App hinzufügen (2 Schritte):**
  1. In `apps.js` einen neuen Block in `window.APPS` eintragen
     (`id`, `titel`, `kurz`, `link`, `repo`, `kategorie`, `symbol`, `datum`).
  2. `anleitungen/_vorlage.md` kopieren nach `anleitungen/<id>.md` und ausfüllen.
  Dazu den Ordner in der Tabelle in der `README.md` ergänzen.
- **Inhaltlich:** Auf die Übersicht gehören **nur Musik-Apps**. Andere Apps
  (z. B. das wieder gelöschte Quiz Taubenschutz) kommen woanders hin.

## Dieses Repo `midi-player`

- Reine HTML-Dateien, kein Build, kein Server.
- `index.html`: MIDI-Player mit Soundfonts (smplr), Synth-Fallback, Hall,
  Notenrolle, Playlist, Mixer.
- `sequenzer.html`: Groove-Werkstatt (Step-Sequencer), Export als MIDI,
  „Im MIDI-Player öffnen“.
- Details: siehe `README.md`.

## Offene Ideen

- MIDI-Player und Groove-Werkstatt auf die Übersicht „Meine Web-Apps“ bringen.
- Diese Datei auch ins Repo `pati2018.github.io` legen, damit Chats dort sie
  ebenfalls lesen.
