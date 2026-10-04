#!/usr/bin/env python3
"""Original score for the GenZone referral spec ad #2 ("The link is the product"), synthesised in code.

120 BPM, 23 s. E minor -> G major lift at the "$500" cut (8.6 s), drums out for
beat 4 (6.2-8.6 s), full F chord lands with the wave wipe (16.8 s) and rings
under the end card and made-by card. Writes assets/music_raw.wav (48 kHz stereo).
Loudness is normalised afterwards with ffmpeg loudnorm (-14 LUFS / -1 dBTP).
"""
import wave
import numpy as np

SR = 48000
DUR = 23.0
BPM = 120
BEAT = 60 / BPM
N = int(SR * DUR)
t = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a, d, s, r, hold):
    """ADSR envelope of total length n samples."""
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    h = max(int(hold * SR) - a - d, 0)
    e = np.concatenate([np.linspace(0, 1, a, False), np.linspace(1, s, d, False),
                        np.full(h, s), np.linspace(s, 0, r)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))


def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def saw(f, n, detune=0.0):
    ph = np.cumsum(np.full(n, f * (1 + detune) / SR))
    return 2 * (ph % 1) - 1


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):          # one-pole, fine for short notes
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def pad_chord(notes, start, length, gain=0.06, cutoff=1800):
    n = int(length * SR)
    s = np.zeros(n)
    for m in notes:
        for dt in (-0.004, 0.0, 0.005):
            s += saw(midi(m), n, dt)
    s = lowpass(s, cutoff) * env(n, 0.25, 0.3, 0.8, 0.6, length - 0.6)
    add(s, start, -0.3, gain)
    add(s, start, 0.3, gain)


def pluck(m, start, gain=0.11, pan=0.0):
    n = int(0.45 * SR)
    s = lowpass(saw(midi(m), n) + 0.5 * saw(midi(m + 12), n, 0.002), 3200)
    s *= np.exp(-np.arange(n) / SR * 9)
    add(s, start, pan, gain)


def sub(m, start, length, gain=0.32):
    n = int(length * SR)
    s = np.sin(2 * np.pi * midi(m) * np.arange(n) / SR) * env(n, 0.005, 0.08, 0.7, 0.05, length)
    add(s, start, 0, gain)


def clap(start, gain=0.16):
    n = int(0.18 * SR)
    rng = np.random.default_rng(int(start * 1000))
    s = rng.standard_normal(n)
    s = s - lowpass(s, 900)                      # rough high-pass
    s *= np.exp(-np.arange(n) / SR * 28)
    add(s, start, -0.15, gain)
    add(s, start + 0.012, 0.15, gain * 0.6)


def kick(start, gain=0.5):
    n = int(0.35 * SR)
    k = np.arange(n) / SR
    f = 45 + 90 * np.exp(-k * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 9)
    add(s, start, 0, gain)


# bars of 4 beats. (root midi, chord notes)
BAR = 4 * BEAT
PROG = [(40, [64, 67, 71]),   # Em      0.0   macro on the link
        (36, [60, 64, 67]),   # C       2.0
        (43, [62, 67, 71]),   # G       4.0   pull-out
        (38, [62, 66, 69]),   # D       6.0   glide down (drums out)
        (43, [67, 71, 74]),   # G lift  8.0   "$500" lands ~8.6
        (38, [66, 69, 74]),   # D       10.0  "$400"
        (40, [67, 71, 76]),   # Em      12.0  attached / fixed
        (36, [64, 67, 72]),   # C       14.0
        (38, [66, 69, 74])]   # D       16.0  -> logo chord at 18.0
for b, (root, chord) in enumerate(PROG):
    st = b * BAR
    pad_chord(chord, st, BAR + 0.3, gain=0.05 if b < 4 else 0.065)
    for k in range(8):                                   # 8th-note sub pulse
        sub(root, st + k * BEAT / 2, BEAT / 2 * 0.9, 0.22 if b == 3 else 0.3)
    arp = chord + [chord[1] + 12]
    for k in range(8):                                   # pluck arpeggio
        pluck(arp[k % 4] + (12 if b >= 4 else 0), st + k * BEAT / 2, pan=(-0.4, 0.4)[k % 2])
    if b != 3:                                           # drums drop for beat 4
        for k in range(4):
            kick(st + k * BEAT, 0.45 if k in (0, 2) else 0.0)
            if k in (1, 3):
                clap(st + k * BEAT)

# final F major chord on the wipe, ringing under end card + made-by card
WIPE = 18.0
kick(WIPE, 0.6)
n = int((DUR - WIPE) * SR)
fin = np.zeros(n)
for m in (55, 62, 67, 71, 74, 79):
    for dt in (-0.004, 0.0, 0.006):
        fin += saw(midi(m), n, dt)
fin = lowpass(fin, 2400) * env(n, 0.02, 1.5, 0.45, 4.0, n / SR - 4.0)
add(fin, WIPE, -0.25, 0.05)
add(fin, WIPE, 0.25, 0.05)
sub(31, WIPE, DUR - WIPE - 0.5, 0.35)

# master: gentle fade out, peak normalise to -3 dBFS (loudnorm does the rest)
fade = np.ones(N)
fo = int(1.6 * SR)
fade[-fo:] = np.linspace(1, 0, fo)
L *= fade
R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.7, R / peak * 0.7
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open("assets/music_raw.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/music_raw.wav", DUR, "s")
