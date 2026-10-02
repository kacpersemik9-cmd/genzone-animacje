#!/usr/bin/env python3
"""GenZone Referral Dashboard — 30s launch video. Generates index.html.

No screenshots folder exists, so the dashboard is rebuilt in HTML/CSS from the
storyboard screens. The logo mark, wordmark and QR are real crops from the
storyboard PDF (assets/img). Run: python3 build.py
"""

# ---------------------------------------------------------------- layout
# Dashboard frame: 1500x800, placed at (210, 70) inside a 1920x1080 camera layer.
DX, DY = 210, 70


def cam_to(px, py, s, tx=960, ty=470):
    """Camera transform (origin 0 0) that puts dashboard-local point (px,py) at
    screen point (tx,ty) with scale s."""
    return dict(x=round(tx - (DX + px) * s, 1), y=round(ty - (DY + py) * s, 1), scale=s)


def js(d):
    return "{" + ", ".join(f"{k}: {v}" for k, v in d.items()) + "}"


NAV = ["Referral Dashboard", "Payouts", "Marketing Tools", "Resources"]
NAV_ICONS = ["◎", "▣", "✦", "▤"]


def sidebar(active):
    items = "".join(
        f'<div class="nav{" on" if n == active else ""}" style="top:{120 + i * 56}px">'
        f'<span class="ni">{NAV_ICONS[i]}</span>{n}{"<span class=chev>›</span>" if n == active else ""}</div>'
        for i, n in enumerate(NAV))
    return (f'<div class="side"><img class="side-logo" src="assets/img/wordmark.png" alt="GenZone">{items}'
            '<div class="back">← Back to main dashboard</div>'
            '<div class="acct"><span class="av">D</span><div><b>Account</b><small>Manage profile</small></div></div></div>')


def frame(inner, active, did):
    return (f'<div class="dash" id="{did}"><div class="dash-in">{sidebar(active)}'
            f'<div class="main"><div class="dim"></div>{inner}</div></div></div>')


STATS = [("Total earned", "$2,150.00", "No prior activity"),
         ("Pending payout", "$750.00", "No prior activity"),
         ("Active referrals", "16", "<em>↗ 25%</em> vs last 30 days"),
         ("Conversion rate", "37.5%", "No prior activity")]

VIEW_REFER = (
    '<div class="h1" style="left:24px;top:30px">Refer &amp; Earn</div>'
    '<div class="sub" style="left:24px;top:80px">Code GENZ-AGESAS</div>'
    '<div class="badge" style="right:24px;top:40px">● Approved</div>'
    + "".join(f'<div class="card stat" style="left:{24 + i * 302}px;top:124px">'
              f'<div class="lab">{l}</div><div class="val">{v}</div><div class="note">{n}</div></div>'
              for i, (l, v, n) in enumerate(STATS))
    + '<div class="card" style="left:24px;top:268px;width:584px;height:500px">'
      '<div class="lab" style="position:absolute;left:24px;top:24px">YOUR CODE</div>'
      '<div class="code" style="position:absolute;left:24px;top:46px">GENZ-AGESAS</div>'
      '<div class="body" style="position:absolute;left:24px;top:96px;width:300px">Your link and code, unique to you. '
      'Share either one. Anyone who forms their company through it is credited to you automatically.</div>'
      '<div class="qr" style="position:absolute;left:356px;top:28px"><img src="assets/img/qr.png" alt="QR code"></div>'
      '<div class="btn ghost" style="position:absolute;left:372px;top:248px">⤓ Download QR</div>'
      '<div class="field mono" style="position:absolute;left:24px;top:330px;width:536px">https://portal.genzone.com/r/GENZ-AGESAS</div>'
      '<div class="btnrow" style="position:absolute;left:24px;top:404px">'
      '<div class="btn ghost" id="copy1">⧉ Copy link</div><div class="btn green">⇪ Share</div><div class="btn ghost">↗ Preview</div></div>'
      '</div>'
    + '<div class="card" style="left:632px;top:268px;width:552px;height:500px">'
      '<div class="h3" style="position:absolute;left:24px;top:24px">Refer someone</div>'
      '<div class="flab" style="left:24px;top:70px">THEIR NAME *</div><div class="field" style="left:24px;top:92px;width:240px">Jane Doe</div>'
      '<div class="flab" style="left:288px;top:70px">THEIR EMAIL *</div><div class="field" style="left:288px;top:92px;width:240px">jane@company.com</div>'
      '<div class="flab" style="left:24px;top:160px">THEIR NUMBER *</div><div class="field" style="left:24px;top:182px;width:240px">+971 50 000 0000</div>'
      '<div class="flab" style="left:288px;top:160px">INTERESTED IN (optional)</div><div class="field" style="left:288px;top:182px;width:240px">Not sure yet ⌄</div>'
      '<div class="flab" style="left:24px;top:250px">THEIR SITUATION (optional)</div>'
      '<div class="field" style="left:24px;top:272px;width:504px;height:110px;white-space:normal">What are they trying to do? Anything our team should know before reaching out.</div>'
      '<div class="small" style="position:absolute;left:24px;top:432px">Referred by <b>GENZ-AGESAS</b></div>'
      '<div class="btn blue" style="position:absolute;right:24px;top:420px">➤ Submit referral</div>'
      '</div>')

PIPE = [("Lead", "3"), ("Call booked", "3"), ("Signed up", "3"), ("Applied", "0"),
        ("In review", "1"), ("Paid", "6"), ("Completed", "0")]
ROWS = [("Abbasd Ahamd", "Call booked", "Sep 3, 2026"), ("i***@g***.com", "Signed up", "Aug 28, 2026"),
        ("Abbas Ahmad", "Lead", "Aug 27, 2026"), ("Shayan Nasiri", "Lead", "Aug 20, 2026"),
        ("Abbas Ahmad", "Lead", "Aug 20, 2026"), ("d***@e***.com", "Signed up", "Aug 12, 2026")]
BARS = {4: 500, 5: 200, 6: 100, 7: 500, 8: 500, 9: 200}   # month index -> USD
MONTHS = "Oct Nov Dec Jan Feb Mar Apr May Jun Jul Aug Sep".split()


def bar_chart():
    w, h, x0, y0 = 520, 200, 40, 10
    out = [f'<svg width="{w + 50}" height="{h + 40}" class="chart">']
    for v in (0, 150, 300, 450, 600):
        y = y0 + h - v / 600 * h
        out.append(f'<line x1="{x0}" x2="{x0 + w}" y1="{y}" y2="{y}" class="gl"/><text x="0" y="{y + 4}" class="ax">{v}</text>')
    bw = w / 12
    for i, m in enumerate(MONTHS):
        cx = x0 + bw * i + bw / 2
        out.append(f'<text x="{cx}" y="{y0 + h + 22}" class="ax" text-anchor="middle">{m}</text>')
        if i in BARS:
            bh = BARS[i] / 600 * h
            out.append(f'<rect class="bar" data-y="{y0 + h - bh:.1f}" data-h="{bh:.1f}" data-base="{y0 + h}" x="{cx - 13}" y="{y0 + h - bh:.1f}" width="26" height="{bh:.1f}" rx="3"/>')
    out.append("</svg>")
    return "".join(out)


def area_chart():
    w, h, x0, y0 = 520, 200, 40, 10
    vals = [0, 0, 0, 0, 11500, 1200, 800, 9000, 5000, 1000, 0, 0]
    pts = [(x0 + w / 11 * i, y0 + h - v / 12000 * h) for i, v in enumerate(vals)]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        mx = (ax + bx) / 2
        d += f" C{mx:.1f},{ay:.1f} {mx:.1f},{by:.1f} {bx:.1f},{by:.1f}"
    out = [f'<svg width="{w + 50}" height="{h + 40}" class="chart">']
    for v, lab in ((0, "0"), (3000, "3K"), (6000, "6K"), (9000, "9K"), (12000, "12K")):
        y = y0 + h - v / 12000 * h
        out.append(f'<line x1="{x0}" x2="{x0 + w}" y1="{y}" y2="{y}" class="gl"/><text x="0" y="{y + 4}" class="ax">{lab}</text>')
    for i, m in enumerate(MONTHS):
        out.append(f'<text x="{x0 + w / 11 * i}" y="{y0 + h + 22}" class="ax" text-anchor="middle">{m}</text>')
    out.append(f'<path d="{d} L{x0 + w},{y0 + h} L{x0},{y0 + h} Z" class="area"/><path d="{d}" class="aline" pathLength="1"/>')
    out.append("</svg>")
    return "".join(out)


def pill(stage):
    return f'<span class="pill {stage.split()[0].lower()}">● {stage}</span>'


VIEW_TRACK = (
    '<div class="card" id="pipe" style="left:24px;top:24px;width:1160px;height:116px">'
    '<div class="lab" style="position:absolute;left:20px;top:16px">REFERRAL PIPELINE</div>'
    '<div class="small" style="position:absolute;right:20px;top:14px">16 total</div>'
    + "".join(f'<div class="stage" style="left:{20 + i * 162}px"><span>{n.upper()}</span><b{" class=goldnum" if n == "Paid" else ""}>{v}</b></div>'
              + (f'<div class="arrow" style="left:{20 + i * 162 + 146}px">›</div>' if i < 6 else "")
              for i, (n, v) in enumerate(PIPE))
    + '</div>'
    '<div class="card pop" id="table" style="left:24px;top:160px;width:1160px;height:314px">'
    '<div class="h3" style="position:absolute;left:20px;top:16px">👥 Referral tracking</div>'
    '<div class="small" style="position:absolute;right:20px;top:18px">16 total</div>'
    '<div class="thead"><span style="left:20px">CONTACT</span><span style="left:330px">PACKAGE</span>'
    '<span style="left:520px">DEAL VALUE</span><span style="left:700px">YOUR COMMISSION</span>'
    '<span style="left:880px">STAGE</span><span style="right:20px">DATE</span></div>'
    + "".join(f'<div class="trow" style="top:{90 + i * 37}px"><span style="left:20px">{n}</span>'
              f'<span style="left:340px">—</span><span style="left:540px">—</span><span style="left:740px">—</span>'
              f'<span style="left:880px">{pill(s)}</span><span style="right:20px">{d}</span></div>'
              for i, (n, s, d) in enumerate(ROWS))
    + '</div>'
    f'<div class="card pop" id="ch1" style="left:24px;top:494px;width:568px;height:282px">'
    f'<div class="lab" style="position:absolute;left:20px;top:16px">COMMISSIONS EARNED</div>'
    f'<div class="small" style="position:absolute;right:20px;top:14px">USD</div>'
    f'<div style="position:absolute;left:10px;top:44px">{bar_chart()}</div></div>'
    f'<div class="card pop" id="ch2" style="left:616px;top:494px;width:568px;height:282px">'
    f'<div class="lab" style="position:absolute;left:20px;top:16px">REFERRED DEAL VALUE</div>'
    f'<div class="small" style="position:absolute;right:20px;top:14px">USD</div>'
    f'<div style="position:absolute;left:10px;top:44px">{area_chart()}</div></div>')

VIEW_MARKETING = (
    '<div class="h1" style="left:24px;top:30px">Marketing Tools</div>'
    '<div class="sub" style="left:24px;top:80px">Copy that\'s ready to post, with your link already in it.</div>'
    '<div class="card" id="linkbar" style="left:24px;top:124px;width:1160px;height:70px">'
    '<div class="mono" style="position:absolute;left:24px;top:24px;font-size:17px">⛓ https://portal.genzone.com/r/GENZ-AGESAS</div>'
    '<div class="btn blue" id="copy2" style="position:absolute;right:16px;top:13px">⧉ Copy link</div></div>'
    '<div class="tabs" id="tabs" style="left:24px;top:216px"><span class="on">LinkedIn</span><span>X</span>'
    '<span>Instagram</span><span>WhatsApp</span><span>Email</span></div>'
    '<div class="card" style="left:24px;top:276px;width:568px;height:330px">'
    '<div class="h3" style="position:absolute;left:20px;top:18px">Short post</div><div class="btn ghost sm" style="position:absolute;right:16px;top:14px">⧉ Copy</div>'
    '<div class="small" style="position:absolute;left:20px;top:48px">Best for a general audience: leads with the problem, not the product.</div>'
    '<div class="field" style="left:20px;top:84px;width:528px;height:220px;white-space:normal;line-height:1.6">'
    'Most founders I talk to want a company in Dubai or the US, then stall on the paperwork.<br><br>'
    'I\'ve been recommending GenZone. They handle the formation end to end (licence, visas, bank account intro) '
    'and they tell you what it actually costs before you commit.</div></div>'
    '<div class="card" style="left:616px;top:276px;width:568px;height:330px">'
    '<div class="h3" style="position:absolute;left:20px;top:18px">Personal story</div><div class="btn ghost sm" style="position:absolute;right:16px;top:14px">⧉ Copy</div>'
    '<div class="small" style="position:absolute;left:20px;top:48px">Higher engagement. Replace the first line with your own experience.</div>'
    '<div class="field" style="left:20px;top:84px;width:528px;height:220px;white-space:normal;line-height:1.6">'
    '[Say what happened to you here: the quote you got, the month you lost, the thing nobody explained.]<br><br>'
    'That\'s why I point people at GenZone now. Clear pricing, a real person on WhatsApp, and they set up '
    'companies in both Dubai and the US.</div></div>'
    '<div class="card" style="left:24px;top:626px;width:568px;height:150px">'
    '<div class="h3" style="position:absolute;left:20px;top:18px">Caption for an image post</div>'
    '<div class="small" style="position:absolute;left:20px;top:48px">Pair with a banner from the asset library below.</div>'
    '<div class="field" style="left:20px;top:84px;width:528px">Dubai or the US? The right answer depends on where your customers are…</div></div>')

FAQ = [("When does a referral become a commission?",
        "When the person you referred pays for their formation. Signing up is not enough: the commission accrues against their first paid order."),
       ("How long does my link stay attached to someone?",
        "Indefinitely. Once someone arrives through your link they stay attached to you. There is no window to beat."),
       ("When do I get paid?",
        "Commissions are approved first, then batched into a payout by the GenZone team. The Payouts page shows what is approved and waiting."),
       ("What happens if a client refunds?",
        "An unpaid commission is reversed. If it was already paid out to you, it stays paid and is settled against future earnings."),
       ("Can I refer myself or my own company?",
        "No. Self-referral is blocked automatically, and the referral will not attribute.")]
VIEW_FAQ = ('<div class="card" style="left:24px;top:40px;width:1160px;height:736px">'
            '<div class="h3" style="position:absolute;left:28px;top:26px">ⓘ Common questions</div>'
            + "".join(f'<div class="qa" style="top:{80 + i * 128}px"><b>{q}</b><p>{a}</p></div>' for i, (q, a) in enumerate(FAQ))
            + '</div>')

VIEW_PAYOUTS = (
    '<div class="h1" style="left:24px;top:30px">Payouts</div>'
    '<div class="sub" style="left:24px;top:80px">What you\'re owed, what we\'ve sent, and where it goes.</div>'
    '<div class="card" style="left:24px;top:124px;width:568px;height:226px">'
    '<div class="h3" style="position:absolute;left:20px;top:18px">▣ Payouts</div>'
    '<div class="avail" id="avail"><div class="lab">AVAILABLE TO PAY OUT</div><div class="val">$500.00</div>'
    '<div class="note">Approved commissions not yet included in a payout.</div></div>'
    '<div class="small" style="position:absolute;left:20px;top:192px">No payout is currently being processed.</div></div>'
    '<div class="card" style="left:616px;top:124px;width:568px;height:226px">'
    '<div class="h3" style="position:absolute;left:20px;top:18px">▣ Payout history</div>'
    '<div class="small" style="position:absolute;left:20px;top:54px">No payouts yet.</div></div>'
    '<div class="card" style="left:24px;top:374px;width:1160px;height:402px">'
    '<div class="h3" style="position:absolute;left:20px;top:18px">🏛 Payout settings</div>'
    '<div class="flab" style="left:20px;top:62px">Method</div><div class="field" style="left:20px;top:84px;width:1120px">Bank transfer</div>'
    '<div class="flab" style="left:20px;top:150px">Account holder</div><div class="field" style="left:20px;top:172px;width:548px">Full name on the account</div>'
    '<div class="flab" style="left:592px;top:150px">Bank name</div><div class="field" style="left:592px;top:172px;width:548px">e.g. Emirates NBD</div>'
    '<div class="flab" style="left:20px;top:238px">Account number / IBAN</div><div class="field" style="left:20px;top:260px;width:548px">IBAN or account number</div>'
    '<div class="flab" style="left:592px;top:238px">SWIFT / BIC</div><div class="field" style="left:592px;top:260px;width:548px">e.g. EBILAEAD</div>'
    '<div class="btn blue" style="position:absolute;left:20px;top:330px">💾 Save payout method</div></div>')

EARN_DUBAI = [("Dubai Business License", "$500.00"), ("Business License + 1 Residency Visa", "$500.00"),
              ("Business License + 2 Residency Visas (or more)", "$750.00")]
EARN_US = [("Basic", "$150.00"), ("Advanced", "$250.00"), ("Done-For-You", "$500.00")]


def earn_table(eid, hl):
    def col(x, title, desc, rows, key):
        return (f'<div class="ecol" style="left:{x}px"><b class="et">{title}</b><p>{desc}</p>'
                + "".join(f'<div class="erow{" hl" if (key, i) == hl else ""}" style="top:{118 + i * 50}px">'
                          f'<span>{n}</span><span class="money">{v}</span></div>' for i, (n, v) in enumerate(rows))
                + '</div>')
    return (f'<div class="earn" id="{eid}"><div class="h3" style="position:absolute;left:28px;top:22px">✓ What you earn</div>'
            + col(24, "Dubai Company Referrals", "A UAE free-zone company: trade licence, plus residence visas for the owner and family if they want them.", EARN_DUBAI, "d")
            + col(666, "US LLC Referrals", "A US limited liability company for founders anywhere: formation, EIN and registered agent, with tax filing on the higher tiers.", EARN_US, "u")
            + '<div class="small" style="position:absolute;left:28px;top:392px">Paid once your referral pays for their formation. '
              'The rate is fixed at that moment, so a later change never moves what you have already earned.</div></div>')


# ------------------------------------------------------------------ scenes
clips, tw = [], []


def clip(cid, start, dur, html, track=2, cls="scene"):
    clips.append(f'<div id="{cid}" class="clip {cls}" data-start="{start}" data-duration="{dur}" data-track-index="{track}">{html}</div>')


def line(cid, start, dur, text):
    clip(cid, start, dur, f'<div class="line">{text}</div>', track=9, cls="linewrap")
    tw.append(f'tl.fromTo("#{cid} .line", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.4, ease: "power3.out"}}, {start + 0.05});')


# Background (whole film) + grid (dashboard scenes)
clip("bg", 0, 30, '<div class="glow"></div><div class="leak tl"></div><div class="leak br"></div>', track=0, cls="bgl")
clip("grid", 3, 23, '<div class="gridlines"></div>', track=1, cls="bgl")
tw.append('tl.fromTo("#grid .gridlines", {opacity: 0}, {opacity: 1, duration: 0.6}, 3);')

# 1. Logo reveal 0-3
WAVE = ("M-200,700 C200,520 420,380 760,560 C1080,740 1300,260 1560,120 L2200,-200 L2200,300 "
        "C1700,420 1500,900 1080,980 C700,1060 420,820 -200,1060 Z")
clip("s1", 0, 3, f'<svg class="wave" viewBox="0 0 1920 1080" preserveAspectRatio="none"><defs>'
     '<radialGradient id="wg" cx="55%" cy="65%" r="60%"><stop offset="0" stop-color="#2B63F0"/><stop offset="1" stop-color="#14306f"/></radialGradient></defs>'
     f'<path d="{WAVE}" fill="url(#wg)"/></svg>'
     '<img class="mark" id="mark1" src="assets/img/mark.png" alt="">'
     '<img class="wordmark" id="wm1" src="assets/img/wordmark.png" alt="GenZone">')
tw += ['tl.fromTo("#s1 .wave", {clipPath: "inset(0% 100% 0% 0%)", opacity: 1}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.8, ease: "power3.inOut"}, 0);',
       'tl.to("#s1 .wave", {opacity: 0, duration: 0.5, ease: "power1.out"}, 1.2);',
       'tl.fromTo("#mark1", {scale: 0.2, rotation: -120, opacity: 0}, {scale: 1, rotation: 0, opacity: 1, duration: 0.8, ease: "back.out(1.4)"}, 0.45);',
       'tl.to("#mark1", {scale: 0.215, x: 109, y: 5, duration: 0.55, ease: "power3.inOut"}, 1.35);',
       'tl.fromTo("#wm1", {opacity: 0, scale: 1.08}, {opacity: 1, scale: 1, duration: 0.45, ease: "power2.out"}, 1.6);',
       'tl.to("#mark1", {opacity: 0, duration: 0.15}, 1.9);']
line("l1", 1.9, 1.1, "Your partner in business formation and growth.")

# 2. Chart 3-6
PTS = [(330, 870), (600, 620), (760, 680), (880, 590), (1040, 570), (1260, 300), (1530, 180)]
path = "M" + " L".join(f"{x},{y}" for x, y in PTS)
seglen = [((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** .5 for a, b in zip(PTS, PTS[1:])]
total = sum(seglen)
coins = "".join(f'<div class="coin" id="coin{i}" style="left:{x - 30}px;top:{y - 30}px">$</div>' for i, (x, y) in enumerate(PTS))
clip("s2", 3, 3, f'<svg class="chartline" viewBox="0 0 1920 1080"><path id="cl" d="{path}" pathLength="{total:.0f}" '
     f'style="stroke-dasharray:{total:.0f};stroke-dashoffset:{total:.0f}"/></svg>{coins}')
tw.append(f'tl.fromTo("#cl", {{strokeDashoffset: {total:.0f}}}, {{strokeDashoffset: 0, duration: 2.0, ease: "power1.inOut"}}, 3.1);')
acc = 0
for i in range(len(PTS)):
    t = 3.1 + 2.0 * (acc / total) if i else 3.1
    tw.append(f'tl.fromTo("#coin{i}", {{scale: 0, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.5)"}}, {t:.2f});')
    if i < len(seglen):
        acc += seglen[i]
tw.append('tl.to("#s2 svg, #s2 .coin", {y: -40, duration: 3, ease: "none"}, 3);')
line("l2", 3.2, 2.8, "From US LLCs to Dubai company setup.")

# 3. Dashboard rise 6-10
clip("s3", 6, 4, f'<div class="stage3d"><div class="cam" id="cam3">{frame(VIEW_REFER, "Referral Dashboard", "d3")}</div></div>')
tw += ['tl.fromTo("#d3", {rotationX: 58, y: 520, opacity: 0}, {rotationX: 0, y: 0, opacity: 1, duration: 1.0, ease: "power3.out"}, 6);',
       f'tl.fromTo("#cam3", {js(cam_to(750, 400, 1, 960, 470))}, {{...{js(cam_to(904, 184, 1.5))}, duration: 0.7, ease: "power3.inOut"}}, 7.1);',
       'tl.fromTo("#d3 .stat", {y: 16, opacity: 0.4}, {y: 0, opacity: 1, duration: 0.35, stagger: 0.08, ease: "power2.out"}, 7.4);',
       f'tl.to("#cam3", {{...{js(cam_to(300 + 24 + 292, 268 + 250, 1.6))}, duration: 0.7, ease: "power3.inOut"}}, 8.5);',
       'tl.fromTo("#copy1", {boxShadow: "0 0 0px rgba(62,197,255,0)"}, {boxShadow: "0 0 34px rgba(62,197,255,0.9)", duration: 0.3, yoyo: true, repeat: 1}, 9.2);']
line("l3", 6.6, 3.4, "Turn your network into earnings.")

# 4. Tracking 10-15
clip("s4", 10, 5, f'<div class="stage3d"><div class="cam" id="cam4">{frame(VIEW_TRACK, "Referral Dashboard", "d4")}</div></div>')
tw += ['tl.fromTo("#d4 .main", {y: 140}, {y: 0, duration: 0.5, ease: "power3.out"}, 10);',
       f'tl.fromTo("#cam4", {js(cam_to(300 + 604, 82, 1.45))}, {{...{js(cam_to(300 + 604, 82, 1.55))}, duration: 1.2, ease: "none"}}, 10);',
       'tl.fromTo("#d4 .stage", {y: 18, opacity: 0}, {y: 0, opacity: 1, duration: 0.25, stagger: 0.08, ease: "power2.out"}, 10.1);',
       f'tl.to("#cam4", {{...{js(cam_to(750, 400, 0.98))}, duration: 0.6, ease: "power3.inOut"}}, 11.2);',
       'tl.to("#d4 .dim", {opacity: 1, duration: 0.4}, 11.6);',
       'tl.to("#table", {scale: 1.05, y: -40, boxShadow: "0 0 0 2px #3EC5FF, 0 0 60px rgba(62,197,255,0.55), 0 30px 80px rgba(0,0,0,0.6)", duration: 0.5, ease: "back.out(1.6)"}, 11.6);',
       'tl.fromTo("#d4 .trow", {x: -20, opacity: 0.2}, {x: 0, opacity: 1, duration: 0.25, stagger: 0.06}, 11.8);',
       'tl.to("#ch1", {scale: 1.08, x: -50, y: 10, boxShadow: "0 0 0 2px #3EC5FF, 0 0 60px rgba(62,197,255,0.55), 0 30px 80px rgba(0,0,0,0.6)", duration: 0.5, ease: "back.out(1.6)"}, 12.7);',
       'tl.to("#ch2", {scale: 1.08, x: 50, y: 10, boxShadow: "0 0 0 2px #3EC5FF, 0 0 60px rgba(62,197,255,0.55), 0 30px 80px rgba(0,0,0,0.6)", duration: 0.5, ease: "back.out(1.6)"}, 12.9);',
       'document.querySelectorAll("#ch1 .bar").forEach((r, i) => tl.fromTo(r, {attr: {y: +r.dataset.base, height: 0}}, {attr: {y: +r.dataset.y, height: +r.dataset.h}, duration: 0.5, ease: "power3.out"}, 12.9 + i * 0.06));',
       'tl.fromTo("#ch2 .aline", {strokeDashoffset: 1}, {strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut"}, 13.1);']
line("l4", 10.3, 4.7, "Track every referral from your dashboard.")


# 5. Kinetic money 15-20
def headline(cid, start, dur, money, mid, last):
    words = ([f'<span class="w gold">{money}</span>'] + [f'<span class="w silver">{w}</span>' for w in mid.split()]
             + [f'<span class="w blue">{last}</span>'])
    clip(cid, start, dur, f'<div class="headline">{" ".join(words)}</div>')
    tw.append(f'tl.fromTo("#{cid} .w", {{yPercent: 60, opacity: 0, scale: 1.3}}, {{yPercent: 0, opacity: 1, scale: 1, '
              f'duration: 0.32, ease: "expo.out", stagger: 0.12}}, {start});')
    tw.append(f'tl.fromTo("#{cid} .headline", {{scale: 1}}, {{scale: 1.06, duration: {dur}, ease: "none"}}, {start});')


def earn_zoom(cid, start, dur, hl, row_xy):
    clip(cid, start, dur, f'<div class="earnwrap" id="{cid}w">{earn_table(cid + "t", hl)}</div>')
    rx, ry = row_xy                     # row centre in table-local px; table is 1300x440 centred
    tx, ty = 960 - 650 + rx, 540 - 220 + ry
    tw.append(f'tl.fromTo("#{cid}w", {{scale: 1, x: 0, y: 0}}, {{scale: 2.1, x: {(960 - tx) * 2.1:.0f}, y: {(540 - ty) * 2.1:.0f}, '
              f'duration: 0.55, ease: "expo.inOut"}}, {start + 0.2});')
    tw.append(f'tl.fromTo("#{cid} .hl", {{boxShadow: "0 0 0 0px rgba(245,196,81,0)"}}, '
              f'{{boxShadow: "0 0 0 3px #F5C451, 0 0 40px rgba(245,196,81,0.6)", duration: 0.3}}, {start + 0.6});')


headline("s5a", 15, 1.3, "$500", "For a Successful", "US LLC")
earn_zoom("s5b", 16.3, 1.2, ("u", 2), (666 + 305, 118 + 100 + 64 + 23))
headline("s5c", 17.5, 1.3, "$750", "For a Dubai Company", "Setup")
earn_zoom("s5d", 18.8, 1.2, ("d", 2), (24 + 305, 118 + 100 + 64 + 23))

# 6. Swipes 20-26
SW = [("s6a", 19.9, 2.35, VIEW_MARKETING, "Marketing Tools", "Ready-to-post marketing copy", (904, 190), 1.5),
      ("s6b", 22.0, 2.3, VIEW_FAQ, "Resources", "Clear rules", (300 + 600, 330), 1.18),
      ("s6c", 24.0, 2.7, VIEW_PAYOUTS, "Payouts", "Get paid", (608, 235), 1.75)]
for i, (cid, st, du, view, act, txt, focus, zs) in enumerate(SW):
    clip(cid, st, du, f'<div class="stage3d"><div class="cam" id="{cid}c">{frame(view, act, cid + "d")}</div></div>', track=3 + i % 2)
    tw.append(f'tl.fromTo("#{cid}d", {{rotationY: -65, x: 900, opacity: 0}}, {{rotationY: 0, x: 0, opacity: 1, duration: 0.4, ease: "power3.out"}}, {st});')
    tw.append(f'tl.fromTo("#{cid}c", {js(cam_to(750, 400, 0.98))}, {{...{js(cam_to(focus[0], focus[1], zs))}, duration: 0.6, ease: "power3.inOut"}}, {st + 0.55:.2f});')
    if i < 2:
        tw.append(f'tl.to("#{cid}d", {{rotationY: 65, x: -900, opacity: 0, duration: 0.35, ease: "power3.in"}}, {st + du - 0.35:.2f});')
    line(f"l6{i}", st + 0.2 if i else 20.1, (SW[i + 1][1] if i < 2 else 26.0) - (st + 0.2 if i else 20.1), txt)
tw.append('tl.fromTo("#tabs span", {y: 10, opacity: 0.3}, {y: 0, opacity: 1, duration: 0.2, stagger: 0.07}, 20.9);')
tw.append('tl.fromTo("#s6bd .qa", {x: 30, opacity: 0}, {x: 0, opacity: 1, duration: 0.25, stagger: 0.09}, 22.35);')
tw.append('tl.fromTo("#avail .val", {scale: 0.8}, {scale: 1, duration: 0.4, ease: "back.out(2)"}, 24.9);')

# 7. Wave-mark wipe + end card 26-30
clip("wipe", 25.95, 1.0, '<img class="mark" id="mark2" src="assets/img/mark.png" alt="">', track=8)
tw += ['tl.fromTo("#mark2", {scale: 0.15, rotation: -40, opacity: 0.95}, {scale: 6.5, rotation: 0, duration: 0.6, ease: "power3.in"}, 25.95);',
       'tl.to("#mark2", {opacity: 0, duration: 0.3}, 26.6);']
clip("end", 26.55, 3.45,
     '<img class="wordmark" id="wm2" src="assets/img/wordmark.png" alt="GenZone">'
     '<div class="url" id="url"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#2B63F0" stroke-width="1.6">'
     '<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12h20M4 7h16M4 17h16"/></svg>'
     '<span>www.genzone.com</span></div>'
     '<div class="endline" id="endline">Share your link. Refer your network. Start earning.</div>'
     '<div class="cta" id="cta">Join the referral program</div>', track=7)
tw += ['tl.fromTo("#wm2", {scale: 1.2, opacity: 0}, {scale: 1, opacity: 1, duration: 0.45, ease: "expo.out"}, 26.55);',
       'tl.fromTo("#url", {y: 20, opacity: 0}, {y: 0, opacity: 1, duration: 0.3, ease: "power3.out"}, 26.65);',
       'tl.fromTo("#endline", {y: 20, opacity: 0}, {y: 0, opacity: 1, duration: 0.3, ease: "power3.out"}, 26.75);',
       'tl.fromTo("#cta", {scale: 0.7, opacity: 0}, {scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)"}, 26.85);',
       'tl.to("#cta", {boxShadow: "0 0 50px rgba(62,197,255,0.8)", duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut"}, 27.5);']

CSS = open("style.css").read()
html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
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
"""
open("index.html", "w").write(html)
print(f"wrote index.html: {len(clips)} clips, {len(tw)} tweens")
