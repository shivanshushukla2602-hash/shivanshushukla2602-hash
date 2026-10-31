#!/usr/bin/env python3
"""Package rasterized vector frames into compact animations with static fallbacks."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];FRAMES=ROOT/'preview/rendered-v5';OUT=ROOT/'assets'
for name in ['header','header-mobile','lab','lab-mobile']:
 images=[Image.open(FRAMES/f'{name}-{i:03}.png').convert('RGB') for i in range(96 if name.startswith('lab') else 72)]
 # A shared palette avoids colour flicker and keeps the unchanged portrait compact.
 palette=images[35].quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
 frames[0].save(OUT/f'{name}-v5.gif',save_all=True,append_images=frames[1:],duration=62 if name.startswith('lab') else 110,loop=0,optimize=True,disposal=1)
 images[-1].save(OUT/f'{name}-v5-static.png',optimize=True)
 print(name,(OUT/f'{name}-v5.gif').stat().st_size,'bytes')
