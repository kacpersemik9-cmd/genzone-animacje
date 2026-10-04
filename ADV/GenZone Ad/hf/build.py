#!/usr/bin/env python3
"""GenZone Referral Program — spec ad, Idea A "You already get asked". PREVIEW v1, 16:9.

Picture + original score only (no VO, no SFX in this pass). Every on-screen element is
kinetic type, a real dashboard screenshot (cropped, code blurred) or the GenZone logo.
Run: python3 build.py   ->  index.html
"""
W, H = 1920, 1080
EARN = ("assets/img/what-you-earn.jpg", 1229, 389)
LINK = ("assets/img/linkcard.png", 590, 112)
MARK = "assets/img/wave-mark_from-pdf.png"
WORD = "assets/img/wordmark_from-pdf.png"
GOLD_ROW = (48, 191, 553, 39)        # Business License + 1 Residency Visa — $500 per sale
DUBAI_ROWS = [(48, 152, 553, 39), (48, 191, 553, 39), (48, 230, 553, 39)]
US_ROWS = [(634, 152, 552, 39), (634, 191, 552, 39), (634, 230, 552, 39)]
CARDS = {"cD": (40, 67, 570, 216), "cU": (626, 67, 569, 216)}

clips, tw = [], []


def clip(cid, start, dur, html, track=2, cls="scene"):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{start}" data-duration="{dur}" '
                 f'data-track-index="{track}">{html}</div>')


def T(s):
    tw.append(s)


def words(text, cls="w"):
    out = []
    for tok in text.split(" "):
        c = cls
        if tok.startswith("*"):
            tok, c = tok[1:], cls + " acc"
        if tok.startswith("$"):
            c = cls + " gold"
        out.append(f'<span class="{c}">{tok}</span>')
    return " ".join(out)


def crop_div(img, x, y, w, h, s, extra=""):
    return (f'<div class="crop" style="width:{w * s:.0f}px;height:{h * s:.0f}px;'
            f'background-image:url({img[0]});background-size:{img[1] * s:.0f}px {img[2] * s:.0f}px;'
            f'background-position:-{x * s:.0f}px -{y * s:.0f}px;{extra}"></div>')


# ---------------------------------------------------------------- background
clip("bg", 0, 24, '<div class="glow" id="glow"></div><div class="leak tl"></div><div class="leak br"></div>',
     track=0, cls="bgl")
T('tl.fromTo("#glow", {x: -260, y: -40, scale: 1}, {x: 260, y: 60, scale: 1.15, duration: 24, ease: "sine.inOut"}, 0);')
clip("grid", 3.6, 10.6, '<div class="gridlines"></div>', track=1, cls="bgl")
T('tl.fromTo("#grid .gridlines", {opacity: 0}, {opacity: 1, duration: 0.4}, 3.6);')
T('tl.to("#grid .gridlines", {opacity: 0, duration: 0.3}, 13.9);')

# ---------------------------------------------------------------- 1. the question (0 - 2.45)
clip("b1", 0, 2.45, f'<div class="qwrap" id="q1"><div class="q">{words("How do I open a")}</div>'
     f'<div class="q">{words("*Dubai *company?")}</div></div>')
T('tl.fromTo("#q1 .w", {scale: 1.7, opacity: 0, filter: "blur(22px)"}, {scale: 1, opacity: 1, filter: "blur(0px)", '
  'duration: 0.42, ease: "expo.out", stagger: 0.11}, 0.15);')
T('tl.fromTo("#q1", {scale: 1}, {scale: 1.07, duration: 2.0, ease: "none"}, 0);')
T('tl.to("#q1", {scale: 3.4, opacity: 0, filter: "blur(28px)", duration: 0.38, ease: "power3.in"}, 2.07);')

# ---------------------------------------------------------------- 2. whip to US LLC (2.4 - 3.65)
clip("b2", 2.4, 1.25, f'<div class="qwrap" id="q2"><div class="q">{words("…or a *US *LLC?")}</div></div>')
T('tl.fromTo("#q2", {x: 1100, filter: "blur(40px)", opacity: 0}, {x: 0, filter: "blur(0px)", opacity: 1, '
  'duration: 0.34, ease: "expo.out"}, 2.4);')
T('tl.to("#q2", {x: -1100, filter: "blur(40px)", opacity: 0, duration: 0.26, ease: "power3.in"}, 3.39);')

# ---------------------------------------------------------------- 3. your own link (3.6 - 6.25)
S3 = 2.6
lw, lh = LINK[1] * S3, LINK[2] * S3
copy = crop_div(LINK, 17, 58, 101, 36, S3, "position:absolute;left:%dpx;top:%dpx" % (17 * S3, 58 * S3))
clip("b3", 3.6, 2.65,
     f'<div class="stage3d"><div class="shot" id="lk" style="left:{960 - lw / 2:.0f}px;top:{430 - lh / 2:.0f}px;'
     f'width:{lw:.0f}px;height:{lh:.0f}px"><img src="{LINK[0]}" alt="GenZone referral link">'
     f'<div class="sweep" id="sweep" style="left:{17 * S3:.0f}px;top:{11 * S3:.0f}px;width:{555 * S3:.0f}px;height:{36 * S3:.0f}px"></div>'
     f'<div id="copyBtn">{copy}</div></div></div>'
     f'<div class="cap" id="cap3">{words("Send them to *GenZone,")} <br>{words("with your own link.")}</div>')
T('tl.fromTo("#lk", {rotationX: 72, y: 380, opacity: 0, scale: 0.8}, {rotationX: 0, y: 0, opacity: 1, scale: 1, '
  'duration: 0.75, ease: "back.out(1.3)"}, 3.6);')
T('tl.to("#lk", {scale: 1.12, duration: 1.9, ease: "none"}, 4.35);')
T('tl.fromTo("#sweep", {backgroundPosition: "-120% 0"}, {backgroundPosition: "220% 0", duration: 0.7, ease: "power2.inOut"}, 4.55);')
T('tl.fromTo("#copyBtn .crop", {scale: 1}, {scale: 0.9, duration: 0.09, ease: "power2.out", transformOrigin: "50% 50%"}, 5.3);')
T('tl.to("#copyBtn .crop", {scale: 1, duration: 0.25, ease: "back.out(3)"}, 5.39);')
T('tl.fromTo("#copyBtn .crop", {boxShadow: "0 0 0 0px rgba(62,197,255,0)"}, {boxShadow: "0 0 0 3px #3EC5FF, 0 0 30px rgba(62,197,255,0.8)", duration: 0.15}, 5.3);')
T('tl.fromTo("#cap3 .w", {y: 50, opacity: 0, filter: "blur(10px)"}, {y: 0, opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out", stagger: 0.06}, 3.85);')
T('tl.to("#b3 .stage3d, #cap3", {scale: 1.6, opacity: 0, filter: "blur(18px)", duration: 0.3, ease: "power3.in"}, 5.95);')

# ---------------------------------------------------------------- 4. when they form a company, you earn (6.2 - 8.65)
S4 = 1.22
ew, eh = EARN[1] * S4, EARN[2] * S4
ex, ey = 960 - ew / 2, 430 - eh / 2
pops = ""
for cid, (x, y, w, h) in CARDS.items():
    pops += (f'<div class="pop" id="{cid}" style="left:{ex + x * S4:.0f}px;top:{ey + y * S4:.0f}px">'
             f'{crop_div(EARN, x, y, w, h, S4)}</div>')
clip("b4", 6.2, 2.45,
     f'<div class="stage3d"><div class="shot" id="earnBase" style="left:{ex:.0f}px;top:{ey:.0f}px;width:{ew:.0f}px;height:{eh:.0f}px">'
     f'<img src="{EARN[0]}" alt="What you earn"><div class="dim" id="dim4"></div></div>{pops}</div>'
     f'<div class="cap" id="cap4">{words("When they form a company,")} <br>{words("*you *earn.")}</div>')
T('tl.fromTo("#earnBase", {scale: 2.3, filter: "blur(24px)", opacity: 0}, {scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.55, ease: "expo.out"}, 6.2);')
T('tl.to("#dim4", {opacity: 1, duration: 0.3}, 6.85);')
T('tl.fromTo("#cD", {opacity: 0}, {opacity: 1, rotationY: 14, x: -30, z: 60, duration: 0.6, ease: "back.out(1.4)", transformOrigin: "100% 50%"}, 6.85);')
T('tl.fromTo("#cU", {opacity: 0}, {opacity: 1, rotationY: -14, x: 30, z: 60, duration: 0.6, ease: "back.out(1.4)", transformOrigin: "0% 50%"}, 6.95);')
T('tl.fromTo("#cap4 .w", {y: 50, opacity: 0, filter: "blur(10px)"}, {y: 0, opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out", stagger: 0.07}, 6.45);')

# ---------------------------------------------------------------- 5a. $500 punch (8.6 - 10.1)
clip("b5a", 8.6, 1.5,
     '<div class="flash" id="flash5"></div><div class="money">'
     '<div class="upto" id="upto">Up to</div><div class="big gold" id="big500">$500</div>'
     '<div class="per" id="per">per company</div></div>')
T('tl.fromTo("#flash5", {opacity: 0.35}, {opacity: 0, duration: 0.18}, 8.6);')
T('tl.fromTo("#big500", {scale: 2.6, filter: "blur(30px)", opacity: 0}, {scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.42, ease: "expo.out"}, 8.6);')
T('tl.to("#b5a .money", {scale: 1.06, duration: 1.5, ease: "none"}, 8.6);')
T('tl.fromTo("#upto", {y: 30, opacity: 0}, {y: 0, opacity: 1, duration: 0.3, ease: "power3.out"}, 8.8);')
T('tl.fromTo("#per", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0)", duration: 0.4, ease: "power3.inOut"}, 8.95);')

# ---------------------------------------------------------------- 5b. the real $500 row (10.1 - 11.45)
S5 = 2.75
rx, ry, rw, rh = GOLD_ROW
pad = 10
row = crop_div(EARN, rx - pad, ry - pad, rw + 2 * pad, rh + 2 * pad, S5)
bw_, bh_ = (rw + 2 * pad) * S5, (rh + 2 * pad) * S5
clip("b5b", 10.1, 1.35,
     f'<div class="rowshot" id="row5" style="left:{960 - bw_ / 2:.0f}px;top:{470 - bh_ / 2:.0f}px">{row}'
     f'<svg class="trace" width="{bw_:.0f}" height="{bh_:.0f}"><rect x="6" y="6" width="{bw_ - 12:.0f}" height="{bh_ - 12:.0f}" rx="18" '
     f'pathLength="1" id="tr5"/></svg></div>')
T('tl.fromTo("#row5", {scale: 0.45, filter: "blur(20px)", opacity: 0}, {scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.4, ease: "expo.out"}, 10.1);')
T('tl.fromTo("#tr5", {strokeDashoffset: 1}, {strokeDashoffset: 0, duration: 0.55, ease: "power2.inOut"}, 10.35);')
T('tl.to("#row5", {scale: 1.06, duration: 0.9, ease: "none"}, 10.5);')

# ---------------------------------------------------------------- 6. rate rack (11.4 - 14.25)
S6 = 2.45
rows = [("Dubai company", r) for r in DUBAI_ROWS] + [("US LLC", r) for r in US_ROWS]
rack = ""
for i, (lab, (x, y, w, h)) in enumerate(rows):
    rack += (f'<div class="rack" id="rk{i}" style="left:{960 - (w + 16) * S6 / 2:.0f}px;top:{470 - (h + 12) * S6 / 2:.0f}px">'
             f'{crop_div(EARN, x - 8, y - 6, w + 16, h + 12, S6)}</div>')
clip("b6", 11.4, 2.85,
     '<div class="stage3d">' + rack + '</div>'
     '<div class="kicker" id="k6a">Dubai company</div><div class="kicker" id="k6b">US LLC</div>'
     '<div class="lower" id="low6">Dubai: paid when the licence is issued  ·  US LLC: paid when the client pays</div>')
for i in range(6):
    t0 = 11.45 + i * 0.45
    T(f'tl.fromTo("#rk{i}", {{rotationX: -95, y: -60, opacity: 0}}, {{rotationX: 0, y: 0, opacity: 1, duration: 0.28, ease: "power3.out"}}, {t0:.2f});')
    T(f'tl.fromTo("#rk{i} .crop", {{boxShadow: "0 0 0 0px rgba(245,196,81,0)"}}, {{boxShadow: "0 0 0 3px #F5C451, 0 0 34px rgba(245,196,81,0.55)", duration: 0.12, yoyo: true, repeat: 1}}, {t0 + 0.2:.2f});')
    if i < 5:
        T(f'tl.to("#rk{i}", {{rotationX: 95, y: 60, opacity: 0, duration: 0.2, ease: "power3.in"}}, {t0 + 0.42:.2f});')
T('tl.fromTo("#k6a", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: 0.25}, 11.45);')
T('tl.to("#k6a", {opacity: 0, y: -20, duration: 0.2}, 12.75);')
T('tl.fromTo("#k6b", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: 0.25}, 12.8);')
T('tl.fromTo("#low6", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: 0.35}, 11.7);')
T('tl.to("#b6 .stage3d, #k6b, #low6", {opacity: 0, filter: "blur(16px)", duration: 0.25}, 13.95);')

# ---------------------------------------------------------------- 7. join + wave-mark roll and wipe (14.2 - 17.0)
clip("b7", 14.2, 2.8, f'<div class="qwrap" id="q7"><div class="q small">{words("Join the *GenZone")}</div>'
     f'<div class="q small">{words("referral program.")}</div></div>'
     '')
clip("wipe", 15.3, 1.9, f'<img class="mark" id="mark" src="{MARK}" alt="GenZone wave mark">', track=8)
T('tl.fromTo("#q7 .w", {y: 80, opacity: 0, filter: "blur(16px)"}, {y: 0, opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out", stagger: 0.08}, 14.25);')
T('tl.to("#q7", {x: 260, opacity: 0.0, filter: "blur(12px)", duration: 0.3, ease: "power2.in"}, 15.45);')
T('tl.fromTo("#mark", {x: -1300, rotation: -540, scale: 0.55}, {x: 0, rotation: 0, scale: 0.55, duration: 0.6, ease: "power3.out"}, 15.3);')
T('tl.to("#mark", {scale: 9, transformOrigin: "44% 41%", duration: 0.6, ease: "power3.in"}, 15.95);')
T('tl.to("#mark", {opacity: 0, duration: 0.45, ease: "power1.out"}, 16.62);')

# ---------------------------------------------------------------- 8. end card (16.8 - 21.6)
clip("end", 16.5, 5.1,
     f'<div class="endin"><img class="wordmark" id="wm" src="{WORD}" alt="GenZone">'
     '<div class="url" id="url"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#3EC5FF" stroke-width="1.6">'
     '<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12h20M4 7h16M4 17h16"/></svg>'
     '<span>www.genzone.com</span></div><div class="cta" id="cta">Join the referral program</div></div>', track=7)
T('tl.fromTo("#wm", {scale: 1.25, filter: "blur(14px)", opacity: 0}, {scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.5, ease: "expo.out"}, 16.65);')
T('tl.fromTo("#url", {y: 24, opacity: 0}, {y: 0, opacity: 1, duration: 0.35, ease: "power3.out"}, 16.9);')
T('tl.fromTo("#cta", {scale: 0.7, opacity: 0}, {scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}, 17.1);')
T('tl.to("#cta", {boxShadow: "0 0 0 2px #3EC5FF, 0 0 60px rgba(62,197,255,0.75)", duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut"}, 18.0);')
T('tl.to("#end .endin", {opacity: 0, filter: "blur(10px)", duration: 0.3}, 21.3);')

# ---------------------------------------------------------------- 9. made by card (21.6 - 24)
clip("madeby", 21.6, 2.4, '<div class="mb"><div class="mb1" id="mb1">made by</div>'
     '<div class="mb2" id="mb2">Kacper Semik</div><div class="mbline" id="mbl"></div></div>', track=7)
T('tl.fromTo("#mb1", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: 0.35, ease: "power3.out"}, 21.65);')
T('tl.fromTo("#mb2", {clipPath: "inset(0 100% 0 0)", filter: "blur(8px)"}, {clipPath: "inset(0 0% 0 0)", filter: "blur(0px)", duration: 0.6, ease: "power3.inOut"}, 21.8);')
T('tl.fromTo("#mbl", {scaleX: 0}, {scaleX: 1, duration: 0.6, ease: "power3.inOut"}, 22.0);')
T('tl.to("#madeby .mb", {opacity: 0, duration: 0.5}, 23.45);')

# music
clips.append('<audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="24" data-track-index="10"></audio>')

css = open("style.css").read()
open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="24" data-width="{W}" data-height="{H}">
{chr(10).join("      " + c for c in clips)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join("      " + x for x in tw)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
""")
print(f"wrote index.html: {len(clips)} clips, {len(tw)} tweens")
