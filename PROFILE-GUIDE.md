# Keeping this profile yours

The root README is the public GitHub profile. Its artwork lives in `assets/`.

## Edit content

- Change the introduction, links and project destinations in `README.md`.
- Change the original artwork and copy in `scripts/visuals.py`; `scripts/generate_design.py` writes the static artwork and animation frames.
- Run `python3 -m pip install -r requirements.txt` and `npm install`, then `npm run render` to rebuild the original vectors, animated header and isometric lab. Set `CHROME_PATH` if Chrome is installed somewhere other than its normal macOS location.
- The GIFs are original vector-rendered animations. Each has a static fallback for reduced-motion preferences. These graphics do not depend on third-party stats-card services.

## Refresh public statistics

`Refresh public profile cards` runs once a day, or manually from the Actions tab.

- `scripts/update_activity.py` uses public GitHub repository data and the unauthenticated public contribution calendar. It never requests private contribution data.
- `scripts/update_coding.py` uses the supplied coding handles and accessible official public sources. Missing metrics remain absent; they are not presented as zero.
- `assets/activity-data.json` and `assets/coding-data.json` record the sources behind the cards.
- Generated GitHub language counts describe public repositories; they do not claim proficiency.

## Add achievements or solved totals

Only add verified numbers. Keep a dated source link or a screenshot for any manually supplied result. Never commit login cookies, passwords, API tokens, or account recovery details.

The four coding destinations are LeetCode `Shivanshu_19`, Codeforces `shivanshu_19`, GeeksforGeeks `shivanshu19`, and PW IOI BruteForce `shivanshu_19`.

## Design direction

Warm charcoal and ivory, with coral, sage, butter-yellow and a little muted lilac. Bold sans-serif type, a portrait capsule, short personal copy, open icon rows, simple project cards, and a contribution garden based on real activity. The animations are gentle accents around readable content. There are no terminal windows, command headings, code snippets, or neon blue panels.

The portrait is the owner's existing photograph. The studio illustration is original generated artwork, not a photograph of the owner's workspace; it lives at `assets/studio-illustration-v3.png`. Header and studio animations have dedicated mobile layouts and static reduced-motion fallbacks.

Illustration generation used the built-in image-generation tool via the [imagegen skill](/Users/shivanshushukla/.codex/skills/.system/imagegen/SKILL.md). Final prompt:

> Use case: stylized-concept. Asset type: a wide premium editorial illustration for Shivanshu Shukla's professional GitHub README. Create an original beautifully crafted isometric miniature developer studio on a warm almost-black charcoal background (#171614), not blue. A single young adult stylized designer figure with dark hair, charcoal sweatshirt, at a sculptural walnut desk with a cream ultrawide display, compact keyboard, small leafy plant, and neat books. Monitor shows abstract colorful design shapes, no code or text. Warm tactile matte clay, brushed aluminum and walnut materials, elegant soft studio light, subtly colorful coral / sage green / butter yellow objects. Sophisticated designer collectible diorama, crisp high-detail 3D render, generous negative space on the left for later typography, scene on the right two-thirds, wide landscape 3:2. No neon, no sci-fi, no robots, no terminal, no letters or logos or watermark. Calm, human, professional and art-directed; reference is the general idea of a miniature desk scene, not a replica of anyone else's artwork.

## Suggested account settings

The profile README is published automatically by its username-matching repository. Account-level settings require their own GitHub permission. If updating them manually in **Edit profile**, use:

- **Name:** Shivanshu Shukla
- **Bio:** CS @ PW IOI · Java & JavaScript · Frontend + DSA · Learning by building. Open to internships & collaboration.
- **Website:** https://shiv-and-shu-portfolio.vercel.app
- **Location:** Bengaluru, India

For the pinned-repository area below the README, useful choices are My-Portfolio, PyCosmos, SevaRecover, InnovateX, SpendWise-old, and Bus-Reservation-System.
