#!/usr/bin/env python3
"""Generates index.html: every page of the GenZone storyboard PDF, in order,
shown full-frame (uncropped), cut on a 0.5s beat grid. Run: python3 build.py"""

# Seconds per page (multiples of 0.5). Pages that carry a subtitle line get
# reading time; in-between animation frames stay short.
DUR = [1.5, 2, 3, 1.5, 3, 1.5, 3.5, 2.5, 1.5, 2.5, 2.5, 2, 2.5, 1.5,
       3, 2.5, 2.5, 1.5, 3, 2.5, 1.5, 3, 1.5, 8]
assert len(DUR) == 24 and sum(DUR) == 60

# Motion per page: (start scale, end scale). Opening frames punch in from slightly
# larger; everything settles at or near 1.0 so the whole page stays on screen.
PUNCH = {3, 7, 15, 16, 17, 24}   # section starts / payoff frames

clips, tweens, t = [], [], 0.0
for i, d in enumerate(DUR, start=1):
    cid = f"p{i:02d}"
    clips.append(f'<div id="{cid}" class="clip page" data-start="{t}" data-duration="{d}" data-track-index="1">'
                 f'<img id="{cid}-img" src="assets/pages/page{i:02d}.png" alt="GenZone storyboard page {i}"></div>')
    if i in PUNCH:
        tweens.append(f'tl.fromTo("#{cid}-img", {{scale: 1.08}}, {{scale: 1, duration: 0.45, ease: "expo.out"}}, {t});')
    else:
        tweens.append(f'tl.fromTo("#{cid}-img", {{scale: 1}}, {{scale: 1.025, duration: {d}, ease: "none"}}, {t});')
    t += d

html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
      .page {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}
      .page img {{ display: block; width: 1920px; height: 1080px; transform-origin: 50% 50%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{int(t)}" data-width="1920" data-height="1080">
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
print(f"wrote index.html: {len(clips)} pages, {t}s")
