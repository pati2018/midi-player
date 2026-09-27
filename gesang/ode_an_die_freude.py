#!/usr/bin/env python3
"""Ode an die Freude mit synthetischem Gesang.

Die Gesangsstimme entsteht mit MBROLA (deutsche Stimme de6): espeak-ng liefert
die Phoneme des Textes, danach bekommt jede Silbe die Tonhoehe und Laenge ihrer
Note (mit Vibrato). Die Begleitung (Klavier, Bass, Streicher) wird als MIDI
erzeugt und mit FluidSynth gerendert; ffmpeg mischt beides zu einer MP3.

Benoetigt: espeak-ng, mbrola, mbrola-de6, fluidsynth, fluid-soundfont-gm,
ffmpeg sowie die Python-Pakete mido und numpy.
"""
import math
import os
import subprocess
import sys
import tempfile

import mido

BPM = 96
BEAT = 60.0 / BPM
INTRO_BEATS = 8
VOICE = "mb-de6"
MBROLA_DB = "/usr/share/mbrola/de6/de6"
SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

VOWELS = {"@", "6", "a", "a:", "e", "e:", "E", "E:", "i", "i:", "I", "o", "o:",
          "O", "u", "u:", "U", "y", "y:", "Y", "2", "2:", "9", "aI", "aU", "OY"}
# Konsonantenpaare, die im Deutschen eine Silbe beginnen koennen.
ONSETS = {("f", "R"), ("f", "l"), ("b", "R"), ("b", "l"), ("t", "R"), ("d", "R"),
          ("g", "R"), ("g", "l"), ("k", "R"), ("k", "l"), ("p", "R"), ("p", "l"),
          ("S", "t"), ("S", "p"), ("S", "l"), ("S", "R"), ("S", "v")}

# Text: eine Zeile pro Phrase (15 Silben).
LYRICS = [
    "Freude, schöner Götterfunken, Tochter aus Elysium,",
    "wir betreten feuertrunken, Himmlische, dein Heiligtum!",
    "Deine Zauber binden wieder, was die Mode streng geteilt;",
    "alle Menschen werden Brüder, wo dein sanfter Flügel weilt.",
]

# Melodie in MIDI-Tonhoehen, eine Silbe je Eintrag: [(tonhoehe, schlaege), ...]
# (mehrere Toene = Melisma). Maennerlage, D-Dur.
D, E, Fs, G, A, lA = 50, 52, 54, 55, 57, 45
PHRASE_A = [[(Fs, 1)], [(Fs, 1)], [(G, 1)], [(A, 1)], [(A, 1)], [(G, 1)], [(Fs, 1)],
            [(E, 1)], [(D, 1)], [(D, 1)], [(E, 1)], [(Fs, 1)]]
END_OPEN = [[(Fs, 1.5)], [(E, 0.5)], [(E, 2)]]
END_CLOSED = [[(E, 1.5)], [(D, 0.5)], [(D, 2)]]
PHRASE_B = [[(E, 1)], [(E, 1)], [(Fs, 1)], [(D, 1)],
            [(E, 1)], [(Fs, 0.5), (G, 0.5)], [(Fs, 1)], [(D, 1)],
            [(E, 1)], [(Fs, 0.5), (G, 0.5)], [(Fs, 1)], [(E, 1)],
            [(D, 1)], [(E, 1)], [(lA, 2)]]
MELODY = [PHRASE_A + END_OPEN, PHRASE_A + END_CLOSED, PHRASE_B, PHRASE_A + END_CLOSED]

# Akkorde je Takt (Grundton, Dur/Moll/Sept), ein Eintrag = 2 Schlaege.
CHORDS_A_OPEN = ["D", "D", "A", "A", "D", "D", "A", "A"]
CHORDS_A_CLOSED = ["D", "D", "A", "A", "D", "D", "A7", "D"]
CHORDS_B = ["A", "A", "A", "D", "A", "D", "E", "A7"]
INTRO_CHORDS = ["D", "D", "A7", "A7"]
CHORDS = INTRO_CHORDS + CHORDS_A_OPEN + CHORDS_A_CLOSED + CHORDS_B + CHORDS_A_CLOSED + ["D", "D"]
CHORD_NOTES = {"D": (50, [62, 66, 69]), "A": (45, [61, 64, 69]), "A7": (45, [61, 64, 67]),
               "E": (40, [59, 64, 68])}


def midi_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)


def phonemes(text):
    out = subprocess.run(["espeak-ng", "-v", VOICE, "-q", "--pho", text],
                         capture_output=True, text=True, check=True).stdout
    phons = []
    for line in out.splitlines():
        parts = line.split()
        if parts:
            phons.append((parts[0], int(parts[1])))
    return phons


def syllabify(phons):
    """Teilt die Phonemfolge in Silben: [onset, vokal, coda]."""
    sylls, pending = [], []
    for p, dur in phons:
        if p == "_":
            # Wortgrenze/Pause: offene Konsonanten gehoeren zur vorigen Silbe.
            if sylls and pending:
                sylls[-1][2].extend(pending)
            elif pending:
                pass
            pending = []
            continue
        if p in VOWELS:
            onset = pending
            while sylls and len(onset) >= 2 and (
                    len(onset) > 2 or tuple(p for p, _ in onset) not in ONSETS):
                sylls[-1][2].append(onset[0])
                onset = onset[1:]
            sylls.append([onset, (p, dur), []])
            pending = []
        else:
            pending.append((p, dur))
    if sylls and pending:
        sylls[-1][2].extend(pending)
    return sylls


def pitch_points(notes, total_ms, prev_hz):
    """Tonhoehenverlauf (Prozent, Hz) fuer einen Vokal mit Vibrato."""
    beats = sum(b for _, b in notes)
    pts, t0 = [], 0.0
    for n, b in notes:
        seg = total_ms * b / beats
        hz = midi_hz(n)
        steps = max(2, int(seg / 25))
        for k in range(steps + 1):
            t = t0 + seg * k / steps
            f = hz
            if t - t0 < 45 and prev_hz:  # kurzer Portamento-Einsatz
                f = prev_hz + (hz - prev_hz) * (t - t0) / 45.0
            age = t - t0
            if age > 180:
                depth = min(1.0, (age - 180) / 250.0) * 0.018
                f *= 1 + depth * math.sin(2 * math.pi * 5.4 * t / 1000.0)
            pts.append((100.0 * t / total_ms, f))
        t0 += seg
        prev_hz = hz
    return pts


def build_pho():
    # Die Anfangskonsonanten der ersten Silbe liegen vor dem ersten Einsatz.
    first_onset = syllabify(phonemes(LYRICS[0]))[0][0]
    lead = sum(min(d, 90) for _, d in first_onset)
    lines = ["_ %d" % (int(INTRO_BEATS * BEAT * 1000) - lead)]
    prev_hz = None
    for text, melody in zip(LYRICS, MELODY):
        sylls = syllabify(phonemes(text))
        if len(sylls) != len(melody):
            sys.exit("Silbenzahl passt nicht: %d statt %d in %r" % (len(sylls), len(melody), text))
        for i, (syl, notes) in enumerate(zip(sylls, melody)):
            onset, (vowel, _), coda = syl
            note_ms = sum(b for _, b in notes) * BEAT * 1000
            nxt_onset = sylls[i + 1][0] if i + 1 < len(sylls) else []
            cons = lambda seq: [(p, min(d, 90)) for p, d in seq]
            coda_c, nxt_c = cons(coda), cons(nxt_onset)
            if i == 0:
                for p, d in cons(onset):
                    lines.append("%s %d 0 %.1f" % (p, d, midi_hz(notes[0][0])))
            rest = 0
            if i == len(sylls) - 1:
                rest = 220  # Atempause am Phrasenende
            vowel_ms = note_ms - sum(d for _, d in coda_c) - sum(d for _, d in nxt_c) - rest
            vowel_ms = max(60, vowel_ms)
            pts = pitch_points(notes, vowel_ms, prev_hz)
            lines.append("%s %d %s" % (vowel, vowel_ms,
                                       " ".join("%.0f %.1f" % (p, f) for p, f in pts)))
            last_hz = midi_hz(notes[-1][0])
            for p, d in coda_c:
                lines.append("%s %d 0 %.1f" % (p, d, last_hz))
            if rest:
                lines.append("_ %d" % rest)
            nxt_hz = midi_hz(melody[i + 1][0][0]) if i + 1 < len(melody) else last_hz
            for p, d in nxt_c:
                lines.append("%s %d 0 %.1f" % (p, d, nxt_hz))
            prev_hz = last_hz
        # Onset der ersten Silbe der naechsten Zeile steht vor ihrem Einsatz:
        # die Atempause wird dafuer gekuerzt.
        if text is not LYRICS[-1]:
            nxt_first = syllabify(phonemes(LYRICS[LYRICS.index(text) + 1]))[0][0]
            shift = sum(min(d, 90) for _, d in nxt_first)
            last = lines.pop()
            dur = int(last.split()[1]) - shift
            if dur > 0:
                lines.append("_ %d" % dur)
    lines.append("_ 3000")
    return "\n".join(lines) + "\n"


def build_midi(path):
    mid = mido.MidiFile(ticks_per_beat=480)
    tempo = mido.MidiTrack()
    tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM)))
    mid.tracks.append(tempo)
    half = 960

    def track(ch, program, vol, events):
        tr = mido.MidiTrack()
        tr.append(mido.Message("program_change", channel=ch, program=program))
        tr.append(mido.Message("control_change", channel=ch, control=7, value=vol))
        tr.append(mido.Message("control_change", channel=ch, control=91, value=60))
        events.sort(key=lambda e: (e[0], e[1] == "on"))
        now = 0
        for t, kind, note, vel in events:
            msg = "note_on" if kind == "on" else "note_off"
            tr.append(mido.Message(msg, channel=ch, note=note, velocity=vel, time=t - now))
            now = t
        mid.tracks.append(tr)

    piano, bass, strings = [], [], []
    for i, name in enumerate(CHORDS):
        root, notes = CHORD_NOTES[name]
        t = i * half
        last = i == len(CHORDS) - 1
        length = half * 2 if last else half
        # Klavier: Akkord auf Schlag 1, Achtel-Nachschlag auf Schlag 2
        for n in notes:
            piano += [(t, "on", n, 62), (t + 440, "off", n, 0)]
            if not last:
                piano += [(t + 480, "on", n, 48), (t + 900, "off", n, 0)]
        bass += [(t, "on", root - 12, 80), (t + length - 20, "off", root - 12, 0)]
        for n in notes:
            strings += [(t, "on", n - 12, 45), (t + length - 10, "off", n - 12, 0)]
    track(0, 0, 90, piano)
    track(1, 32, 100, bass)
    track(2, 48, 70, strings)
    mid.save(path)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "Ode_an_die_Freude_mit_Gesang.mp3"
    with tempfile.TemporaryDirectory() as tmp:
        pho = os.path.join(tmp, "gesang.pho")
        with open(pho, "w") as f:
            f.write(build_pho())
        voice_wav = os.path.join(tmp, "gesang.wav")
        subprocess.run(["mbrola", MBROLA_DB, pho, voice_wav], check=True)
        mid = os.path.join(tmp, "begleitung.mid")
        build_midi(mid)
        band_wav = os.path.join(tmp, "begleitung.wav")
        subprocess.run(["fluidsynth", "-ni", "-g", "0.7", "-r", "44100", "-F", band_wav,
                        SOUNDFONT, mid], check=True, capture_output=True)
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", voice_wav, "-i", band_wav,
            "-filter_complex",
            "[0:a]aresample=44100,highpass=f=90,equalizer=f=3000:t=q:w=1:g=3,"
            "aecho=0.8:0.6:60|110:0.25|0.15,volume=1.6,pan=stereo|c0=c0|c1=c0[v];"
            "[1:a]volume=0.55[b];[v][b]amix=inputs=2:duration=longest:normalize=0,"
            "loudnorm=I=-16:TP=-1.5",
            "-ar", "44100", "-codec:a", "libmp3lame", "-b:a", "192k",
            "-metadata", "title=Ode an die Freude (mit Gesang)",
            "-metadata", "artist=Ludwig van Beethoven / Friedrich Schiller", out,
        ], check=True)
    print(out)


if __name__ == "__main__":
    main()
