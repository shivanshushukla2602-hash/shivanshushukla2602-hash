# Keeping this profile yours

The root README is the public GitHub profile. Its artwork lives in `assets/`.

## Edit content

- Change the introduction, links and project destinations in `README.md`.
- Change the original artwork and copy in `scripts/visuals.py`; `scripts/generate_design.py` writes the static artwork and animation frames.
- Run `python3 -m pip install -r requirements.txt` and `npm install`, then `npm run render` to rebuild the original vectors, animated header and articulated 3D studio. The 3D scene renderer starts its own local preview server. Set `CHROME_PATH` if Chrome is installed somewhere other than its normal macOS location.
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

A black and warm off-white editorial profile. Personal details, project cards, coding-stat numbers, labels, borders and contact artwork use neutral colours. Multiple colours appear in the animated skill details, header ribbons, contribution bars and articulated 3D workstation. The portrait keeps its natural photographic colours.

### Contribution heatmap animation

`assets/activity-v8.gif` and `assets/activity-mobile-v8.gif` are rendered from 72 frames, with identical pause frames merged for a smaller download. They replay the growth of the owner's actual public contribution heights, then return to the beginning. The numerical totals stay fixed. The source dates and counts live in `assets/activity-calendar.json`; the animation never adds fictitious activity. A daily workflow regenerates the GIFs and static reduced-motion versions using `scripts/animate_activity.py` and Pillow.

### Articulated working character

`assets/lab-v8.gif` and `assets/lab-mobile-v8.gif` contain 96 frames of an original Three.js scene, not a still illustration with floating decorations. The seated character has articulated shoulders, elbows, wrists and fingers. He types, sways, nods and turns his head, switches to the mouse, and works with changing monitor content. Keyboard presses, screen progress and a changing activity label are synchronized to the six-second loop.

The scene source is `scripts/studio-scene.mjs`; its surrounding layout is `scripts/studio.html`. The previous generated studio illustration is not used in the profile. `scripts/render_studio.mjs` renders desktop and mobile frames, and `scripts/pack_animations.py` packages them. The portrait remains the owner's existing photograph. Reduced-motion preferences select static artwork for all three animated sections.

## Suggested account settings

The profile README is published automatically by its username-matching repository. Account-level settings require their own GitHub permission. If updating them manually in **Edit profile**, use:

- **Name:** Shivanshu Shukla
- **Bio:** CS @ PW IOI · Java & JavaScript · Frontend + DSA · Learning by building. Open to internships & collaboration.
- **Website:** https://shiv-and-shu-portfolio.vercel.app
- **Location:** Bengaluru, India

For the pinned-repository area below the README, useful choices are My-Portfolio, PyCosmos, SevaRecover, InnovateX, SpendWise-old, and Bus-Reservation-System.

## Kinetic identity header

The selected v9 direction combines off-white Sora typography, a short Fraunces italic line, and a custom iridescent three-dimensional sculpture. It uses no portrait, framed photo card, ribbons drawn under a slogan, or text hidden behind a photograph. `scripts/kinetic-sculpture.mjs` builds the original parametric loop and animates its orientation. `scripts/kinetic-header.html` provides distinct desktop and mobile layouts. `scripts/render_kinetic_header.mjs` renders 120 frames; `scripts/pack_kinetic_header.py` packages the six-second GIF loops and static fallbacks. Three.js's RoomEnvironment helper retains its upstream MIT license in `scripts/Three-LICENSE.txt`.

## Actual coding screenshots

The problem-solving section uses actual GeeksforGeeks and PW IOI BruteForce screenshots captured on 1 November 2026, including statistics, activity heatmaps and solved-question lists. The source URLs and capture status are recorded in `assets/coding-screenshot-sources.json`. These images are dated snapshots; the text statistics below still refresh daily.

LeetCode and Codeforces returned HTTP 403 browser security-verification pages. Their screenshots have not been fabricated or replaced with styled mock-ups. The owner can supply screenshots from a signed-in browser to finish those two entries. Do not replace genuine screenshots with daily generated stats cards.

## Green contribution heatmap

Only the contribution bars use the dark-to-bright green scale, matching the requested activity-heatmap style. The animation still grows from real daily counts and preserves fixed snapshot totals. Both the daily GIF renderer and static SVG fallback use the green palette; the scheduled refresh preserves it.
