# GenZone Referral spec ad — Idea A · ASSETS LIST (step 2)

Status: **for approval. Nothing downloaded.** Every file below goes into `ADV/GenZone Ad/assets_in/`
and is logged in `assets_in/CREDITS.md` (source, licence, date, who supplied it).

## 1. Brand (client-supplied, required)

| File | Used in | Have it? |
|---|---|---|
| `brand/genzone-wordmark.svg` (or PNG ≥ 2000 px, transparent) | beat 7 wipe, end card | **No.** I only have a low-res crop from the PDF. Please supply. |
| `brand/genzone-wave-mark.svg` (or PNG ≥ 1500 px, transparent) | beat 7 roll + wipe | **No.** Please supply. |
| Brand colours | whole film | Using #0B1220 / #2B63F0 / #3EC5FF / gold #F5C451→#B8862B (from your brief). |

## 2. Product screens (client-supplied, used as-is)

| File | Used in | Have it? | Treatment |
|---|---|---|---|
| `screenshots/dashboard-earn-pipeline.png` | beat 3 (link field + Copy link) | JPG only, 1487 px, from chat. **Original PNG please.** | Crop to the link card only. **Blur the code** after `/r/`. The pipeline and tracking table are never on screen. |
| `screenshots/what-you-earn.png` | beats 4, 5, 6 (cards, $500 row, rate rack) | JPG only, 1229 px, from chat. **Original PNG please** (ideally a 2× retina capture, since the $ rows get zoomed ~2.5×). | Crops of the two cards and six rows, plus the terms sentence for the beat 6 lower line. |

No real names appear: the tracking table isn't used, and the only code on screen is blurred.

## 3. Reference (have it)

| File | Use |
|---|---|
| `reference/Genzone_1st_Draft_01-10-2026.pdf` | look and feel only; nothing from it goes on screen |

## 4. Fonts

| Font | Use | Status |
|---|---|---|
| SF Pro Display (Heavy, Bold, Semibold) | all kinetic type + end card | **Not installed here.** Its Apple licence limits use outside Apple-platform UI. Supply the .otf files if you're licensed; otherwise **Inter Display** (OFL, free) as a stand-in. |

## 5. Photos

**None.** Idea A is type + real screens + logo. Nothing to download from Unsplash/Pexels.

## 6. Audio

| Item | Source | Status |
|---|---|---|
| VO, 2 takes on the chosen voice | ElevenLabs | Waiting on voice pick + API access (not reachable from this machine; no key). |
| Music, ~24 s, 112 BPM | made in code by me | after the VO |
| SFX, ~33 cues (list below) | **your library only** | Library path still `[ŚCIEŻKA DO TWOJEJ BIBLIOTEKI SFX]`. Please give the path, or upload the folder. |

SFX I'll pull from the library (by category, for beats 1–9):
- whoosh short/air ×10
- whip/swish ×3
- hit soft ×3
- hit deep ×2
- UI click ×1
- glass tick ×1
- coin/cash tick ×7, pitched up through the rate rack
- shimmer ×1
- logo sting ×1
- riser ×2
- end chord: musical, made with the score

## 7. Made-by card

| Item | Status |
|---|---|
| "made by / Kacper Semik" animated card, ~2 s | I'll build it in the same type system. If you have an existing logo or animation for it, send it and I'll use that instead. |

---

### To approve step 2, please confirm or send:
1. Official **wordmark + wave mark** files.
2. **Original PNG** screenshots (2× if possible).
3. **Font:** SF Pro files, or OK to use Inter Display.
4. **SFX library path** (or upload).
5. **Voice:** which of V1–V4 to audition, and how VO runs: ElevenLabs access from here (allow `api.elevenlabs.io` in the environment's network settings + add an `ELEVENLABS_API_KEY` secret) or you generate on your side.
6. **Script A:** approve as written, or send edits.
