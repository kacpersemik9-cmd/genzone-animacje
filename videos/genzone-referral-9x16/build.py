#!/usr/bin/env python3
"""GenZone Referral Dashboard — 30s launch video, vertical 9:16 (1080x1920).

Same story as genzone-referral-v2, re-framed for vertical: the camera follows
the action across the wide screenshots, and the commission cards stack.
Screenshots in screenshots/ are used unchanged (only cropped/framed).
Run: python3 build.py
"""
W, H = 1080, 1920
DASH = ("screenshots/dashboard-earn-pipeline.jpg", 1487, 908)
EARN = ("screenshots/what-you-earn.jpg", 1229, 389)
FCY = 820          # frame centre y
TY = 760           # where the camera puts its focus point


def origin(img):
    return W / 2 - img[1] / 2, FCY - img[2] / 2


def cam_xy(img, px, py, s, tx=W / 2, ty=TY):
    fx, fy = origin(img)
    return tx - (fx + px) * s, ty - (fy + py) * s


def cam(img, px, py, s, tx=W / 2, ty=TY):
    x, y = cam_xy(img, px, py, s, tx, ty)
    return f"{{x: {x:.1f}, y: {y:.1f}, scale: {s}}}"


def shot(sid, img, overlays=""):
    fx, fy = origin(img)
    return (f'<div class="stage3d"><div class="cam" id="{sid}c"><div class="frame" id="{sid}f" '
            f'style="left:{fx:.1f}px;top:{fy:.1f}px;width:{img[1]}px;height:{img[2]}px">'
            f'<img src="{img[0]}" alt="GenZone dashboard screenshot">{overlays}</div></div></div>')


def box(bid, x, y, w, h, cls="hl"):
    return f'<div class="{cls}" id="{bid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'


def crop_style(img, x, y, w, h):
    return (f'width:{w}px;height:{h}px;background-image:url({img[0]});background-repeat:no-repeat;'
            f'background-position:-{x}px -{y}px;background-size:{img[1]}px {img[2]}px')


clips, tw = [], []


def clip(cid, start, dur, html, track=2, cls="scene"):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{start}" data-duration="{dur}" '
                 f'data-track-index="{track}">{html}</div>')


def line(cid, start, dur, text):
    clip(cid, start, dur, f'<div class="line">{text}</div>', track=9, cls="linewrap")
    tw.append(f'tl.fromTo("#{cid} .line", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.35, ease: "power3.out"}}, {start + 0.05});')


clip("bg", 0, 30, '<div class="glow"></div><div class="leak tl"></div><div class="leak br"></div>', track=0, cls="bgl")
clip("grid", 3, 22, '<div class="gridlines"></div>', track=1, cls="bgl")
tw.append('tl.fromTo("#grid .gridlines", {opacity: 0}, {opacity: 1, duration: 0.5}, 3);')

# 1. Logo reveal 0-3
WAVE = ("M-200,1150 C120,980 300,820 560,980 C800,1130 920,640 1300,500 L1400,300 L1400,900 "
        "C1150,1000 980,1450 700,1500 C420,1550 200,1300 -200,1560 Z")
clip("s1", 0, 3, f'<svg class="wave" viewBox="0 0 {W} {H}" preserveAspectRatio="none"><defs>'
     '<radialGradient id="wg" cx="55%" cy="60%" r="60%"><stop offset="0" stop-color="#2B63F0"/>'
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

# 2+3. Dashboard 3-11
STAGES_X = [291, 458, 624, 791, 958, 1125, 1292]
STAGE_W = [146, 145, 146, 146, 146, 145, 162]
ov = (box("shareHl", 398, 111, 82, 39) + box("copyHl", 289, 111, 104, 39)
      + box("stageHl", STAGES_X[0] - 3, 647, STAGE_W[0] + 6, 53, "hl cyan"))
clip("s2", 3, 8, shot("d", DASH, ov))
tw += [f'tl.set("#dc", {cam(DASH, 743.5, 454, 0.7)}, 3);',
       'tl.fromTo("#df", {rotationX: 60, y: 900, opacity: 0}, {rotationX: 0, y: 0, opacity: 1, duration: 1.0, ease: "power3.out"}, 3);',
       f'tl.to("#dc", {{...{cam(DASH, 572, 107, 1.75)}, duration: 0.55, ease: "expo.inOut"}}, 4.2);',
       'tl.fromTo("#copyHl", {opacity: 0}, {opacity: 1, duration: 0.2}, 4.9);',
       'tl.to("#copyHl", {opacity: 0, duration: 0.2}, 5.6);',
       'tl.fromTo("#shareHl", {opacity: 0, scale: 1}, {opacity: 1, scale: 1.12, duration: 0.18, yoyo: true, repeat: 3, ease: "sine.inOut"}, 5.75);']
line("l2", 3.6, 3.4, "Your personal referral link.")
cx0 = STAGES_X[0] + STAGE_W[0] / 2
tw.append(f'tl.to("#dc", {{...{cam(DASH, cx0 + 160, 673, 2.0)}, duration: 0.7, ease: "power3.inOut"}}, 7.0);')
tw.append('tl.fromTo("#stageHl", {opacity: 0}, {opacity: 1, duration: 0.2}, 7.75);')
for i in range(1, 7):
    t = 7.95 + i * 0.45
    cx = STAGES_X[i] + STAGE_W[i] / 2
    tw.append(f'tl.to("#stageHl", {{x: {STAGES_X[i] - STAGES_X[0]}, scaleX: {(STAGE_W[i] + 6) / (STAGE_W[0] + 6):.3f}, '
              f'transformOrigin: "0% 50%", duration: 0.22, ease: "power2.inOut"}}, {t:.2f});')
    tw.append(f'tl.to("#dc", {{...{cam(DASH, min(max(cx, cx0 + 160), 1454 - 160), 673, 2.0)}, duration: 0.3, ease: "power2.inOut"}}, {t:.2f});')
line("l3", 7.3, 3.7, "Track every referral, from lead to paid.")


def headline(cid, start, dur, parts):
    words = " ".join(f'<span class="w {c}">{t}</span>' for c, t in parts)
    clip(cid, start, dur, f'<div class="headline">{words}</div>')
    tw.append(f'tl.fromTo("#{cid} .w", {{yPercent: 60, opacity: 0, scale: 1.3}}, {{yPercent: 0, opacity: 1, scale: 1, '
              f'duration: 0.32, ease: "expo.out", stagger: 0.14}}, {start});')
    tw.append(f'tl.fromTo("#{cid} .headline", {{scale: 1}}, {{scale: 1.05, duration: {dur}, ease: "none"}}, {start});')


def earn_zoom(cid, start, dur, card_c, row, row_c):
    rx, ry, rw, rh = row
    clip(cid, start, dur, shot(cid, EARN, box(cid + "hl", rx, ry, rw, rh, "hl hlgold")))
    tw.append(f'tl.fromTo("#{cid}c", {cam(EARN, card_c[0], card_c[1], 1.55)}, {{...{cam(EARN, card_c[0], card_c[1], 1.65)}, duration: 0.6, ease: "power2.out"}}, {start});')
    tw.append(f'tl.to("#{cid}c", {{...{cam(EARN, row_c[0], row_c[1], 1.85)}, duration: 0.6, ease: "expo.inOut"}}, {start + 0.75});')
    tw.append(f'tl.fromTo("#{cid}hl", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {start + 1.3});')


headline("s4a", 11, 1.6, [("gold", "$500"), ("silver", "Per"), ("blue", "Dubai Company")])
earn_zoom("s4b", 12.6, 2.4, (325, 175), (48, 191, 553, 39), (325, 210))
headline("s5a", 15, 1.6, [("silver", "Up to"), ("gold", "$400"), ("silver", "Per"), ("blue", "US LLC")])
earn_zoom("s5b", 16.6, 2.4, (910, 175), (634, 230, 552, 39), (910, 249))

# 6. Cards stack and pop 19-25. Base screenshot dims; crops of each card lift into a vertical stack.
BASE_S = 0.82
bx, by = cam_xy(EARN, 614.5, 194.5, BASE_S, ty=FCY)
fx, fy = origin(EARN)


def screen_pos(x, y, w, h):
    return bx + (fx + x) * BASE_S, by + (fy + y) * BASE_S, w * BASE_S, h * BASE_S


POPS = [("popD", 40, 67, 570, 216, 520), ("popU", 626, 67, 569, 216, 940)]
html6 = shot("e", EARN, '<div class="dimmer" id="dim6"></div>')
for pid, x, y, w, h, ty in POPS:
    sx, sy, _, _ = screen_pos(x, y, w, h)
    html6 += f'<div class="popcard v" id="{pid}" style="left:{sx:.1f}px;top:{sy:.1f}px;{crop_style(EARN, x, y, w, h)}"></div>'
    s = 1.72
    tx, tyy = W / 2 - w * s / 2, ty - h * s / 2
    POPS[POPS.index((pid, x, y, w, h, ty))] = (pid, sx, sy, tx, tyy, s)
# footnote: the two lines of the real terms text that say rates are locked in, stacked in one card
FA, FB = (767, 316, 423, 20), (34, 336, 160, 20)
html6 += (f'<div class="popcard v foot" id="popF"><div style="{crop_style(EARN, *FA)}"></div>'
          f'<div style="{crop_style(EARN, *FB)}"></div></div>')
clip("s6", 19, 6, html6)
tw += [f'tl.fromTo("#ec", {cam(EARN, 614.5, 194.5, 1.6, ty=FCY)}, {{...{cam(EARN, 614.5, 194.5, BASE_S, ty=FCY)}, duration: 0.6, ease: "power3.out"}}, 19);',
       'tl.to("#dim6", {opacity: 1, duration: 0.35}, 19.5);', 'tl.to("#ef", {opacity: 0.18, duration: 0.4}, 19.6);']
for (pid, sx, sy, tx, tyy, s), t in zip(POPS, (19.6, 19.8)):
    tw.append(f'tl.fromTo("#{pid}", {{opacity: 0, x: 0, y: 0, scale: {BASE_S}}}, {{opacity: 1, x: {tx - sx:.1f}, y: {tyy - sy:.1f}, '
              f'scale: {s}, duration: 0.5, ease: "back.out(1.5)"}}, {t});')
tw += ['tl.to("#popU", {opacity: 0.45, duration: 0.2}, 19.9);',
       'tl.to("#popU", {opacity: 1, duration: 0.25}, 21.0);',
       'tl.to("#popD", {opacity: 0.45, duration: 0.25}, 21.0);',
       'tl.to("#popU", {opacity: 0.45, duration: 0.25}, 23.0);',
       'tl.fromTo("#popF", {opacity: 0, y: 60, scale: 0.9}, {opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.7)"}, 23.0);']
line("l6a", 19.35, 1.65, "Fixed fee per Dubai company.")
line("l6b", 21.0, 2.0, "Percentage on every US LLC.")
line("l6c", 23.0, 2.0, "Your rate is locked in when you earn it.")

# 7. Wipe + end card
clip("wipe", 24.95, 1.0, '<img class="mark" id="mark2" src="assets/img/mark.png" alt="">', track=8)
tw += ['tl.fromTo("#mark2", {scale: 0.15, rotation: -40, opacity: 0.95}, {scale: 9, rotation: 0, duration: 0.6, ease: "power3.in"}, 24.95);',
       'tl.to("#mark2", {opacity: 0, duration: 0.3}, 25.6);']
clip("end", 25.55, 4.45,
     '<img class="wordmark" id="wm2" src="assets/img/wordmark.png" alt="GenZone">'
     '<div class="url" id="url"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2B63F0" stroke-width="1.6">'
     '<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12h20M4 7h16M4 17h16"/></svg>'
     '<span>www.genzone.com</span></div>'
     '<div class="endline" id="endline">Share your link.<br>Refer your network.<br>Start earning.</div>'
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
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="{W}" data-height="{H}">
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
