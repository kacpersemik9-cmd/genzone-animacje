#!/usr/bin/env python3
"""Generates index.html for the GenZone 60s promo.

Every screen shot is a crop of a real GenZone screen (assets/screens/*.png,
taken unchanged from the storyboard PDF). Rects are in source pixels (1920x1032).
Run: python3 build.py
"""
import json
import re

W, H = 1920, 1080
SRC_H = 1032
CENTER = (960, 400)        # where the focused region lands
MAX_W, MAX_H, MAX_S = 1680, 540, 3.0
PAD_X, PAD_Y = 14, 0       # source px of breathing room around a region

# (start, duration, kind, payload)
WORD, SHOT = "word", "shot"
TIMELINE = [
    (0, 2, WORD, "Your business is <b>global.</b>"),
    (2, 2, WORD, "Is your <b>company?</b>"),
    (4, 3, SHOT, dict(img="p19", rect=(596, 557, 460, 44), mode="wide",
                      cap="Stuck on the <b>paperwork?</b>")),
    (7, 2, WORD, "GenZone <b>handles it.</b>"),
    (9, 3, SHOT, dict(img="p8", rect=(632, 370, 435, 44), mode="push",
                      cap="<b>Dubai:</b> free-zone company, trade licence, residence visas")),
    (12, 3, SHOT, dict(img="p8", rect=(1100, 370, 430, 44), mode="pan", from_rect=(632, 370, 435, 44),
                       cap="<b>US LLC:</b> formation, EIN, registered agent")),
    (15, 2, WORD, "Pick <b>UAE</b> or <b>US.</b>"),
    (17, 3, SHOT, dict(img="p8", rect=(632, 422, 310, 120), mode="push",
                       cap="Licence only, or add <b>residence visas</b>")),
    (20, 3, SHOT, dict(img="p8", rect=(1100, 422, 200, 120), mode="push",
                       cap="Basic, Advanced or <b>Done-For-You</b>")),
    (23, 2, WORD, "<b>End to end.</b>"),
    (25, 4, SHOT, dict(img="p19", rect=(596, 623, 465, 66), mode="wide",
                       cap="Licence, visas, <b>bank account intro</b>")),
    (29, 3, SHOT, dict(img="p19", rect=(596, 645, 465, 44), mode="pan", from_rect=(596, 623, 465, 66),
                       cap="Know the <b>real cost</b> before you commit")),
    (32, 2, WORD, "No need to <b>fly to Dubai.</b>"),
    (34, 3, SHOT, dict(img="p19", rect=(1128, 623, 465, 44), mode="wide",
                       cap="A <b>real person</b> on WhatsApp")),
    (37, 4, SHOT, dict(img="p19", rect=(1128, 645, 465, 44), mode="pan", from_rect=(1128, 623, 465, 44),
                       cap="Compare <b>Dubai vs US.</b> No guessing.")),
    (41, 2, WORD, "<b>Fully remote.</b>"),
    (43, 3, SHOT, dict(img="p15", rect=(1293, 466, 236, 54), mode="push",
                       cap="See what <b>clients say</b> on Google")),
    (46, 3, SHOT, dict(img="p15", rect=(1293, 524, 236, 54), mode="pan", from_rect=(1293, 466, 236, 54),
                       cap="Free <b>guides &amp; walkthroughs</b>")),
]
END_START, END_DUR = 49, 11
TOTAL = END_START + END_DUR


def fit_scale(rect):
    _, _, rw, rh = rect
    return min(MAX_S, MAX_W / (rw + 2 * PAD_X), MAX_H / (rh + 2 * PAD_Y))


def cam(rect, s):
    """Transform that puts rect's centre on CENTER at scale s."""
    rx, ry, rw, rh = rect
    return dict(x=round(CENTER[0] - (rx + rw / 2) * s, 2),
                y=round(CENTER[1] - (ry + rh / 2) * s, 2),
                scale=round(s, 4))


def clip_for(rect, s):
    _, _, rw, rh = rect
    dw, dh = (rw + 2 * PAD_X) * s, (rh + 2 * PAD_Y) * s
    left, top = CENTER[0] - dw / 2, CENTER[1] - dh / 2
    return f"inset({top:.1f}px {W - left - dw:.1f}px {H - top - dh:.1f}px {left:.1f}px round 22px)"


def words(html):
    """Wrap each word in a span; words inside <b> get the accent class."""
    out = []
    for m in re.finditer(r"<b>(.*?)</b>|([^<\s]+)", html):
        if m.group(1):
            out += [f'<span class="w a">{w}</span>' for w in m.group(1).split()]
        else:
            out.append(f'<span class="w">{m.group(2)}</span>')
    return " ".join(out)


clips, tweens = [], []
for i, (t, d, kind, p) in enumerate(TIMELINE):
    cid = f"c{i:02d}"
    if kind == WORD:
        clips.append(
            f'<div id="{cid}" class="clip scene" data-start="{t}" data-duration="{d}" data-track-index="1">'
            f'<div class="card"><div class="big">{words(p)}</div></div></div>')
        tweens.append(f'tl.fromTo("#{cid} .w", {{yPercent: 110, opacity: 0}}, '
                      f'{{yPercent: 0, opacity: 1, duration: 0.32, ease: "back.out(1.7)", stagger: 0.07}}, {t});')
        tweens.append(f'tl.fromTo("#{cid} .card", {{scale: 1}}, {{scale: 1.05, duration: {d}, ease: "none"}}, {t});')
        continue

    rect = p["rect"]
    s = fit_scale(rect)
    end = cam(rect, s)
    final_clip = clip_for(rect, s)
    clips.append(
        f'<div id="{cid}" class="clip scene" data-start="{t}" data-duration="{d}" data-track-index="1">'
        f'<div class="win"><img id="{cid}-img" class="cam" src="assets/screens/{p["img"]}.png" alt=""></div>'
        f'<div class="cap">{words(p["cap"])}</div></div>')
    sel = f"#{cid} .cam"
    if p["mode"] == "wide":
        k = H / SRC_H
        start = dict(x=round(W / 2 - W / 2 * k, 2), y=0, scale=round(k, 4))
        tweens.append(f'tl.fromTo("#{cid} .win", {{clipPath: "inset(0px 0px 0px 0px round 0px)"}}, '
                      f'{{clipPath: "{final_clip}", duration: 0.7, ease: "expo.inOut"}}, {t + 0.15});')
        zoom_at, zoom_dur = t + 0.15, 0.7
    else:
        start = cam(rect, s * 0.8) if p["mode"] == "push" else cam(p["from_rect"], s)
        tweens.append(f'tl.set("#{cid} .win", {{clipPath: "{final_clip}"}}, {t});')
        zoom_at, zoom_dur = t, 0.5
    tweens.append(f'tl.fromTo("{sel}", {json.dumps(start)}, '
                  f'{{...{json.dumps(end)}, duration: {zoom_dur}, ease: "expo.out"}}, {zoom_at});')
    drift = cam(rect, s * 1.035)
    tweens.append(f'tl.to("{sel}", {{...{json.dumps(drift)}, duration: {round(d - (zoom_at - t) - zoom_dur, 2)}, '
                  f'ease: "none"}}, {round(zoom_at + zoom_dur, 2)});')
    tweens.append(f'tl.fromTo("#{cid} .cap .w", {{yPercent: 100, opacity: 0}}, '
                  f'{{yPercent: 0, opacity: 1, duration: 0.3, ease: "power3.out", stagger: 0.04}}, {round(zoom_at + 0.35, 2)});')

# End card
e = END_START
clips.append(
    f'<div id="end" class="clip scene" data-start="{e}" data-duration="{END_DUR}" data-track-index="1">'
    '<div class="endwrap">'
    '<img id="logo" src="assets/screens/logo.png" alt="GenZone">'
    '<div id="tag" class="tag"><span class="w">Your company.</span> <span class="w">Anywhere.</span> '
    '<span class="w a">Done for you.</span></div>'
    '<div id="cta" class="cta">Book your free consultation at <b>genzone.com</b></div>'
    '</div></div>')
tweens += [
    f'tl.fromTo("#logo", {{scale: 1.25, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.6, ease: "expo.out"}}, {e});',
    f'tl.fromTo("#tag .w", {{yPercent: 100, opacity: 0}}, {{yPercent: 0, opacity: 1, duration: 0.35, '
    f'ease: "back.out(1.7)", stagger: 0.6}}, {e + 1});',
    f'tl.fromTo("#cta", {{y: 40, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {e + 3});',
    f'tl.to("#cta", {{scale: 1.04, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 3}}, {e + 5});',
]

html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Inter";
        src: url("assets/fonts/inter-var.woff2") format("woff2");
        font-weight: 100 900;
        font-style: normal;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0a1226; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0a1226;
               font-family: "Inter", sans-serif; color: #ffffff; }}
      .scene {{ position: absolute; inset: 0; background: #0a1226; }}
      .card {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }}
      .big {{ font-size: 156px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.05;
              text-align: center; max-width: 1700px; }}
      .w {{ display: inline-block; }}
      .a {{ color: #4f8bff; }}
      .win {{ position: absolute; inset: 0; overflow: hidden; }}
      .cam {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1032px; transform-origin: 0 0; }}
      .cap {{ position: absolute; left: 140px; right: 140px; top: 760px; text-align: center;
              font-size: 72px; font-weight: 800; letter-spacing: -0.025em; line-height: 1.12; }}
      .endwrap {{ position: absolute; inset: 0; display: flex; flex-direction: column;
                  align-items: center; justify-content: center; gap: 44px; }}
      #logo {{ display: block; width: 820px; height: 220px;
               -webkit-mask-image: radial-gradient(ellipse 60% 70% at 50% 50%, #000 62%, transparent 100%);
               mask-image: radial-gradient(ellipse 60% 70% at 50% 50%, #000 62%, transparent 100%); }}
      .tag {{ font-size: 76px; font-weight: 800; letter-spacing: -0.03em; }}
      .cta {{ display: block; padding: 26px 52px; border-radius: 999px; background: #2d65f0;
              font-size: 44px; font-weight: 600; color: #ffffff; }}
      .cta b {{ font-weight: 800; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      {chr(10).join("      " + c for c in clips).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in tweens).strip()}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)
print(f"wrote index.html: {len(clips)} clips, {TOTAL}s")
