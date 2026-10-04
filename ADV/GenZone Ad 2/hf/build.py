#!/usr/bin/env python3
"""GenZone Referral Program — spec ad #2, Idea 2 "The link is the product". PREVIEW v1, 16:9.

One continuous camera move through the real dashboard screenshot (dash_safe.png:
cropped above the pipeline, referral code + "Referred by" code blurred), rows lifting
off in gold, the frame closing into a circle where the wave mark draws itself, end card,
made-by card. Picture + original score; no VO, no SFX.
Run: python3 build.py -> index.html
"""
W, H = 1920, 1080
DASH = ("assets/img/dash_safe.png", 1487, 598)
MARK = "assets/img/wave-mark_from-pdf.png"
WORD = "assets/img/wordmark_from-pdf.png"
ROW_DUBAI = (304, 412, 552, 39)     # Business License + 1 Residency Visa — $500 per sale
ROW_US = (889, 452, 553, 39)        # Done-For-You — 20% · up to $400
FOOT = (1022, 538, 422, 18)         # "The terms are fixed at that moment, so a later change never moves what"
LINKFIELD = (291, 66, 555, 36)
CX, CY = 960, 470                   # camera origin on screen

clips, tw = [], []


def clip(cid, start, dur, html, track=2, cls="scene"):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{start}" data-duration="{dur}" '
                 f'data-track-index="{track}">{html}</div>')


def T(s):
    tw.append(s)


def cam(px, py, s):
    """World transform that puts dashboard point (px, py) on the camera origin at scale s."""
    return f"x: {-px * s:.1f}, y: {-py * s:.1f}, scale: {s}"


def crop(x, y, w, h, extra=""):
    return (f'<div class="crop {extra}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background-position:-{x}px -{y}px"></div>')


def caption(cid, start, dur, lines, top=None):
    inner = "".join(f'<div class="ln"><span>{l}</span></div>' for l in lines)
    style = f' style="top:{top}px"' if top else ""
    clip(cid, start, dur, f'<div class="capt"{style}>{inner}</div>', track=9, cls="capwrap")
    T(f'tl.fromTo("#{cid} .ln span", {{yPercent: 115, skewY: 7, filter: "blur(8px)"}}, '
      f'{{yPercent: 0, skewY: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out", stagger: 0.09}}, {start});')
    T(f'tl.to("#{cid} .ln span", {{yPercent: -115, filter: "blur(8px)", duration: 0.28, ease: "power3.in", stagger: 0.04}}, {start + dur - 0.3:.2f});')


# ------------------------------------------------------------------ stage
clip("bg", 0, 23, '<div class="glow" id="glow"></div><div class="leak tl"></div><div class="leak br"></div>', track=0, cls="bgl")
T('tl.fromTo("#glow", {x: 240, y: -60, scale: 1.1}, {x: -240, y: 50, scale: 0.95, duration: 23, ease: "sine.inOut"}, 0);')
clip("grid", 2.6, 13.6, '<div class="gridlines" id="gl"></div>', track=1, cls="bgl")
T('tl.fromTo("#gl", {opacity: 0}, {opacity: 1, duration: 0.6}, 2.8);')
T('tl.fromTo("#gl", {backgroundPosition: "0px 0px"}, {backgroundPosition: "-150px -300px", duration: 13.6, ease: "none"}, 2.6);')
T('tl.to("#gl", {opacity: 0, duration: 0.5}, 15.4);')

# ------------------------------------------------------------------ the oner (0 - 17.0)
lift = crop(*ROW_DUBAI, extra="lift") .replace('class="crop lift"', 'class="crop lift" id="liftD"') \
     + crop(*ROW_US, extra="lift").replace('class="crop lift"', 'class="crop lift" id="liftU"')
world = (f'<div class="world" id="world" style="width:{DASH[1]}px;height:{DASH[2]}px">'
         f'<img src="{DASH[0]}" alt="GenZone referral dashboard"><div class="edge" id="edge"></div>'
         f'<div class="sweep" id="sweep" style="left:{LINKFIELD[0]}px;top:{LINKFIELD[1]}px;width:{LINKFIELD[2]}px;height:{LINKFIELD[3]}px"></div>'
         f'<div class="dimw" id="dimw"></div>{lift}'
         f'<div class="uline" id="uline" style="left:{FOOT[0]}px;top:{FOOT[1] + FOOT[3] - 1}px;width:{FOOT[2]}px"></div></div>')
clip("oner", 0, 17.0, f'<div class="lens" id="lens"><div class="cam" id="cam" style="left:{CX}px;top:{CY}px">{world}</div></div>')

# 0-3  macro on the link, focus rack, slow drift along the URL
T(f'tl.fromTo("#world", {{{cam(330, 84, 3.6)}}}, {{{cam(470, 84, 3.9)}, duration: 3.0, ease: "none"}}, 0);')
T('tl.fromTo("#cam", {rotationY: -16, rotationX: 7}, {rotationY: -9, rotationX: 4, duration: 3.0, ease: "none"}, 0);')
T('tl.fromTo("#lens", {filter: "blur(16px)"}, {filter: "blur(0px)", duration: 0.9, ease: "power2.out"}, 0.05);')
T('tl.set("#lens", {filter: "none"}, 0.97);')
caption("c1", 0.7, 2.25, ["This is your link."])

# 3-7  fast pull-out to the whole screen with a 3D settle
T(f'tl.to("#world", {{{cam(743, 299, 1.12)}, duration: 1.25, ease: "expo.inOut"}}, 3.0);')
T('tl.to("#cam", {rotationY: 7, rotationX: 10, duration: 0.7, ease: "power2.in"}, 3.0);')
T('tl.to("#cam", {rotationY: 0, rotationX: 0, duration: 0.9, ease: "back.out(1.6)"}, 3.7);')
T(f'tl.to("#world", {{{cam(743, 299, 1.06)}, duration: 2.6, ease: "none"}}, 4.25);')
T('tl.fromTo("#edge", {backgroundPosition: "0% 0%"}, {backgroundPosition: "300% 0%", duration: 2.4, ease: "none"}, 4.2);')
caption("c2", 4.35, 2.65, ["Share it with anyone who needs", "a company in Dubai or the US."], top=850)

# 7-12  glide down to the earnings table; rows lift off in gold
T(f'tl.to("#world", {{{cam(872, 432, 1.85)}, duration: 1.3, ease: "power3.inOut"}}, 7.0);')
T('tl.to("#cam", {rotationX: 12, duration: 0.65, ease: "power2.in"}, 7.0);')
T('tl.to("#cam", {rotationX: 3, duration: 0.65, ease: "power2.out"}, 7.65);')
T('tl.to("#dimw", {opacity: 1, duration: 0.35}, 8.35);')
T('tl.fromTo("#liftD", {z: 0, opacity: 0}, {z: 230, opacity: 1, duration: 0.55, ease: "back.out(1.7)"}, 8.4);')
T(f'tl.to("#world", {{{cam(600, 432, 1.85)}, duration: 1.7, ease: "power1.inOut"}}, 8.4);')
caption("c3", 8.6, 1.7, ['Up to <b class="gold">$500</b>', "per Dubai company."], top=780)
T('tl.to("#liftD", {z: 0, opacity: 0, duration: 0.3, ease: "power2.in"}, 10.2);')
T(f'tl.to("#world", {{{cam(1160, 470, 1.85)}, duration: 0.6, ease: "power3.inOut"}}, 10.2);')
T('tl.fromTo("#liftU", {z: 0, opacity: 0}, {z: 230, opacity: 1, duration: 0.55, ease: "back.out(1.7)"}, 10.45);')
caption("c4", 10.55, 1.55, ['Up to <b class="gold">$400</b>', "per US LLC."], top=780)
T('tl.to("#liftU", {z: 0, opacity: 0, duration: 0.3, ease: "power2.in"}, 12.0);')
T('tl.to("#dimw", {opacity: 0, duration: 0.3}, 12.0);')

# 12-15  back up to the link (stays attached), then the terms line (fixed when earned)
T(f'tl.to("#world", {{{cam(568, 96, 2.1)}, duration: 0.8, ease: "expo.inOut"}}, 12.0);')
T('tl.to("#cam", {rotationX: -6, rotationY: 5, duration: 0.8, ease: "power2.inOut"}, 12.0);')
T('tl.fromTo("#sweep", {backgroundPosition: "-120% 0"}, {backgroundPosition: "220% 0", duration: 0.8, ease: "power2.inOut"}, 12.6);')
caption("c5", 12.35, 1.35, ["It stays attached to your link."], top=880)
T(f'tl.to("#world", {{{cam(1233, 548, 2.6)}, duration: 0.75, ease: "expo.inOut"}}, 13.6);')
T('tl.to("#cam", {rotationX: 4, rotationY: -6, duration: 0.75, ease: "power2.inOut"}, 13.6);')
T('tl.fromTo("#uline", {scaleX: 0}, {scaleX: 1, duration: 0.5, ease: "power3.inOut"}, 14.2);')
caption("c6", 13.8, 1.35, ["Your rate is fixed", "the moment you earn."], top=780)

# 15-17  the frame closes into a circle; the wave mark draws inside it
T(f'tl.to("#world", {{{cam(743, 299, 0.62)}, duration: 1.0, ease: "expo.inOut"}}, 15.1);')
T('tl.to("#cam", {rotationX: 0, rotationY: 0, duration: 0.8}, 15.1);')
T(f'tl.fromTo("#lens", {{clipPath: "circle(1200px at {CX}px {CY}px)"}}, {{clipPath: "circle(230px at {CX}px {CY}px)", duration: 0.9, ease: "power3.inOut"}}, 15.3);')
T('tl.to("#world", {opacity: 0, duration: 0.45}, 16.25);')

clip("logo", 16.0, 2.5, f'<div class="ring" id="ring"></div><img class="mark" id="mark" src="{MARK}" alt="GenZone wave mark">', track=5)
T('tl.fromTo("#ring", {opacity: 0, scale: 1}, {opacity: 1, scale: 1, duration: 0.3}, 16.0);')
T('tl.fromTo("#mark", {"--a": "0deg", rotation: -90}, {"--a": "360deg", rotation: 0, duration: 0.95, ease: "power2.inOut"}, 16.2);')
T('tl.to("#ring", {opacity: 0, scale: 1.25, duration: 0.4}, 17.0);')
# mark shrinks into the "o" of the wordmark
T('tl.to("#mark", {scale: 0.215, x: 120, y: -14, duration: 0.6, ease: "power3.inOut"}, 17.25);')
T('tl.to("#mark", {opacity: 0, duration: 0.1}, 17.9);')

# ------------------------------------------------------------------ end card (17.6 - 20.8)
clip("end", 17.6, 3.2,
     f'<div class="endin"><img class="wordmark" id="wm" src="{WORD}" alt="GenZone">'
     '<div class="url" id="url"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#3EC5FF" stroke-width="1.6">'
     '<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12h20M4 7h16M4 17h16"/></svg>'
     '<span>www.genzone.com</span></div><div class="cta" id="cta"><span class="shine"></span>Join the referral program</div></div>', track=7)
T('tl.fromTo("#wm", {opacity: 0, filter: "blur(10px)"}, {opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power2.out"}, 17.6);')
T('tl.fromTo("#url", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: 0.35, ease: "power3.out"}, 18.0);')
T('tl.fromTo("#cta", {opacity: 0, y: 26, scale: 0.92}, {opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2)"}, 18.15);')
T('tl.fromTo("#cta .shine", {xPercent: -120}, {xPercent: 220, duration: 0.8, ease: "power2.inOut"}, 18.9);')
T('tl.to("#end .endin", {opacity: 0, duration: 0.3}, 20.5);')

# ------------------------------------------------------------------ made by (20.8 - 23.0)
name = "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in "Kacper Semik")
clip("madeby", 20.8, 2.2, f'<div class="mb"><div class="mb1" id="mb1">made by</div><div class="mb2" id="mb2">{name}</div></div>', track=7)
T('tl.fromTo("#mb1", {opacity: 0, scaleX: 1.6, filter: "blur(6px)"}, {opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out"}, 20.85);')
T('tl.fromTo("#mb2 .ch", {opacity: 0, y: 40, rotationX: -80, filter: "blur(10px)"}, {opacity: 1, y: 0, rotationX: 0, filter: "blur(0px)", duration: 0.55, ease: "expo.out", stagger: 0.035}, 20.95);')
T('tl.to("#madeby .mb", {opacity: 0, duration: 0.5}, 22.45);')

clips.append('<audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="23" data-track-index="10"></audio>')

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
    <div id="root" data-composition-id="main" data-start="0" data-duration="23" data-width="{W}" data-height="{H}">
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
