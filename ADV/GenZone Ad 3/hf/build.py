#!/usr/bin/env python3
"""GenZone Referral Program — premium SaaS spot (#3), 24 s, 1920x1080 (rendered at 4K via 2x DPR).

The dashboard UI is rebuilt in HTML/CSS to match the supplied screenshots (layout, colours,
cards, typography), so every number can count up and every text stays vector-sharp.
Demo values only: code GENZ-DEMO42, "Demo client". Commission figures are the real rates.
Run: python3 build.py -> index.html
"""
W, H = 1920, 1080
CODE = "GENZ-DEMO42"
LOGO = "assets/img/wordmark_from-pdf.png"

DUBAI = [("Dubai Business License", 250, None), ("Business License + 1 Residency Visa", 500, None),
         ("Business License + 2 Residency Visas (or more)", 500, None)]
US = [("Basic", 15, 75), ("Advanced", 15, 150), ("Done-For-You", 20, 400)]
STAGES = ["Lead", "Call booked", "Signed up", "Applied", "In review", "Paid", "Completed"]

ICON = {
    "nav0": '<circle cx="12" cy="12" r="8"/><path d="M9 12l2 2 4-4"/>',
    "nav1": '<rect x="4" y="6" width="16" height="12" rx="2"/><path d="M16 12h2"/>',
    "nav2": '<path d="M4 10v4h3l6 4V6L7 10H4z"/><path d="M17 9a4 4 0 010 6"/>',
    "nav3": '<path d="M4 5h6a2 2 0 012 2v12a2 2 0 00-2-2H4zM20 5h-6a2 2 0 00-2 2v12a2 2 0 012-2h6z"/>',
    "copy": '<rect x="8" y="8" width="11" height="11" rx="2"/><path d="M5 15V6a1 1 0 011-1h9"/>',
    "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="17" cy="6" r="2.5"/><circle cx="17" cy="18" r="2.5"/><path d="M8.3 10.8l6.4-3.6M8.3 13.2l6.4 3.6"/>',
    "ext": '<path d="M14 5h5v5M19 5l-8 8"/><path d="M17 14v4a1 1 0 01-1 1H6a1 1 0 01-1-1V8a1 1 0 011-1h4"/>',
    "send": '<path d="M4 12l16-7-7 16-2-7z"/>',
    "earn": '<circle cx="12" cy="12" r="8.5"/><path d="M9 12.5l2 2 4-4.5"/>',
    "link": '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
    "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 19a7 7 0 0114 0"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "dollar": '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.2c-.6-.8-1.5-1.2-2.5-1.2-1.4 0-2.5.8-2.5 2s1.1 1.7 2.5 2 2.5.8 2.5 2-1.1 2-2.5 2c-1 0-2-.4-2.6-1.2M12 6.5v11"/>',
    "people": '<circle cx="9" cy="9" r="3"/><path d="M3.5 18a5.5 5.5 0 0111 0"/><circle cx="17" cy="9.5" r="2.5"/><path d="M15.5 14a4.5 4.5 0 016 4"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def ic(name, size=18, stroke="currentColor", sw=1.8):
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


# ---------------------------------------------------------------- dashboard (1500 x 860)
def dashboard(did):
    nav = ["Referral Dashboard", "Payouts", "Marketing Tools", "Resources"]
    navs = "".join(f'<div class="nav{" on" if i == 0 else ""}" id="{did}nav{i}" style="top:{96 + i * 46}px">'
                   f'<span class="ni">{ic("nav" + str(i), 15)}</span>{n}{"<span class=chev>›</span>" if i == 0 else ""}</div>'
                   for i, n in enumerate(nav))
    stages = "".join(f'<div class="pst" style="left:{18 + i * 168}px"><span>{s.upper()}</span><b>0</b></div>'
                     + (f'<div class="pch" style="left:{18 + i * 168 + 152}px">›</div>' if i < 6 else "")
                     for i, s in enumerate(STAGES))

    def rows(items, us):
        out = ""
        for i, (n, a, cap) in enumerate(items):
            v = f"{a}% · up to ${cap}" if us else f"${a} per sale"
            out += f'<div class="drow" style="top:{102 + i * 39}px"><span>{n}</span><b>{v}</b></div>'
        return out

    return f'''<div class="dash" id="{did}">
  <div class="side"><img class="slogo" src="{LOGO}" alt="GenZone">{navs}
    <div class="back">← Back to main dashboard</div>
    <div class="acct"><span class="av"></span><div><b>Account</b><small>Manage profile</small></div><span class="chev2">⌄</span></div></div>
  <div class="card" style="left:258px;top:0;width:590px;height:180px">
    <div class="field" id="{did}field" style="left:16px;top:26px;width:556px">https://portal.genzone.com/r/{CODE}</div>
    <div class="btns" style="left:16px;top:78px">
      <div class="btn b1" id="{did}copy">{ic("copy", 15)}Copy link</div>
      <div class="btn b2" id="{did}share">{ic("share", 15)}Share</div>
      <div class="btn b3">{ic("ext", 15)}Preview</div></div></div>
  <div class="card" style="left:868px;top:0;width:596px;height:180px">
    <div class="field ta" style="left:16px;top:22px;width:564px">What are they trying to do? Anything our team should know before reaching out.</div>
    <div class="small" style="left:16px;top:132px">Referred by <b>{CODE}</b> ({CODE})</div>
    <div class="btn b4" style="right:16px;top:122px">{ic("send", 14)}Submit referral</div></div>
  <div class="card" style="left:258px;top:200px;width:1206px;height:356px">
    <div class="h3" style="left:22px;top:20px">{ic("earn", 17)} What you earn</div>
    <div class="col" style="left:20px;top:56px;width:574px"><div class="ct">Dubai Company Referrals</div>
      <div class="cd">A UAE free-zone company: trade licence, plus residence visas for the owner and family if they want them.</div>{rows(DUBAI, False)}</div>
    <div class="col" style="left:612px;top:56px;width:574px"><div class="ct">US LLC Referrals</div>
      <div class="cd">A US limited liability company for founders anywhere: formation, EIN and registered agent, with tax filing on the higher tiers.</div>{rows(US, True)}</div>
    <div class="foot" style="left:20px;top:290px;width:1166px">A percentage is of what your referral actually pays, after any discount we give them; the "up to" figure is that percentage of the full package price. A fixed amount is paid per company formed, whatever the client paid. US LLC referrals earn when the client pays; Dubai referrals earn when the company licence is issued. The terms are fixed at that moment, so a later change never moves what you have already earned.</div></div>
  <div class="card" style="left:258px;top:576px;width:1206px;height:108px">
    <div class="lab" style="left:18px;top:16px">REFERRAL PIPELINE</div>{stages}</div>
  <div class="card" style="left:258px;top:704px;width:1206px;height:156px">
    <div class="h3" style="left:18px;top:22px">{ic("people", 17)} Referral tracking</div>
    <div class="small c" style="left:0;right:0;top:86px">No referrals yet. Share your link and they'll appear here.</div></div>
</div>'''


clips, tw = [], []


def clip(cid, start, dur, html, track=2, cls="scene"):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{start}" data-duration="{dur}" '
                 f'data-track-index="{track}">{html}</div>')


def T(s):
    tw.append(s)


def headline(cid, start, dur, text, top=120):
    words = " ".join(f'<span class="hw">{w}</span>' for w in text.split(" "))
    clip(cid, start, dur, f'<div class="head" style="top:{top}px">{words}</div>', track=8, cls="hwrap")
    T(f'tl.fromTo("#{cid} .hw", {{y: 46, opacity: 0, filter: "blur(10px)"}}, {{y: 0, opacity: 1, filter: "blur(0px)", '
      f'duration: 0.5, ease: "expo.out", stagger: 0.05}}, {start});')
    T(f'tl.to("#{cid} .hw", {{y: -30, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power2.in", stagger: 0.02}}, {start + dur - 0.35:.2f});')


# ---------------------------------------------------------------- background
clip("bg", 0, 24, '<div class="glow" id="glow"></div><div class="glow2" id="glow2"></div><div class="leak tl"></div><div class="leak br"></div><div class="grid" id="grid"></div>',
     track=0, cls="bgl")
T('tl.fromTo("#glow", {x: -220, y: -40}, {x: 260, y: 60, duration: 24, ease: "sine.inOut"}, 0);')
T('tl.fromTo("#glow2", {x: 200, y: 80, scale: 0.9}, {x: -260, y: -60, scale: 1.15, duration: 24, ease: "sine.inOut"}, 0);')
T('tl.fromTo("#grid", {backgroundPosition: "0px 0px"}, {backgroundPosition: "-120px -240px", duration: 24, ease: "none"}, 0);')

# ---------------------------------------------------------------- 1. dashboard push-in (0 - 4.4)
# camera: #cam1 origin at screen (960, 540); #w1 holds the 1500x860 dashboard; cam(px,py,s) puts dash point on origin
def cam(px, py, s):
    return f"x: {-px * s:.1f}, y: {-py * s:.1f}, scale: {s}"


clip("s1", 0, 4.45, f'<div class="lens"><div class="cam" id="cam1"><div class="world" id="w1">{dashboard("d1")}</div></div></div>')
T(f'tl.fromTo("#w1", {{{cam(750, 430, 0.62)}}}, {{{cam(750, 430, 0.86)}, duration: 1.5, ease: "expo.out"}}, 0);')
T('tl.fromTo("#cam1", {rotationX: 26, rotationY: -18, y: 140, opacity: 0}, {rotationX: 6, rotationY: -6, y: 0, opacity: 1, duration: 1.5, ease: "expo.out"}, 0);')
T('tl.fromTo("#d1 .card, #d1 .side", {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: 0.6, ease: "power3.out", stagger: 0.06}, 0.15);')
# highlight Referral Dashboard nav
T(f'tl.to("#w1", {{{cam(330, 220, 1.45)}, duration: 0.8, ease: "expo.inOut"}}, 1.35);')
T('tl.to("#cam1", {rotationX: 2, rotationY: 8, duration: 0.8, ease: "power2.inOut"}, 1.35);')
T('tl.fromTo("#d1nav0", {boxShadow: "0 0 0 0px rgba(62,197,255,0), 0 6px 18px rgba(43,99,240,0.5)"}, {boxShadow: "0 0 0 3px #3EC5FF, 0 0 40px rgba(62,197,255,0.85)", duration: 0.35, yoyo: true, repeat: 1, ease: "sine.inOut"}, 1.9);')
# push into the personal link
T(f'tl.to("#w1", {{{cam(552, 44, 1.85)}, duration: 0.85, ease: "expo.inOut"}}, 2.7);')
T('tl.to("#cam1", {rotationX: 0, rotationY: 0, duration: 0.85, ease: "power2.inOut"}, 2.7);')
T('tl.fromTo("#d1field", {boxShadow: "0 0 0 0px rgba(62,197,255,0)"}, {boxShadow: "0 0 0 2px #3EC5FF, 0 0 34px rgba(62,197,255,0.75)", duration: 0.35}, 3.35);')
T('tl.to("#s1 .lens", {opacity: 0, filter: "blur(14px)", duration: 0.5, ease: "power2.in"}, 3.95);')

# ---------------------------------------------------------------- 2. link -> flow (3.6 - 8.1)
FLOW = [("Share", "share"), ("Referral", "link"), ("Client", "user"), ("Sale", "receipt"), ("Commission", "dollar")]
nodes = ""
for i, (lab, icn) in enumerate(FLOW):
    cx = 270 + i * 345
    nodes += (f'<div class="node{" money" if i == 4 else ""}" id="n{i}" style="left:{cx - 120}px">'
              f'<span class="nic">{ic(icn, 30)}</span><span>{lab}</span></div>')
    if i < 4:
        nodes += f'<div class="conn" id="k{i}" style="left:{cx + 120}px;width:105px"></div>'
clip("s2", 3.6, 4.5,
     f'<div class="pill" id="pill"><span class="pic">{ic("link", 26)}</span><span>https://portal.genzone.com/r/{CODE}</span>'
     f'<span class="pcopy">{ic("copy", 18)}Copy link</span></div>'
     f'<div class="flow">{nodes}<div class="dot" id="dot"></div></div>', track=3)
T('tl.fromTo("#pill", {scale: 1.0, y: 0, opacity: 0}, {opacity: 1, duration: 0.25}, 3.6);')
T('tl.to("#pill", {scale: 1.12, z: 0, duration: 0.45, ease: "power2.out", boxShadow: "0 0 0 2px #3EC5FF, 0 0 80px rgba(62,197,255,0.7), 0 40px 80px rgba(0,0,0,0.5)"}, 3.85);')
T('tl.to("#pill", {scale: 0.72, y: -205, duration: 0.7, ease: "expo.inOut"}, 4.4);')
T('tl.fromTo("#pill .pcopy", {scale: 1}, {scale: 0.9, duration: 0.08, yoyo: true, repeat: 1}, 5.0);')
for i in range(5):
    t = 4.85 + i * 0.5
    T(f'tl.fromTo("#n{i}", {{y: 60, opacity: 0, rotationX: -50}}, {{y: 0, opacity: 1, rotationX: 0, duration: 0.5, ease: "expo.out"}}, {t - 0.2:.2f});')
    T(f'tl.to("#n{i}", {{boxShadow: "0 0 0 2px {"#7EF0C0" if i == 4 else "#3EC5FF"}, 0 0 50px {"rgba(126,240,192,0.65)" if i == 4 else "rgba(62,197,255,0.6)"}", duration: 0.25}}, {t + 0.15:.2f});')
    if i < 4:
        T(f'tl.fromTo("#k{i}", {{scaleX: 0}}, {{scaleX: 1, duration: 0.3, ease: "power2.inOut"}}, {t + 0.2:.2f});')
# a light pulse travels the whole flow, from the link into Commission
T('tl.fromTo("#dot", {x: 150, y: -210, opacity: 0}, {x: 270, y: 0, opacity: 1, duration: 0.4, ease: "power2.in"}, 4.75);')
T('tl.to("#dot", {x: 1650, duration: 2.0, ease: "none"}, 5.15);')
T('tl.to("#dot", {scale: 3, opacity: 0, duration: 0.3}, 7.15);')
T('tl.fromTo("#n4 .nic", {scale: 1}, {scale: 1.25, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out"}, 7.15);')
T('tl.to("#s2 .flow, #pill", {opacity: 0, y: "-=40", filter: "blur(12px)", duration: 0.4, ease: "power2.in"}, 7.7);')
headline("h2", 4.3, 3.6, "Share your link. Earn on every sale.", top=900)

# ---------------------------------------------------------------- 3. commission cards (8.0 - 13.3)
def big_card(cid, title, desc, items, us, left):
    rows = ""
    for i, (n, a, cap) in enumerate(items):
        rows += (f'<div class="brow" id="{cid}r{i}" style="top:{150 + i * 68}px"><span>{n}</span>'
                 f'<b class="val" id="{cid}v{i}">{"0% · up to $0" if us else "$0 per sale"}</b></div>')
    return (f'<div class="bcard" id="{cid}" style="left:{left}px"><div class="bt">{title}</div><div class="bd">{desc}</div>{rows}</div>')


clip("s3", 8.0, 5.3,
     '<div class="stage3"><div class="earnhead" id="eh">' + ic("earn", 34, "#3EC5FF", 2) + ' What you earn</div>'
     + big_card("cd", "Dubai Company Referrals", "A UAE free-zone company: trade licence, plus residence visas for the owner and family if they want them.", DUBAI, False, 140)
     + big_card("cu", "US LLC Referrals", "A US limited liability company for founders anywhere: formation, EIN and registered agent, with tax filing on the higher tiers.", US, True, 980)
     + '<div class="when" id="when">Dubai referrals earn when the company licence is issued  ·  US LLC referrals earn when the client pays</div></div>', track=2)
T('tl.fromTo("#eh", {y: 40, opacity: 0}, {y: 0, opacity: 1, duration: 0.5, ease: "expo.out"}, 8.05);')
T('tl.fromTo("#cd", {rotationX: 35, y: 260, opacity: 0}, {rotationX: 0, y: 0, opacity: 1, duration: 0.75, ease: "expo.out"}, 8.1);')
T('tl.fromTo("#cu", {rotationX: 35, y: 260, opacity: 0}, {rotationX: 0, y: 0, opacity: 1, duration: 0.75, ease: "expo.out"}, 8.25);')
T('tl.fromTo("#s3 .stage3", {scale: 1, rotationY: 3}, {scale: 1.05, rotationY: -3, duration: 5.3, ease: "none"}, 8.0);')
for side, items, us, t0 in (("cd", DUBAI, False, 8.85), ("cu", US, True, 10.45)):
    for i, (n, a, cap) in enumerate(items):
        t = t0 + i * 0.5
        if us:
            fmt = '`${Math.round(o.p)}% · up to $${Math.round(o.c)}`'
            T(f'(() => {{ const o = {{p: 0, c: 0}}, el = document.getElementById("{side}v{i}"); '
              f'tl.to(o, {{p: {a}, c: {cap}, duration: 0.7, ease: "power2.out", onUpdate: () => {{ el.textContent = {fmt}; }}}}, {t:.2f}); }})();')
        else:
            fmt = '`$${Math.round(o.v)} per sale`'
            T(f'(() => {{ const o = {{v: 0}}, el = document.getElementById("{side}v{i}"); '
              f'tl.to(o, {{v: {a}, duration: 0.7, ease: "power2.out", onUpdate: () => {{ el.textContent = {fmt}; }}}}, {t:.2f}); }})();')
        T(f'tl.fromTo("#{side}r{i}", {{backgroundColor: "rgba(126,240,192,0)"}}, {{backgroundColor: "rgba(126,240,192,0.12)", duration: 0.25, yoyo: true, repeat: 1, repeatDelay: 0.3}}, {t:.2f});')
        T(f'tl.fromTo("#{side}v{i}", {{textShadow: "0 0 0px rgba(126,240,192,0)"}}, {{textShadow: "0 0 18px rgba(126,240,192,0.9)", duration: 0.3, yoyo: true, repeat: 1, repeatDelay: 0.25}}, {t + 0.2:.2f});')
T('tl.fromTo("#when", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: 0.4}, 12.0);')
T('tl.to("#s3 .stage3", {y: -120, opacity: 0, filter: "blur(16px)", duration: 0.4, ease: "power2.in"}, 12.9);')

# ---------------------------------------------------------------- 4. pipeline (13.2 - 18.0)
SW, SG = 214, 26
pst = ""
for i, s in enumerate(STAGES):
    x = 30 + i * (SW + SG)
    pst += (f'<div class="bst" id="st{i}" style="left:{x}px"><span>{s.upper()}</span>'
            f'<b><i class="z" id="z{i}">0</i><i class="o" id="o{i}">1</i></b>{ic("check", 22, "#7EF0C0", 2.4) if i == 6 else ""}</div>')
    if i < 6:
        pst += f'<div class="bch" style="left:{x + SW + 4}px">›</div>'
clip("s4", 13.2, 4.8,
     '<div class="stage4"><div class="pcard" id="pcard"><div class="plab">REFERRAL PIPELINE</div><div class="ptot">1 total</div>'
     f'{pst}<div class="rail"><div class="fill" id="fill"></div></div>'
     f'<div class="hl" id="phl" style="left:{30 - 4}px"></div></div>'
     '<div class="chip" id="chip">' + ic("user", 18) + ' Demo client  ·  Dubai  ·  Business License + 1 Residency Visa</div></div>', track=2)
T('tl.fromTo("#pcard", {rotationX: -30, y: 200, opacity: 0, scale: 0.9}, {rotationX: 0, y: 0, opacity: 1, scale: 1, duration: 0.7, ease: "expo.out"}, 13.2);')
T('tl.fromTo("#chip", {y: -30, opacity: 0}, {y: 0, opacity: 1, duration: 0.45, ease: "expo.out"}, 13.5);')
T('tl.fromTo("#phl", {opacity: 0}, {opacity: 1, duration: 0.2}, 13.8);')
T('tl.fromTo("#fill", {scaleX: 0}, {scaleX: 1 / 7, duration: 0.3}, 13.8);')
T('tl.set("#z0", {opacity: 0}, 13.85); tl.set("#o0", {opacity: 1}, 13.85);')
for i in range(1, 7):
    t = 13.8 + i * 0.5
    T(f'tl.to("#phl", {{x: {i * (SW + SG)}, duration: 0.32, ease: "power3.inOut"}}, {t:.2f});')
    T(f'tl.to("#fill", {{scaleX: {(i + 1) / 7:.4f}, duration: 0.32, ease: "power3.inOut"}}, {t:.2f});')
    T(f'tl.set("#o{i - 1}", {{opacity: 0}}, {t + 0.16:.2f}); tl.set("#z{i - 1}", {{opacity: 1}}, {t + 0.16:.2f});')
    T(f'tl.set("#z{i}", {{opacity: 0}}, {t + 0.16:.2f}); tl.set("#o{i}", {{opacity: 1}}, {t + 0.16:.2f});')
    T(f'tl.fromTo("#st{i}", {{scale: 1}}, {{scale: 1.06, duration: 0.15, yoyo: true, repeat: 1}}, {t + 0.16:.2f});')
T('tl.to("#phl", {boxShadow: "0 0 0 3px #7EF0C0, 0 0 50px rgba(126,240,192,0.7)", duration: 0.2}, 16.3);')
T('tl.fromTo("#st6 .ic", {scale: 0, opacity: 0}, {scale: 1, opacity: 1, duration: 0.35, ease: "back.out(3)"}, 16.95);')
T('tl.to("#s4 .stage4", {scale: 0.9, opacity: 0, filter: "blur(14px)", duration: 0.4, ease: "power2.in"}, 17.6);')
headline("h4", 13.4, 4.4, "Track every referral, from lead to completed.", top=170)

# ---------------------------------------------------------------- 5. final composition (17.8 - 24)
clip("s5", 17.8, 6.2,
     f'<div class="lens"><div class="cam" id="cam5"><div class="world" id="w5">{dashboard("d5")}</div></div></div>'
     f'<div class="pill small" id="pill5"><span class="pic">{ic("link", 22)}</span><span>portal.genzone.com/r/{CODE}</span>'
     f'<span class="pcopy">{ic("copy", 16)}Copy link</span></div>'
     '<div class="notif" id="notif"><div class="nicon">' + ic("dollar", 30, "#0B1220", 2.2) + '</div>'
     '<div class="ntext"><div class="ntop"><b>GenZone</b><span>now</span></div><div class="ntitle">Commission earned</div>'
     '<div class="namt"><b>+$500.00</b> · Business License + 1 Residency Visa</div></div></div>'
     '<div class="tag" id="tag"><div class="tl1">Share your link.</div><div class="tl2">Refer clients.</div>'
     '<div class="tl3">Earn commissions.</div></div>'
     f'<div class="lock" id="lock"><img src="{LOGO}" alt="GenZone"><div class="cta">Join the referral program  ·  genzone.com</div></div>', track=2)
T(f'tl.fromTo("#w5", {{{cam(860, 400, 0.5)}}}, {{{cam(860, 400, 0.56)}, duration: 6.2, ease: "none"}}, 17.8);')
T('tl.fromTo("#cam5", {rotationY: -40, rotationX: 14, x: 700, y: 40, opacity: 0}, {rotationY: -20, rotationX: 8, x: 380, y: 40, opacity: 1, duration: 1.0, ease: "expo.out"}, 17.8);')
T('tl.to("#cam5", {rotationY: -16, duration: 5.2, ease: "none"}, 18.8);')
T('tl.fromTo("#d5 .card, #d5 .side", {opacity: 0}, {opacity: 1, duration: 0.4, stagger: 0.04}, 17.85);')
T('tl.fromTo("#tag > div", {y: 70, opacity: 0, filter: "blur(12px)"}, {y: 0, opacity: 1, filter: "blur(0px)", duration: 0.55, ease: "expo.out", stagger: 0.35}, 18.2);')
T('tl.fromTo("#pill5", {x: -200, y: 80, opacity: 0, scale: 0.9}, {x: 0, y: 0, opacity: 1, scale: 1, duration: 0.7, ease: "expo.out"}, 18.7);')
T('tl.fromTo("#notif", {y: -160, opacity: 0, scale: 0.92}, {y: 0, opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)"}, 19.6);')
T('tl.to("#notif", {boxShadow: "0 0 0 1.5px rgba(126,240,192,0.9), 0 0 70px rgba(126,240,192,0.55), 0 30px 70px rgba(0,0,0,0.5)", duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut"}, 20.1);')
T('tl.fromTo("#notif .namt b", {scale: 1}, {scale: 1.08, duration: 0.2, yoyo: true, repeat: 1}, 20.0);')
T('tl.fromTo("#lock", {y: 40, opacity: 0}, {y: 0, opacity: 1, duration: 0.6, ease: "expo.out"}, 21.0);')
T('tl.fromTo("#lock .cta", {boxShadow: "0 0 0 1px rgba(62,197,255,0.4)"}, {boxShadow: "0 0 0 2px #3EC5FF, 0 0 40px rgba(62,197,255,0.6)", duration: 0.6, yoyo: true, repeat: 2}, 21.6);')
T('tl.to("#s5 > *", {opacity: 0, duration: 0.45}, 23.5);')

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
