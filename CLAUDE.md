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
- **Barrierefreiheit ist Pflicht:** Große Knöpfe, gut lesbar, sofort Klang (draufdrücken und es klingt),
  Bedienung auch per Tastatur bzw. SoundWhacker/Taster.
- **Nachfragen statt raten**, wenn unklar ist, in welchem Repo oder an welcher App
  gearbeitet werden soll.
- **Nicht ungefragt:** Versionsgeschichte umschreiben, Force-Push auf `main`,
  Apps löschen, die nicht ausdrücklich genannt wurden.
- **Kurzbefehle:** „Online?“ oder „V=“ → prüfen, ob die Veröffentlichung (GitHub Actions /
  Pages) fertig ist, und den Link mit `?v=<Nummer>` nennen (umgeht den Zwischenspeicher).
- **„Mach eine stabile Version“** → neuen Branch `stabil-…` anlegen (z. B. über das
  GitHub-Werkzeug „create_branch“). Tags lassen sich nicht hochladen (Fehler 403).
- **SW-Farben** überall gleich: SW1 rot, SW2 orange, SW3 gelb, SW4 grün, SW5 blau.

## Meine Repositories

| Repo | Inhalt | Online |
|------|--------|--------|
| `pati2018/pati2018.github.io` | **Hauptseite „Meine Web-Apps“** mit allen Musik-Apps | https://pati2018.github.io/ |
| `pati2018/midi-player` | MIDI-Player (`index.html`) und Groove-Werkstatt (`sequenzer.html`), MIDI-Demodateien | laut README für Vercel gedacht – noch nicht auf der Übersicht |
| `pati2018/Gitarre` | Smart Instruments | https://pati2018.github.io/Gitarre/?gitarre |
| `pati2018/soundwhacker-looper` | SoundWhacker Smart Control (`SoundWhacker_Spielen.html`), MIGA (`SoundWhacker_Kamera.html`) und Looper (`SoundWhacker_Looper.html`) | https://pati2018.github.io/soundwhacker-looper/ |
| `pati2018/meine-app` | Beispiel/Vorlage für eine einzelne App | https://pati2018.github.io/meine-app/ |

Braucht ein Chat ein Repo, das nicht in der Sitzung ist, holt er es sich dazu
(z. B. `pati2018.github.io` für Änderungen an der Übersicht).

## Hauptseite `pati2018.github.io`

- **Veröffentlichung:** GitHub Pages direkt aus `main`. Nach dem Push ist die
  Änderung nach 1–2 Minuten online.
- **Sicherungen:** Stabile Stände liegen als eigene Branches (`stabil-v1` bis `stabil-v7`,
  `stabil/tischharfe-v1.0`).
  Vor größeren Umbauen einen neuen Stand sichern.
- **Apps:** Die Liste aller Apps steht in `apps.js` (`window.APPS`).
  - Im Repo selbst (je ein Ordner):
    - `tischharfe/` – Tischharfe mit Unterlegnoten (`lieder.js` = Lieder,
      `kopf.js` = Kopfsteuerung, `aufnahme.js` = Video-Aufnahme)
    - `singen/` – Singen mit SoundWhackern
    - `atemklang/` – Atemklang
  - **Achtung:** `tischharfe/lieder.js` lädt auch SoundWhacker Spielen (Gemeinsame Melodie).
    Wer Lieder ändert, ändert sie in beiden Apps – und erhöht in `SoundWhacker_Spielen.html`
    die Nummer bei `../tischharfe/lieder.js?v=…`, sonst bleibt dort die alte Liste im Speicher.
  - **Reihenfolge auf der Übersicht:** neueste oben; Singen vorletzt (`ganzUnten: 1`),
    Atemklang ganz unten (`ganzUnten: 2`).
  - In eigenen Repos (nur verlinkt):
    - Smart Instruments → Repo `pati2018/Gitarre`
    - SoundWhacker Smart Control und MIGA (Mimik, Gestik, Augensteuerung)
      → Repo `pati2018/soundwhacker-looper`
- **Weitere Dateien:** `index.html` (Übersicht), `app.html` (zeigt die Anleitung
  einer App), `anleitungen/<id>.md` (Anleitungen), `style.css`, `theme.js`
  (Hell/Dunkel), `manifest.webmanifest` (Home-Bildschirm), `lib/` (marked, DOMPurify).
- **Neue App hinzufügen (2 Schritte):**
  1. In `apps.js` einen neuen Block in `window.APPS` eintragen
     (`id`, `titel`, `kurz`, `link`, `repo`, `kategorie`, `symbol`, `datum`).
  2. `anleitungen/_vorlage.md` kopieren nach `anleitungen/<id>.md` und ausfüllen.
  Dazu den Ordner in der Tabelle in der `README.md` ergänzen.
- **Inhaltlich:** Auf die Übersicht gehören **nur Musik-Apps**. Andere Apps
  (z. B. das wieder gelöschte Quiz Taubenschutz) kommen woanders hin.

## Repo `soundwhacker-looper`

- Veröffentlichung aus `main` über GitHub Actions („Seite veröffentlichen“).
- **Sicherungen:** `stabil-1` bis `stabil-36` als Tags, ab `stabil-37` als Branches.

## Dieses Repo `midi-player`

- Reine HTML-Dateien, kein Build, kein Server.
- `index.html`: MIDI-Player mit Soundfonts (smplr), Synth-Fallback, Hall,
  Notenrolle, Playlist, Mixer.
- `sequenzer.html`: Groove-Werkstatt (Step-Sequencer), Export als MIDI,
  „Im MIDI-Player öffnen“.
- Details: siehe `README.md`.

## Offene Ideen

- MIDI-Player und Groove-Werkstatt auf die Übersicht „Meine Web-Apps“ bringen.

## Diese Datei gibt es zweimal

Gleicher Inhalt in `pati2018.github.io` und `midi-player`. Bei Änderungen beide
Kopien aktualisieren.
