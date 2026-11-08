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

## Groove-Werkstatt (`sequenzer.html`)

Die zweite App der Seite: ein Step-Sequencer zum Anklicken, ebenfalls eine einzige HTML-Datei ohne Abhängigkeiten.

- **Drei Spuren** mit je 16 Schritten: Schlagzeug (Kick, Snare, Clap, Hi-Hat, offene Hi-Hat, Tom), Melodie (10 Töne) und Bass (6 Töne) – alles live mit der Web-Audio-API synthetisiert.
- **Immer in der Tonart**: Melodie und Bass folgen Tonart und Skala (Dur/Moll, Pentatonik, Blues, Dorisch). Wer die Tonart wechselt, transponiert den ganzen Groove.
- **Fünf Melodieklänge** (Zupfsynth, E-Piano, Sägezahn, Flächen, Glocke), Echo und gebundene Noten.
- **Tempo und Swing**, Lautstärke/Stumm je Spur, **Würfeln** für Zufallsideen und vier Vorlagen.
- **Export als MIDI-Datei** (1–8 Takte) oder direkt **„Im MIDI-Player öffnen"**, wo der Groove mit echten Instrumenten erklingt.
- **Teilen per Link**: der komplette Groove steckt in der URL. Der letzte Stand wird im Browser gemerkt.

## Nutzung

`index.html` im Browser öffnen — das war's. Für die echten Instrumente wird eine Internetverbindung gebraucht (die Soundfonts kommen per CDN).

## Deployment

Statische Seite, kein Build-Schritt. Auf Vercel als Static Site deploybar.
