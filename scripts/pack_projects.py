"""Package browser-rendered project artwork as seamless GitHub-compatible GIFs."""
from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1]
for project in json.loads((root/'scripts/project-data.json').read_text()):
 for suffix in ('','-mobile'):
  name=project['key']+suffix
  images=[Image.open(root/f'preview/projects-v10/{name}-{i:03}.png').convert('RGB') for i in range(48)]
  # One palette per loop avoids frame-to-frame colour flicker.
  palette=images[0].quantize(colors=256,method=Image.Quantize.MEDIANCUT)
  frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
  dest=root/f'assets/project-{name}-v10.gif'
  frames[0].save(dest,save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=1)
  images[0].save(root/f'assets/project-{name}-v10-static.png',optimize=True)
  print(dest.name,round(dest.stat().st_size/1024),'KB')
