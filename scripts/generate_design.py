#!/usr/bin/env python3
"""Build original editorial studio vectors and animation frames; render with render_animations.mjs."""
from pathlib import Path
import base64
from visuals import header,about,stack,project,footer,PROJECTS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets';FRAMES=ROOT/'preview/frames-v5';FRAMES.mkdir(parents=True,exist_ok=True)
portrait='data:image/png;base64,'+base64.b64encode((OUT/'portrait.png').read_bytes()).decode()
for mobile in [False,True]:
 suffix='-mobile' if mobile else ''
 for name,fn in [('about',about),('stack',stack),('footer',footer)]: (OUT/f'{name}{suffix}-v5.svg').write_text(fn(mobile))
 for item in PROJECTS:(OUT/f'project-{item[0]}{suffix}-v5.svg').write_text(project(item,mobile))
 for i in range(72):
  t=i/9
  (FRAMES/f'header{suffix}-{i:03}.svg').write_text(header(t,portrait,mobile))

print('Generated editorial artwork and 72-frame desktop/mobile header sequences.')
