#!/usr/bin/env python3
"""Build original editorial studio vectors and animation frames; render with render_animations.mjs."""
from pathlib import Path
import base64
from visuals import header,about,stack,project,footer,lab,PROJECTS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets';FRAMES=ROOT/'preview/frames-v3';FRAMES.mkdir(parents=True,exist_ok=True)
art='data:image/png;base64,'+base64.b64encode((OUT/'studio-illustration-v3.png').read_bytes()).decode()
portrait='data:image/png;base64,'+base64.b64encode((OUT/'portrait.png').read_bytes()).decode()
for mobile in [False,True]:
 suffix='-mobile' if mobile else ''
 for name,fn in [('about',about),('stack',stack),('footer',footer)]: (OUT/f'{name}{suffix}-v3.svg').write_text(fn(mobile))
 for item in PROJECTS:(OUT/f'project-{item[0]}{suffix}-v3.svg').write_text(project(item,mobile))
 for i in range(72):
  t=i/9
  (FRAMES/f'header{suffix}-{i:03}.svg').write_text(header(t,portrait,mobile))
  (FRAMES/f'lab{suffix}-{i:03}.svg').write_text(lab(t,mobile,art))
print('Generated editorial artwork and 72-frame desktop/mobile header and lab sequences.')
