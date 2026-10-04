# GenZone Referral Program — premium SaaS spot (#3)

24 s · 16:9 · rendered 3840×2160 at 60 fps · no VO · original score (-14 LUFS / -1 dBTP)

| Time | Scene |
|---|---|
| 0–4.4 | Rebuilt GenZone dashboard rises in 3D with a camera push-in; "Referral Dashboard" nav glows; push into the personal link |
| 3.6–8.1 | The link lifts off and floats forward; a light pulse travels Share → Referral → Client → Sale → Commission. "Share your link. Earn on every sale." |
| 8.0–13.3 | "What you earn": Dubai and US LLC glass cards; every commission counts up with a green glow, row by row; payout timing line |
| 13.2–18.0 | Referral pipeline: a demo referral moves Lead → Call booked → Signed up → Applied → In review → Paid (gold) → Completed (check) |
| 17.8–24 | Final composition: tilted dashboard, link pill, glowing "Commission earned +$500.00" notification, "Share your link. Refer clients. Earn commissions.", GenZone logo + "Join the referral program · genzone.com" |

Notes
- The UI is rebuilt in HTML/CSS from the two dashboard screenshots (reference/) so numbers can animate and text stays sharp at 4K.
- Demo values only: referral code `GENZ-DEMO42`, "Demo client". Commission figures are the real rates.
- Logo: crop from the client storyboard PDF (official files not yet received).
- Fonts: DM Sans (UI, OFL) and Inter (headlines, OFL).
- Build: `cd hf && python3 music.py && python3 build.py && npx hyperframes render . -q high --fps 60 --resolution 4k`
