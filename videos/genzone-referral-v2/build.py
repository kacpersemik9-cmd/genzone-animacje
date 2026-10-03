#!/usr/bin/env python3
"""GenZone Referral Dashboard — 30s launch video (v2). Generates index.html.

Uses the two real dashboard screenshots in screenshots/ unchanged:
  dashboard-earn-pipeline.jpg (1487x908) and what-you-earn.jpg (1229x389).
Logo mark + wordmark are crops from the GenZone storyboard PDF (no logo.png given).
Run: python3 build.py
"""

DASH = ("screenshots/dashboard-earn-pipeline.jpg", 1487, 908)
EARN = ("screenshots/what-you-earn.jpg", 1229, 389)


def frame_origin(w, h, cy=470):
    return 960 - w / 2, cy - h / 2


def cam(img, px, py, s, tx=960, ty=440):
    """Camera (origin 0 0) putting image point (px,py) at screen (tx,ty) at scale s."""
    fx, fy = frame_origin(img[1], img[2])
    return f"{{x: {tx - (fx + px) * s:.1f}, y: {ty - (fy + py) * s:.1f}, scale: {s}}}"


def shot(sid, img, overlays=""):
    fx, fy = frame_origin(img[1], img[2])
    return (f'<div class="stage3d"><div class="cam" id="{sid}c"><div class="frame" id="{sid}f" '
            f'style="left:{fx:.1f}px;top:{fy:.1f}px;width:{img[1]}px;height:{img[2]}px">'
            f'<img src="{img[0]}" alt="GenZone dashboard screenshot">{overlays}</div></div></div>')


def box(bid, x, y, w, h, cls="hl"):
    return f'<div class="{cls}" id="{bid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'


def crop(cid, img, x, y, w, h):
    """A pop-out card: the same screenshot, cropped to one card (not redrawn)."""
    return (f'<div class="popcard" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background-image:url({img[0]});background-position:-{x}px -{y}px;background-size:{img[1]}px {img[2]}px"></div>')


clips, tw = [], []


def clip(cid, start, dur, html, track=2, cls="scene"):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{start}" data-duration="{dur}" '
                 f'data-track-index="{track}">{html}</div>')


def line(cid, start, dur, text):
    clip(cid, start, dur, f'<div class="line">{text}</div>', track=9, cls="linewrap")
    tw.append(f'tl.fromTo("#{cid} .line", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.35, ease: "power3.out"}}, {start + 0.05});')


# background + grid
clip("bg", 0, 30, '<div class="glow"></div><div class="leak tl"></div><div class="leak br"></div>', track=0, cls="bgl")
clip("grid", 3, 22, '<div class="gridlines"></div>', track=1, cls="bgl")
tw.append('tl.fromTo("#grid .gridlines", {opacity: 0}, {opacity: 1, duration: 0.5}, 3);')

# 1. Logo reveal 0-3
WAVE = ("M-200,700 C200,520 420,380 760,560 C1080,740 1300,260 1560,120 L2200,-200 L2200,300 "
        "C1700,420 1500,900 1080,980 C700,1060 420,820 -200,1060 Z")
clip("s1", 0, 3, '<svg class="wave" viewBox="0 0 1920 1080" preserveAspectRatio="none"><defs>'
     '<radialGradient id="wg" cx="55%" cy="65%" r="60%"><stop offset="0" stop-color="#2B63F0"/>'
     f'<stop offset="1" stop-color="#14306f"/></radialGradient></defs><path d="{WAVE}" fill="url(#wg)"/></svg>'
     '<img class="mark" id="mark1" src="assets/img/mark.png" alt="">'
     '<img class="wordmark" id="wm1" src="assets/img/wordmark.png" alt="GenZone">')
tw += ['tl.fromTo("#s1 .wave", {clipPath: "inset(0% 100% 0% 0%)", opacity: 1}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.8, ease: "power3.inOut"}, 0);',
       'tl.to("#s1 .wave", {opacity: 0, duration: 0.5, ease: "power1.out"}, 1.2);',
       'tl.fromTo("#mark1", {scale: 0.2, rotation: -120, opacity: 0}, {scale: 1, rotation: 0, opacity: 1, duration: 0.8, ease: "back.out(1.4)"}, 0.45);',
       'tl.to("#mark1", {scale: 0.215, x: 109, y: 5, duration: 0.55, ease: "power3.inOut"}, 1.35);',
       'tl.fromTo("#wm1", {opacity: 0, scale: 1.08}, {opacity: 1, scale: 1, duration: 0.45, ease: "power2.out"}, 1.6);',
       'tl.to("#mark1", {opacity: 0, duration: 0.15}, 1.9);']
line("l1", 1.9, 1.1, "Your partner in business formation and growth.")

# 2+3. Dashboard 3-11 (one continuous shot: rise, link push-in, Share pulse, pan to pipeline)
STAGES_X = [291, 458, 624, 791, 958, 1125, 1292]
STAGE_W = [146, 145, 146, 146, 146, 145, 162]
ov = (box("shareHl", 398, 111, 82, 39) + box("copyHl", 289, 111, 104, 39)
      + box("stageHl", STAGES_X[0] - 3, 647, STAGE_W[0] + 6, 53, "hl cyan"))
clip("s2", 3, 8, shot("d", DASH, ov))
tw += [f'tl.fromTo("#dc", {cam(DASH, 743.5, 454, 0.92)}, {{...{cam(DASH, 743.5, 454, 0.92)}, duration: 0.01}}, 3);',
       'tl.fromTo("#df", {rotationX: 60, y: 560, opacity: 0}, {rotationX: 0, y: 0, opacity: 1, duration: 1.0, ease: "power3.out"}, 3);',
       f'tl.to("#dc", {{...{cam(DASH, 572, 107, 2.45)}, duration: 0.55, ease: "expo.inOut"}}, 4.2);',
       'tl.fromTo("#copyHl", {opacity: 0}, {opacity: 1, duration: 0.2}, 4.9);',
       'tl.to("#copyHl", {opacity: 0, duration: 0.2}, 5.6);',
       'tl.fromTo("#shareHl", {opacity: 0, scale: 1}, {opacity: 1, scale: 1.12, duration: 0.18, yoyo: true, repeat: 3, ease: "sine.inOut"}, 5.75);',
       f'tl.to("#dc", {{...{cam(DASH, 872, 672, 1.5)}, duration: 0.7, ease: "power3.inOut"}}, 7.0);']
line("l2", 3.6, 3.4, "Your personal referral link.")
# glowing highlight steps across the 7 stages on a 0.45s beat
tw.append('tl.fromTo("#stageHl", {opacity: 0}, {opacity: 1, duration: 0.2}, 7.75);')
for i in range(1, 7):
    tw.append(f'tl.to("#stageHl", {{x: {STAGES_X[i] - STAGES_X[0]}, scaleX: {(STAGE_W[i] + 6) / (STAGE_W[0] + 6):.3f}, transformOrigin: "0% 50%", duration: 0.22, ease: "power2.inOut"}}, {7.95 + i * 0.45:.2f});')
tw.append(f'tl.to("#dc", {{...{cam(DASH, 1000, 672, 1.5)}, duration: 2.6, ease: "none"}}, 8.0);')
line("l3", 7.3, 3.7, "Track every referral, from lead to paid.")


# 4+5. Kinetic money + table zoom
def headline(cid, start, dur, parts):
    words = " ".join(f'<span class="w {c}">{t}</span>' for c, t in parts)
    clip(cid, start, dur, f'<div class="headline">{words}</div>')
    tw.append(f'tl.fromTo("#{cid} .w", {{yPercent: 60, opacity: 0, scale: 1.3}}, {{yPercent: 0, opacity: 1, scale: 1, '
              f'duration: 0.32, ease: "expo.out", stagger: 0.14}}, {start});')
    tw.append(f'tl.fromTo("#{cid} .headline", {{scale: 1}}, {{scale: 1.06, duration: {dur}, ease: "none"}}, {start});')


def earn_zoom(cid, start, dur, card_c, row, row_c):
    rx, ry, rw, rh = row
    clip(cid, start, dur, shot(cid, EARN, box(cid + "hl", rx, ry, rw, rh, "hl hlgold")))
    tw.append(f'tl.fromTo("#{cid}c", {cam(EARN, card_c[0], card_c[1], 1.45)}, {{...{cam(EARN, card_c[0], card_c[1], 1.6)}, duration: 0.6, ease: "power2.out"}}, {start});')
    tw.append(f'tl.to("#{cid}c", {{...{cam(EARN, row_c[0], row_c[1], 2.75)}, duration: 0.6, ease: "expo.inOut"}}, {start + 0.75});')
    tw.append(f'tl.fromTo("#{cid}hl", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {start + 1.3});')


headline("s4a", 11, 1.6, [("gold", "$500"), ("silver", "Per"), ("blue", "Dubai Company")])
earn_zoom("s4b", 12.6, 2.4, (325, 210), (48, 191, 553, 39), (325, 210))
headline("s5a", 15, 1.6, [("silver", "Up to"), ("gold", "$400"), ("silver", "Per"), ("blue", "US LLC")])
earn_zoom("s5b", 16.6, 2.4, (910, 210), (634, 230, 552, 39), (910, 249))

# 6. Both cards pop 19-25
pops = (crop("popD", EARN, 40, 67, 570, 216) + crop("popU", EARN, 626, 67, 569, 216)
        + crop("popF", EARN, 24, 290, 1190, 70) + '<div class="dimmer" id="dim6"></div>')
clip("s6", 19, 6, shot("e", EARN, pops))
tw += [f'tl.fromTo("#ec", {cam(EARN, 614.5, 194.5, 2.0)}, {{...{cam(EARN, 614.5, 194.5, 1.42, ty=430)}, duration: 0.6, ease: "power3.out"}}, 19);',
       'tl.to("#dim6", {opacity: 1, duration: 0.35}, 19.5);',
       'tl.to("#popD", {opacity: 1, scale: 1.06, x: -30, y: -10, duration: 0.45, ease: "back.out(1.7)"}, 19.6);',
       'tl.to("#popU", {opacity: 1, scale: 1.06, x: 30, y: -10, duration: 0.45, ease: "back.out(1.7)"}, 19.8);',
              'tl.to("#popU", {scale: 1.1, duration: 0.3}, 21.0);',
       'tl.to("#popD", {opacity: 0, scale: 1.0, x: 0, y: 0, duration: 0.3}, 21.0);',
       'tl.to("#popU", {opacity: 0, scale: 1.0, x: 0, y: 0, duration: 0.3}, 23.0);',
       'tl.to("#popF", {opacity: 1, scale: 1.04, y: 14, duration: 0.4, ease: "back.out(1.7)"}, 23.0);']
line("l6a", 19.35, 1.65, "Fixed fee per Dubai company.")
line("l6b", 21.0, 2.0, "Percentage on every US LLC.")
line("l6c", 23.0, 2.0, "Your rate is locked in when you earn it.")

# 7. Wipe + end card 25-30
clip("wipe", 24.95, 1.0, '<img class="mark" id="mark2" src="assets/img/mark.png" alt="">', track=8)
tw += ['tl.fromTo("#mark2", {scale: 0.15, rotation: -40, opacity: 0.95}, {scale: 6.5, rotation: 0, duration: 0.6, ease: "power3.in"}, 24.95);',
       'tl.to("#mark2", {opacity: 0, duration: 0.3}, 25.6);']
clip("end", 25.55, 4.45,
     '<img class="wordmark" id="wm2" src="assets/img/wordmark.png" alt="GenZone">'
     '<div class="url" id="url"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#2B63F0" stroke-width="1.6">'
     '<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12h20M4 7h16M4 17h16"/></svg>'
     '<span>www.genzone.com</span></div>'
     '<div class="endline" id="endline">Share your link. Refer your network. Start earning.</div>'
     '<div class="cta" id="cta">Join the referral program</div>', track=7)
tw += ['tl.fromTo("#wm2", {scale: 1.2, opacity: 0}, {scale: 1, opacity: 1, duration: 0.45, ease: "expo.out"}, 25.55);',
       'tl.fromTo("#url", {y: 20, opacity: 0}, {y: 0, opacity: 1, duration: 0.3, ease: "power3.out"}, 25.7);',
       'tl.fromTo("#endline", {y: 20, opacity: 0}, {y: 0, opacity: 1, duration: 0.3, ease: "power3.out"}, 25.85);',
       'tl.fromTo("#cta", {scale: 0.7, opacity: 0}, {scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)"}, 26.0);',
       'tl.to("#cta", {boxShadow: "0 0 50px rgba(62,197,255,0.8)", duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut"}, 26.6);']

css = open("style.css").read()
open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1920" data-height="1080">
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
