"""Package the selected kinetic identity without touching the existing studio animation."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];frames_dir=ROOT/'preview/rendered-v9';out=ROOT/'assets'
for name in ['header','header-mobile']:
 images=[Image.open(frames_dir/f'{name}-{i:03}.png').convert('RGB') for i in range(120)]
 palette=images[22].quantize(colors=192,method=Image.Quantize.MEDIANCUT)
 frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
 frames[0].save(out/f'{name}-v9.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,optimize=True,disposal=1)
 images[0].save(out/f'{name}-v9-static.png',optimize=True)
 print(name,(out/f'{name}-v9.gif').stat().st_size,'bytes')
