# Animated project showcase

Six individually linked project reels replace the old two-column text grid. Each pairs a short purpose statement with an actual project screenshot. Alternating desktop layouts create a visual rhythm; mobile assets stack the text above the preview.

The typography stays off-white on black. Colour belongs to the screenshots and moving artwork. Floating browser windows, counter-moving outlines, a rotating asterisk and a small moving label form a seamless 3.84-second loop. Copy remains stationary. Reduced-motion readers receive still PNGs.

## Sources

- `scripts/project-data.json`: project names, context, purpose, stack and repository destinations.
- `scripts/project-showcase.html`: original HTML/CSS artwork and deterministic motion.
- `scripts/render_projects.mjs`: Chrome rendering, 48 frames per project and viewport.
- `scripts/pack_projects.py`: common-palette GIF packaging and still fallbacks.
- `assets/project-previews/`: screenshots of the actual portfolio and project interfaces; these are interface previews, not claims that every project is hosted publicly.

## Regenerate

Install the pinned Node dependencies and Python requirements, then run `npm run render:projects`. Chrome must be installed. The portfolio screenshot is already included; if removed, the renderer captures the portfolio running at `http://127.0.0.1:8080/`.

Only artwork inside the images animates on GitHub. Repository links use normal Markdown/HTML anchors; no unsupported JavaScript or hover behaviour is required in the README.
