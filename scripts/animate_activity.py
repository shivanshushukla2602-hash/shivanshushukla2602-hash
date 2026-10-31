"""Daily, self-hosted multicolour heatmap animations from the verified public calendar."""
from pathlib import Path
from datetime import date,timedelta
import math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets'
BG='#0b0b0b';FG='#eee9df';MUTED='#a9a59d';ACCENT=FG;LINE='#30302e'
def font(size,bold=False):return ImageFont.truetype(str(OUT/'fonts'/('manrope-bold.ttf' if bold else 'manrope-regular.ttf')),size)
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def frame(days,data,mobile=False,phase=None):
 w,h=(600,770) if mobile else (1200,600);im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im);d.rounded_rectangle((1,1,w-2,h-2),radius=24,outline=LINE,width=1)
 def txt(x,y,s,size=16,color=FG,bold=False):d.text((x,y),str(s),font=font(size,bold),fill=color,anchor='ls')
 txt(34,45,'A YEAR OF SHOWING UP',12,ACCENT)
 txt(32,98,'Progress, one day at a time.',30 if mobile else 40,FG,True)
 for i,(v,k) in enumerate([(data['public_contributions_365_days'],'contributions'),(data['public_repositories'],'public repositories'),(len(data['original_repository_languages']),'languages in repos')]):
  x=34+i*(190 if mobile else 365);txt(x,167,v,43 if mobile else 53,FG,True);txt(x,195,k,12 if mobile else 16,MUTED)
 start=date.fromisoformat(data['as_of'])-timedelta(days=364);base=start-timedelta(days=(start.weekday()+1)%7)
 ox,oy=(103,330) if mobile else (155,290);sx,sy=(8.2,4.1) if mobile else (17,3.0);maximum=max([v['count'] for v in days.values()]+[1])
 colors=[('#1b2920','#142018','#26372b'),('#17452a','#10351f','#2f7542'),('#20773c','#17592d','#48a455'),('#2b9d46','#207634','#6bd36b'),('#4bb750','#368d3a','#9be788')]
 for ds,item in sorted(days.items()):
  day=date.fromisoformat(ds) if isinstance(ds,str) else ds;week,weekday=divmod((day-base).days,7);x=ox+week*sx-weekday*sx*.78;y=oy+week*sy+weekday*sy*2.2
  growth=1 if phase is None else smooth((phase/.56*1.3-week/53*.36)/.72)*(1-smooth((phase-.88)/.12))
  z=4+(math.log1p(item['count'])/math.log1p(maximum)*85*growth if item['count'] else 0);left,right,top=colors[min(4,item['level'])];a=sx*.78;b=sy*1.8
  if phase is not None and item['count'] and abs(week/53-(phase*1.5)%1)<.025:top='#c4ffc0'
  d.polygon([(x,y-z),(x+a,y+b-z),(x+a,y+b),(x,y)],fill=left);d.polygon([(x,y-z),(x-a,y+b-z),(x-a,y+b),(x,y)],fill=right);d.polygon([(x,y-z),(x+a,y+b-z),(x,y+2*b-z),(x-a,y+b-z)],fill=top)
 d.line((34,h-77,w-34,h-77),fill=LINE)
 txt(34,h-45,'Animated replay of your real contribution history.',14 if mobile else 17,MUTED)
 txt(34,h-20,'Public GitHub activity · '+data['as_of']+' · Totals stay fixed',12,MUTED)
 return im

def render_animations(days,data):
 for mobile in [False,True]:
  suffix='-mobile' if mobile else '';images=[frame(days,data,mobile,i/72) for i in range(72)]
  # Common palette keeps the stationary type and background perfectly stable.
  palette=images[46].quantize(colors=128,method=Image.Quantize.MEDIANCUT)
  frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
  frames[0].save(OUT/f'activity{suffix}-v9.gif',save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=True,disposal=1)
  frame(days,data,mobile).save(OUT/f'activity{suffix}-v9-static.png',optimize=True)
