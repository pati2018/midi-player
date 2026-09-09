# MIDI-Player

Ein MIDI-Player, der komplett im Browser läuft — eine einzige HTML-Datei, kein Build, kein Server.

## Was er kann

- **Eigener MIDI-Parser**: liest Standard-MIDI-Dateien (Format 0 und 1) direkt im Browser. Ausgewertet werden neben Noten auch Haltepedal (CC64), Kanal-Lautstärke (CC7), Expression (CC11), Panorama (CC10) und All-Notes-Off (CC120/123).
- **Echte Instrumente**: General-MIDI-Soundfonts über [smplr](https://github.com/danigb/smplr) (MusyngKite bzw. FluidR3_GM als schlanke Variante), inklusive Drumkit.
- **Synth-Fallback**: fällt automatisch auf eine eigene Synthese-Engine zurück, wenn die Samples nicht erreichbar sind — pro GM-Familie ein eigenes Patch mit Filterhüllkurve, Vibrato und Stereobreite, dazu synthetisiertes Schlagzeug.
- **Raumklang**: Faltungshall mit vier generierten Impulsantworten (Studio, Zimmer, Konzertsaal, Kirche), dahinter Kompressor und Limiter.
- **Notenrolle**: Canvas-Visualisierung der Noten, Klick springt an die Stelle.
- **Playlist**: mehrere Dateien per Auswahl oder Drag & Drop, Autoplay zum nächsten Titel.
- **Regler** für Tempo, Klangfarbe, Raum, Hall, Brillanz und Lautstärke.

Eine kurze Fassung von „Ode an die Freude" ist als Base64 eingebettet und startet ohne Datei-Upload.

## Nutzung

`index.html` im Browser öffnen — das war's. Für die echten Instrumente wird eine Internetverbindung gebraucht (die Soundfonts kommen per CDN).

## Deployment

Statische Seite, kein Build-Schritt. Auf Vercel als Static Site deploybar.
