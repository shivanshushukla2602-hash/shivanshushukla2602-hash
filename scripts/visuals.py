"""Original editorial profile artwork: warm neutrals, human language and colour in motion."""
from html import escape as e
from datetime import date,timedelta
import math,textwrap
BG='#0b0b0b';PANEL='#141413';FG='#eee9df';MUTED='#a9a59d';CORAL='#f2a092';MINT='#9dd8bc';YELLOW='#f1d580';LILAC='#c7aff0';SKY='#9bcdf2';LINE='#30302e'
FONT='Arial,Helvetica,sans-serif'
def text(x,y,value,size=16,color=FG,weight='normal',extra=''):
 return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{e(str(value))}</text>'
def rect(x,y,w,h,fill=PANEL,stroke=LINE,rx=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def svg(w,h,title,body):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{e(title)}</title><defs><linearGradient id="coral" x2=".7" y2="1"><stop stop-color="#ffd8cd"/><stop offset="1" stop-color="#c97e7d"/></linearGradient><linearGradient id="sage" x2=".7" y2="1"><stop stop-color="#d4eee2"/><stop offset="1" stop-color="#73ae99"/></linearGradient><linearGradient id="gold" x2=".7" y2="1"><stop stop-color="#faedb9"/><stop offset="1" stop-color="#c8a461"/></linearGradient></defs><style>@media(prefers-reduced-motion:reduce){{.motion{{animation:none!important;display:none}}}}</style>{rect(1,1,w-2,h-2,BG,LINE,24)}{body}</svg>'''
def label(x,y,value,color=MUTED):return text(x,y,value,12,color,extra='letter-spacing="2.2"')
def star(x,y,size,color,rotation=0):
 return f'<g transform="translate({x} {y}) rotate({rotation})">'+''.join(f'<path d="M{-size} 0H{size}" stroke="{color}" stroke-width="{size*.18}" transform="rotate({a})"/>' for a in [0,45,90,135])+'</g>'
def header(t,portrait,mobile=False):
 w,h=(600,760) if mobile else (1200,590);q=t/8*math.tau
 b='<defs><linearGradient id="signature"><stop stop-color="'+CORAL+'"/><stop offset=".35" stop-color="'+LILAC+'"/><stop offset=".7" stop-color="'+SKY+'"/><stop offset="1" stop-color="'+MINT+'"/></linearGradient></defs>'
 b+=label(32,42,'A WORK IN PROGRESS',MUTED)+text(w-32,42,'BENGALURU, INDIA',11,MUTED,extra='text-anchor="end" letter-spacing="1.5"')
 if mobile:
  b+=text(30,123,'Shivanshu',64,FG,'bold',extra='letter-spacing="-2.6"')+text(30,191,'Shukla.',64,FG,'bold',extra='letter-spacing="-2.6"')
  px,py,pw,ph=34,245,210,254
  b+=text(281,282,'A curious',30,FG,'bold',extra='letter-spacing="-.8"')+text(281,318,'mind.',30,FG,'bold',extra='letter-spacing="-.8"')
  b+=text(281,372,'A maker’s',30,FG,'bold',extra='letter-spacing="-.8"')+text(281,408,'instinct.',30,FG,'bold',extra='letter-spacing="-.8"')
  b+=label(282,458,'CS @ PW IOI',MUTED)+text(282,486,'Learning by doing.',16,MUTED)
 else:
  px,py,pw,ph=52,104,302,320
  b+=text(431,147,'A curious mind.',51,FG,'bold',extra='letter-spacing="-2"')+text(431,207,'A maker’s instinct.',51,FG,'bold',extra='letter-spacing="-2"')
  b+=text(434,261,'Small ideas. Thoughtful work.',22,MUTED)
  b+=text(434,302,'CS @ PW IOI',13,MUTED,extra='letter-spacing="1.4"')+text(625,302,'JAVA · JAVASCRIPT · DSA',13,MUTED,extra='letter-spacing="1.2"')
 # A rectangular portrait print, registered to an asymmetric colour-block backing.
 lift=math.sin(q)*3;angle=math.sin(q)*.8
 b+=f'<g transform="translate(0 {lift:.2f}) rotate({angle:.2f} {px+pw/2} {py+ph/2})">'
 b+=f'<path d="M{px-10} {py+24}V{py-9}H{px+pw-24}L{px+pw+14} {py+29}V{py+ph+10}H{px-10}Z" fill="#242422"/>'
 b+=f'<path d="M{px+pw-26} {py-9}V{py+29}H{px+pw+14}Z" fill="{FG}"/>'
 b+=f'<defs><clipPath id="portrait"><rect x="{px}" y="{py+3}" width="{pw}" height="{ph}" rx="7"/></clipPath></defs>'
 b+=f'<image href="{portrait}" x="{px}" y="{py+3}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#portrait)"/>'
 for i,col in enumerate([CORAL,YELLOW,MINT,SKY]):b+=f'<rect x="{px+12+i*19}" y="{py+ph-12}" width="13" height="4" rx="2" fill="{col}"/>'
 b+='</g>'
 # Four independent ribbons form an original moving signature, away from the photograph and copy.
 x0,x1,y0=(32,568,606) if mobile else (434,1140,362)
 for i,col in enumerate([CORAL,LILAC,SKY,MINT]):
  yy=y0+i*14;wave=math.sin(q+i*.65)*19;wave2=math.cos(q+i*.65)*19
  path=f'M{x0} {yy}C{x0+(x1-x0)*.24} {yy-wave*2},{x0+(x1-x0)*.32} {yy+wave2*2},{(x0+x1)/2} {yy}S{x1-(x1-x0)*.15} {yy-wave*2},{x1} {yy}'
  b+=f'<path d="{path}" stroke="{col}" stroke-width="{5 if mobile else 6}" fill="none" stroke-linecap="round" opacity=".9"/>'
 if mobile:
  b+=text(300,558,'Small ideas. Thoughtful work.',23,FG,'bold',extra='text-anchor="middle" letter-spacing="-.5"')
  b+=text(300,704,'JAVA · JAVASCRIPT · DSA',15,MUTED,extra='text-anchor="middle" letter-spacing="1.5"')+text(300,740,'Open to internships & collaboration ↗',14,MUTED,extra='text-anchor="middle"')
 else:
  b+=f'<path d="M34 459H1166" stroke="{LINE}"/>'
  b+=text(50,535,'SHIVANSHU SHUKLA',80,FG,'bold',extra='textLength="1096" lengthAdjust="spacingAndGlyphs"')
  b+=label(34,569,'LEARNING BY DOING',MUTED)+text(1166,569,'Open to internships & collaboration ↗',13,MUTED,extra='text-anchor="end"')
 return svg(w,h,'Shivanshu Shukla. A curious mind, a maker’s instinct. An original editorial identity with an offset portrait print, fully readable name and four animated colour ribbons. CS at PW IOI, Java, JavaScript and DSA.',b)
def about(mobile=False):
 w,h=(600,515) if mobile else (1200,305)
 b=label(34,44,'THE PERSON BEHIND THE PROJECTS',MUTED)
 lines=['A curious mind.','A hands-on learner.']
 for i,line in enumerate(lines):b+=text(32,108+i*50,line,40 if mobile else 42,FG,'bold',extra='letter-spacing="-1.8"')
 if mobile:
  b+=text(34,226,'Studying computer science at PW IOI.',21,MUTED)+text(34,258,'Learning by making, testing, and trying again.',21,MUTED)
  for i,(a,v,c) in enumerate([('BASED IN','Bengaluru, India',MUTED),('CURRENT FOCUS','Java, JavaScript & DSA',MUTED),('OPEN TO','Internships & collaboration',MUTED)]):
   y=323+i*64;b+=label(34,y,a,c)+text(34,y+28,v,23,FG)
 else:
  b+=text(34,220,'Studying computer science at PW IOI.',20,MUTED)+text(34,251,'Learning by making, testing, and trying again.',20,MUTED)
  for i,(a,v,c) in enumerate([('BASED IN','Bengaluru, India',MUTED),('CURRENT FOCUS','Java, JavaScript & DSA',MUTED),('OPEN TO','Internships & collaboration',MUTED)]):
   y=80+i*79;b+=f'<circle cx="688" cy="{y-4}" r="4" fill="{c}"/>'+label(710,y-3,a)+text(710,y+29,v,25,FG)
 return svg(w,h,'About Shivanshu: a curious, hands-on computer science student at PW IOI in Bengaluru. Focused on Java, JavaScript and DSA. Open to internships and collaboration.',b)
def icon(kind,x,y,color,scale=1):
 paths={'java':'M-13 4H10V12Q10 22-2 22Q-13 22-13 12ZM10 6H15Q24 6 20 14H11M-17 27H17M-7-16Q4-24 1-9Q-4-4 2 0M6-18Q18-24 11-7', 'js':'M-18-19H20V20H-18ZM-4-3V10Q-4 16-11 12M14-1Q3-7 5 2Q6 6 12 7Q20 13 7 15', 'web':'M-20-16H20V17H-20ZM-20-7H20M-5 0L-12 5L-5 10M5 0L12 5L5 10', 'react':'M-21 0Q0-18 21 0Q0 18-21 0ZM-10-18Q16-9 10 18Q-16 9-10-18ZM10-18Q-16-9-10 18Q16 9 10-18','leaf':'M-18 17Q-23-18 19-20Q24 17-18 17ZM-16 15L11-11','git':'M0-23L23 0L0 23L-23 0ZM-10-10L8 8M-2-2V13','dsa':'M-18-18H-5V-5H-18ZM7-18H20V-5H7ZM-5 8H8V21H-5ZM-11-5V2H14V-5M1 2V8','python':'M-18-2V-13Q-18-22-7-22H6Q14-22 14-13V1H-8V12H-21Q-28 12-28 1Q-28-9-18-9M18 2V13Q18 22 7 22H-6Q-14 22-14 13V-1H8V-12H21Q28-12 28-1Q28 9 18 9'}
 return f'<g transform="translate({x} {y}) scale({scale})"><path d="{paths.get(kind,paths["web"])}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>'
def stack(mobile=False):
 w,h=(600,800) if mobile else (1200,470);b=label(34,43,'WHAT I WORK WITH',FG)
 groups=[('LANGUAGES',[('java','Java',CORAL),('js','JavaScript',YELLOW),('python','Python basics',MINT)]),('BUILDING INTERFACES',[('web','HTML & CSS',CORAL),('react','React',MINT),('web','Responsive UI',LILAC)]),('JAVA & TOOLS',[('leaf','Spring Boot',MINT),('git','Hibernate / ORM',YELLOW),('git','Maven · Git',CORAL)])]
 for row,(name,items) in enumerate(groups):
  yy=(90+row*205) if mobile else (92+row*116);b+=label(34,yy,name)
  for col,(kind,value,color) in enumerate(items):
   x=(92+col*193) if mobile else (370+col*285);y=yy+60 if mobile else yy-3
   b+=icon(kind,x,y,color,.75)
   b+=text(x,y+48,value,18,FG,extra='text-anchor="middle"') if mobile else text(x+38,y+7,value,22,FG)
 b+=f'<g class="motion"><circle r="3" fill="{CORAL}"><animateMotion dur="7s" repeatCount="indefinite" path="M34 {h-104}H{w-34}"/></circle></g>'
 b+=f'<path d="M34 {h-104}H{w-34}" stroke="{LINE}"/>'+label(34,h-70,'ALSO EXPLORING',MUTED)
 b+=text(34,h-37,'Servlets · WebAssembly · Pyodide',19 if mobile else 20,FG)
 if not mobile:b+=text(w-34,h-37,'Next: React depth · Node.js · System design',18,MUTED,extra='text-anchor="end"')
 return svg(w,h,'Skills: Java, JavaScript, Python foundations; HTML, CSS and React; Spring Boot, Hibernate, ORM, Maven, Git, Servlets; WebAssembly and Pyodide.',b)
PROJECTS=[('portfolio','PERSONAL PORTFOLIO','Shivanshu Shukla','A place for my work and learning journey.','HTML · CSS · JAVASCRIPT',CORAL),('pycosmos','PERSONAL PLATFORM','PyCosmos','Making Python practice possible in a browser.','REACT · JAVASCRIPT · PYODIDE',MINT),('sevarecover','AMAZON BUILDATHON','SevaRecover','Helping people understand rejected applications.','REACT · TYPESCRIPT · PYTHON',YELLOW),('innovatex','END-SEMESTER PROJECT','InnovateX','Bringing our team and its work together.','HTML · CSS · JAVASCRIPT',LILAC),('spendwise','END-SEMESTER PROJECT','SpendWise','Exploring simpler everyday money interfaces.','HTML · CSS · FINANCE UI',CORAL),('bus','END-SEMESTER PROJECT','Bus Reservation','Connecting seat booking, records and a database.','EXPRESS · SQLITE · JAVASCRIPT',MINT)]
def project(item,mobile=False):
 slug,kicker,name,desc,tech,color=item;color=FG;w,h=(300,300) if mobile else (490,245)
 b=f'<rect x="1" y="28" width="4" height="54" rx="2" fill="{color}"/>'+label(23,37,kicker,color)+text(w-24,38,'↗',25,color,extra='text-anchor="end"')
 # A small visual signature, not a terminal window.
 b+=f'<circle cx="{w-45}" cy="{h-48}" r="28" fill="{color}" opacity=".1"/>'
 for i,line in enumerate(textwrap.wrap(name,18 if mobile else 25)):b+=text(22,91+i*34,line,30 if mobile else 34,color,'bold',extra='letter-spacing="-1.2"')
 y=169 if mobile else 142
 for i,line in enumerate(textwrap.wrap(desc,27 if mobile else 45)):b+=text(23,y+i*23,line,16,MUTED)
 b+=text(23,h-26,tech,10,color,extra='letter-spacing=".5"')
 return svg(w,h,name+': '+desc+' '+kicker+'. '+tech,b)
def coding_card(key,data,mobile=False):
 names={'leetcode':('LeetCode','Shivanshu_19',YELLOW),'codeforces':('Codeforces','shivanshu_19',SKY),'gfg':('GeeksforGeeks','shivanshu19',MINT),'bruteforce':('PW IOI BruteForce','shivanshu_19',CORAL)}
 name,handle,color=names[key];color=FG;w,h=(300,280) if mobile else (490,252);value=data.get('solved','—')
 b=text(22,38,name,21 if mobile else 25,FG,'bold',extra='letter-spacing="-.7"')+text(22,65,'@'+handle,13,MUTED)
 b+=text(18,143,value,79,color,'bold',extra='letter-spacing="-4"')+text(22,171,'unique accepted problems' if key=='codeforces' else 'problems solved',16,MUTED)
 details=data.get('breakdown')
 if details:
  start=22;total=max(1,sum(details.values()))
  for (k,v),c in zip(details.items(),[FG,'#c4beb5','#77736e']):
   width=(w-44)*v/total;b+=f'<rect x="{start:.2f}" y="190" width="{width:.2f}" height="4" rx="2" fill="{c}"/>';start+=width
  b+=text(22,218,' · '.join(k.title()+' '+str(v) for k,v in details.items()),11 if mobile else 14,FG)
 elif 'score' in data:b+=text(22,212,'Coding score  '+str(data['score']),16,FG)
 else:b+=text(22,212,'Data structures & algorithms',12 if mobile else 15,FG)
 b+=text(22,h-13,'Verified '+data.get('as_of','—'),10,MUTED)+text(w-22,h-14,'↗',19,color,extra='text-anchor="end"')
 return svg(w,h,name+': '+str(value)+' solved, publicly verified '+data.get('as_of','not yet available'),b)
def activity(days,data,mobile=False):
 w,h=(600,770) if mobile else (1200,600);b=label(34,45,'A YEAR OF SHOWING UP',MUTED)+text(32,98,'Progress, one day at a time.',30 if mobile else 40,FG,'bold',extra='letter-spacing="-1.5"')
 for i,(v,k) in enumerate([(data['public_contributions_365_days'],'contributions'),(data['public_repositories'],'public repositories'),(len(data['original_repository_languages']),'languages in repos')]):
  x=34+i*(190 if mobile else 365);b+=text(x,167,v,43 if mobile else 53,FG,'bold',extra='letter-spacing="-2"')+text(x,195,k,12 if mobile else 16,MUTED)
 # Isometric garden: each tile represents a real public day, height follows its count.
 start=date.fromisoformat(data['as_of'])-timedelta(days=364);base=start-timedelta(days=(start.weekday()+1)%7)
 originx,originy=(103,330) if mobile else (155,290);sx,sy=(8.2,4.1) if mobile else (17,3.0)
 maxcount=max([v['count'] for v in days.values()]+[1]);palette=[('#1b2920','#142018','#26372b'),('#17452a','#10351f','#2f7542'),('#20773c','#17592d','#48a455'),('#2b9d46','#207634','#6bd36b'),('#4bb750','#368d3a','#9be788')]
 for d,item in sorted(days.items()):
  if isinstance(d,str):d=date.fromisoformat(d)
  week,weekday=divmod((d-base).days,7);x=originx+week*sx-weekday*sx*.78;y=originy+week*sy+weekday*sy*2.2
  z=4+(min(1,math.log1p(item['count'])/math.log1p(maxcount))*70 if item['count'] else 0);left,right,top=palette[min(4,item['level'])];a=sx*.78;bb=sy*1.8
  b+=f'<g><title>{d.isoformat()}: {item["count"]} public contributions</title><path d="M{x:.1f} {y-z:.1f}l{a:.1f} {bb:.1f}v{z:.1f}l{-a:.1f} {-bb:.1f}Z" fill="{left}"/><path d="M{x:.1f} {y-z:.1f}l{-a:.1f} {bb:.1f}v{z:.1f}l{a:.1f} {-bb:.1f}Z" fill="{right}"/><path d="M{x:.1f} {y-z:.1f}l{a:.1f} {bb:.1f}l{-a:.1f} {bb:.1f}l{-a:.1f} {-bb:.1f}Z" fill="{top}"/></g>'
 b+=f'<path d="M34 {h-77}H{w-34}" stroke="{LINE}"/>'+text(34,h-45,'Each tile is a day. Every height comes from real activity.',14 if mobile else 17,MUTED)+text(34,h-20,'Public GitHub activity · '+data['as_of'],12,MUTED)
 return svg(w,h,'An isometric contribution garden made from '+str(data['public_contributions_365_days'])+' real public GitHub contributions over 365 days.',b)
def footer(mobile=False):
 w,h=(600,260) if mobile else (1200,235);b=label(34,43,'GOOD CONVERSATIONS WELCOME',FG)+text(32,112,'Let’s make something',38 if mobile else 57,FG,'bold',extra='letter-spacing="-2"')+text(32,162,'worth making.',38 if mobile else 57,FG,'bold',extra='letter-spacing="-2"')+text(34,h-29,'shivanshushukla2602@gmail.com',18,MUTED)+text(w-36,h-28,'↗',32,FG,extra='text-anchor="end"')
 return svg(w,h,'Contact Shivanshu Shukla for internships and collaboration: shivanshushukla2602@gmail.com.',b)
