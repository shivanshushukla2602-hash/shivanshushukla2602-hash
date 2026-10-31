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

A separate midnight developer-studio identity: cyan, violet and pink signals; monospaced terminal panels; a portrait-led animated header; a connected skill map; a verified contribution orbit; and an original animated isometric robot lab. This design is independent of the portfolio website. Reference-profile artwork and biography are not copied.

## Suggested account settings

The profile README is published automatically by its username-matching repository. Account-level settings require their own GitHub permission. If updating them manually in **Edit profile**, use:

- **Name:** Shivanshu Shukla
- **Bio:** CS @ PW IOI · Java & JavaScript · Frontend + DSA · Learning by building. Open to internships & collaboration.
- **Website:** https://shiv-and-shu-portfolio.vercel.app
- **Location:** Bengaluru, India

For the pinned-repository area below the README, useful choices are My-Portfolio, PyCosmos, SevaRecover, InnovateX, SpendWise-old, and Bus-Reservation-System.
