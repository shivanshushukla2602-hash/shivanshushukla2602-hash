"""Clearly labelled charts from official public statistics; never native screenshots."""
from html import escape
import math
BG='#101113';FG='#eee9df';MUTED='#9d9fa5';LINE='#303238';GREEN='#8ed18d';YELLOW='#ffc15b';RED='#ff725e'
def txt(x,y,value,size=16,color=FG,bold=False,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" {extra}>{escape(str(value))}</text>'
def shell(title,body,as_of):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><rect x="1" y="1" width="638" height="358" rx="22" fill="{BG}" stroke="{LINE}"/><rect x="438" y="20" width="176" height="24" rx="12" fill="#202226"/>'+txt(526,36,'VERIFIED-DATA CHART',10,MUTED,extra='text-anchor="middle" letter-spacing=".6"')+body+f'<path d="M26 316H614" stroke="{LINE}"/>'+txt(26,341,'Official public data · '+as_of,12,MUTED)+txt(612,342,'↗',22,FG,extra='text-anchor="end"')+'</svg>'
def leetcode(data):
 total=data.get('solved');counts=data.get('breakdown',{});date=data.get('as_of','Not available')
 b=txt(26,39,'LeetCode',26,FG,True)+txt(27,66,'Shivanshu_19 · Problems overview',14,MUTED)
 if total is None or not counts:return shell('LeetCode verified data unavailable',b+txt(26,185,'Public statistics are currently unavailable.',20,MUTED),date)
 if sum(counts.values())!=total:raise ValueError('LeetCode difficulty counts do not match solved total')
 cx,cy,r=168,192,82;circ=2*math.pi*r
 b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#292d31" stroke-width="17"/>'
 start=0
 for name,color in [('easy',GREEN),('medium',YELLOW),('hard',RED)]:
  n=counts.get(name,0);length=circ*n/max(total,1)
  if n:b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="17" stroke-dasharray="{max(0,length-2):.3f} {circ:.3f}" stroke-dashoffset="{-start:.3f}" transform="rotate(-90 {cx} {cy})"/>'
  start+=length
 b+=txt(cx,193,total,54,FG,True,extra='text-anchor="middle" letter-spacing="-2"')+txt(cx,222,'problems solved',14,MUTED,extra='text-anchor="middle"')
 for i,(name,color) in enumerate([('easy',GREEN),('medium',YELLOW),('hard',RED)]):
  y=145+i*52;b+=f'<rect x="336" y="{y-13}" width="11" height="11" rx="3" fill="{color}"/>'+txt(363,y,name.title(),21,FG)+txt(594,y,counts.get(name,0),24,color,True,extra='text-anchor="end"')
 return shell('LeetCode verified-data chart: '+str(total)+' solved; '+', '.join(f'{counts.get(k,0)} {k}' for k in ['easy','medium','hard']),b,date)
def codeforces(data):
 total=data.get('solved');distribution=data.get('rating_distribution',{});date=data.get('as_of','Not available')
 b=txt(26,39,'Codeforces',26,FG,True)+txt(27,66,'shivanshu_19',14,MUTED)
 b+=txt(606,99,total if total is not None else '—',46,FG,True,extra='text-anchor="end" letter-spacing="-2"')+txt(606,120,'unique accepted problems',12,MUTED,extra='text-anchor="end"')
 b+=txt(27,107,'Solved problems by rating',19,FG,True)
 if not distribution:return shell('Codeforces verified data: rating breakdown unavailable',b+txt(27,188,'Rating breakdown currently unavailable.',17,MUTED),date)
 if sum(distribution.values())!=total:raise ValueError('Codeforces rating counts do not match unique solved total')
 # Fixed rating bands remain readable if the owner later solves a wider range.
 bands=[('Under 1000',0),('1000–1199',0),('1200–1399',0),('1400–1599',0),('1600+',0),('Unrated',0)]
 if len(distribution)<=4:items=sorted(distribution.items(),key=lambda kv:float('inf') if kv[0]=='unrated' else int(kv[0]));items=[('Unrated' if k=='unrated' else k,v) for k,v in items]
 else:
  values=[0]*6
  for k,v in distribution.items():
   index=5 if k=='unrated' else (0 if int(k)<1000 else 1 if int(k)<1200 else 2 if int(k)<1400 else 3 if int(k)<1600 else 4);values[index]+=v
  items=[(bands[i][0],v) for i,v in enumerate(values) if v]
 step=min(64,112/max(1,len(items)-1));start=167 if len(items)<=2 else 150
 for i,(rating,n) in enumerate(items):
  y=start+i*step;color=['#8ed18d','#51aa69','#2c824e','#9add9d','#6cbd7e','#3d915b'][i]
  b+=txt(27,y+3,rating,17,FG)
  b+=f'<rect x="140" y="{y-14}" width="394" height="18" rx="9" fill="#242b26"/><rect x="140" y="{y-14}" width="{394*n/max(total,1):.2f}" height="18" rx="9" fill="{color}"/>'
  b+=txt(602,y+3,n,20,color,True,extra='text-anchor="end"')
 b+=txt(27,292,'Share of unique solves · '+str(data.get('submissions','—'))+' total submissions',13,MUTED)
 return shell('Codeforces verified-data chart: '+str(total)+' unique solved; '+', '.join(k+': '+str(v) for k,v in items),b,date)
def render(key,data):
 return leetcode(data) if key=='leetcode' else codeforces(data)

def overview(cache,mobile=False):
 """Four separate platform totals in one responsive, neutral summary."""
 w,h=(600,420) if mobile else (1000,252)
 body=f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="#0b0b0b" stroke="#30302e"/>'
 body+=txt(28,38,'PROBLEMS SOLVED',12,FG,extra='letter-spacing="2"')
 entries=[('leetcode','LeetCode'),('codeforces','Codeforces'),('gfg','GeeksforGeeks'),('bruteforce','BruteForce')]
 for i,(key,name) in enumerate(entries):
  data=cache.get(key,{});value=data.get('solved','—');as_of=data.get('as_of','Not verified')
  if mobile:x=30+(i%2)*286;y=121+(i//2)*151
  else:x=30+i*246;y=126
  body+=txt(x,y,value,55 if mobile else 62,FG,True,extra='letter-spacing="-2"')+txt(x,y+34,name,19 if mobile else 18,FG)+txt(x,y+58,'Verified '+as_of,11,MUTED)
  if not mobile and i<3:body+=f'<path d="M{x+218} 73V184" stroke="#30302e"/>'
 if mobile:body+='<path d="M300 73V343M28 216H572" stroke="#30302e"/>'
 body+=f'<path d="M28 {h-46}H{w-28}" stroke="#30302e"/>'+txt(28,h-20,'Separate platform totals · refreshed daily',12,MUTED)
 names=', '.join(name+': '+str(cache.get(key,{}).get('solved','unavailable')) for key,name in entries)
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape("Solved-problem overview — "+names)}</title>'+body+'</svg>'
