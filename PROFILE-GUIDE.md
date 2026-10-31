# Keeping this profile yours

The root README is the public GitHub profile. Its artwork lives in `assets/`.

## Edit content

- Change the introduction, links and project destinations in `README.md`.
- Change the original artwork and copy in `scripts/generate_design.py`.
- Run `python3 -m pip install -r requirements.txt`, then `python3 scripts/generate_design.py` to rebuild the GIF and design cards.
- The GIF is an original code-drawn animation. It has a static fallback for reduced-motion preferences. These graphics do not depend on third-party stats-card services.

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

Pearl type, charcoal surfaces, warm line-work, and an animated signal through a developer workbench. The header, project cards and layout were created for Shivanshu; reference-profile artwork and biography are not copied.
