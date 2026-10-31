"""Original neon developer-studio graphics; standard-library SVG generation."""
from html import escape as e
from datetime import date,timedelta
import math,textwrap
BG='#070c1b';PANEL='#101a33';FG='#e7f2ff';MUTED='#9eafd0';CYAN='#59eaff';PURPLE='#b18cff';PINK='#ff79ac'
FONT='ui-monospace,SFMono-Regular,Consolas,monospace'
def text(x,y,value,size=16,color=FG,weight='normal',extra=''):
 return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{e(str(value))}</text>'
def rect(x,y,w,h,fill=PANEL,stroke='#293c60',rx=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def svg(w,h,title,body):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{e(title)}</title><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#111333"/><stop offset="1" stop-color="#050c19"/></linearGradient><linearGradient id="neon"><stop stop-color="{CYAN}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient><linearGradient id="panel" x2="1" y2="1"><stop stop-color="#24345d"/><stop offset="1" stop-color="#10172e"/></linearGradient><linearGradient id="metal" x2="0" y2="1"><stop stop-color="#d4e7ff"/><stop offset="1" stop-color="#6a86b6"/></linearGradient><radialGradient id="aura"><stop stop-color="{PURPLE}" stop-opacity=".18"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter></defs><style>@media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}</style>{rect(1,1,w-2,h-2,'url(#bg)','#304362',20)}{body}</svg>'''
def chrome(w,label):
 return ''.join(f'<circle cx="{28+i*17}" cy="27" r="4.5" fill="{c}"/>' for i,c in enumerate([PINK,'#ffd37b',CYAN]))+text(96,32,label,11,MUTED)+f'<path d="M18 49H{w-18}" stroke="#283451"/>'
def stars(w,h):
 return ''.join(f'<circle cx="{40+(i*137)%(w-80)}" cy="{62+(i*83)%(h-100)}" r="{1 if i%3 else 1.8}" fill="{CYAN if i%2 else PURPLE}" opacity="{.12+(i%4)*.07}"/>' for i in range(36))
def header(t,portrait,mobile=False):
 w,h=(600,660) if mobile else (1200,510);b=stars(w,h)+chrome(w,'shivanshu@github:~ / developer-space')
 if mobile:
  b+=text(30,96,'HELLO, WORLD_',18,CYAN)+text(28,145,'Shivanshu Shukla',32,FG,'bold')+text(30,185,'Java. JavaScript. Curiosity.',17,PURPLE)
  px,py,pw,ph=365,183,209,205;terminal=(28,320,544,279)
 else:
  b+=text(42,105,'// CODE, CURIOSITY &amp; ONE MORE IDEA'.replace('&amp;','&'),14,CYAN)+text(40,163,'Shivanshu Shukla',45,FG,'bold')+text(42,202,'Turning curiosity into working code.',20,PURPLE)
  px,py,pw,ph=818,94,335,370;terminal=(42,241,703,208)
 b+=f'<ellipse cx="{px+pw/2}" cy="{py+ph/2}" rx="{pw*.8}" ry="{ph*.75}" fill="url(#aura)"/>'
 b+=f'<path d="M{px+pw*.14} {py+ph*.1}L{px+pw*.86} {py+ph*.1}L{px+pw} {py+ph*.3}V{py+ph*.77}L{px+pw*.77} {py+ph*.98}H{px+pw*.08}L{px} {py+ph*.8}V{py+ph*.26}Z" fill="#152342" stroke="url(#neon)" stroke-width="2"/>'
 b+=f'<defs><clipPath id="portrait"><rect x="{px+4}" y="{py+4}" width="{pw-8}" height="{ph-8}" rx="30"/></clipPath></defs><image href="{portrait}" x="{px-15}" y="{py-3}" width="{pw+30}" height="{ph+24}" preserveAspectRatio="xMidYMin meet" clip-path="url(#portrait)"/>'
 b+=f'<path d="M{px-8} {py+ph*.7}V{py+ph+6}H{px+pw*.3}M{px+pw*.7} {py-8}H{px+pw+8}V{py+ph*.24}" fill="none" stroke="{CYAN}" stroke-width="2"/>'
 b+=text(px+18,py+ph+27,'BENGALURU // INDIA',10,CYAN)
 x,y,tw,th=terminal;b+=rect(x,y,tw,th,'#081223','#344367',13)
 b+=text(x+18,y+29,'~/profile  $  whoami',13,CYAN)+f'<path d="M{x+15} {y+43}H{x+tw-15}" stroke="#263452"/>'
 lines=[('CS student @ PW IOI',FG),('Building with Java + JavaScript',PURPLE),('Practising data structures & algorithms',CYAN),('Open to internships + collaboration',PINK)]
 for i,(value,color) in enumerate(lines):
  progress=max(0,min(1,(t-i*.7)/.8));shown=value[:int(len(value)*progress)]
  b+=text(x+18,y+72+i*28,('> ' if progress else '')+shown,12 if mobile else 14,color)
  if 0<progress<1:b+=text(x+25+len(shown)*(7.2 if mobile else 8.4),y+72+i*28,'▌',14,color)
 if t>3.1:b+=text(x+18,y+th-15,'[ READY TO LEARN. READY TO BUILD. ]',10,'#82f5bd')
 if mobile:b+=text(30,250,'$ learn()',18,CYAN)+text(30,279,'$ build()',18,PINK)+text(30,631,'JAVA  /  WEB  /  DSA  /  CREATIVE CODE',12,MUTED)
 else:b+=text(42,484,'JAVA / WEB / DSA',11,MUTED)+text(745,484,'KEEP THE CURIOSITY. SHIP THE IDEA.',11,PURPLE)
 # The terminal refreshes as a quiet decorative signal travels the frame.
 q=(t%8)/8;b+=f'<circle cx="{25+q*(w-50):.2f}" cy="{h-12}" r="3" fill="{CYAN}"/>'
 return svg(w,h,'Shivanshu Shukla — a Java and JavaScript developer, CS student, and DSA learner in Bengaluru.',b)
def about(mobile=False):
 w,h=(600,590) if mobile else (1200,340);b=chrome(w,'profile.config / identity')
 rows=[('name','Shivanshu Shukla'),('education','CS @ PW IOI / 2025–2029'),('location','Bengaluru, India'),('focus','Java + JavaScript + DSA'),('looking_for','Internships & collaboration')]
 b+=text(30,90,'const developer = {',18,PURPLE)
 for i,(key,value) in enumerate(rows):
  y=125+i*(74 if mobile else 34)
  if mobile:b+=text(44,y,key+':',15,CYAN)+text(62,y+29,'"'+value+'",',17,FG)
  else:b+=text(46,y,key+':',16,CYAN)+text(240,y,'"'+value+'",',16,FG)
 b+=text(30,535 if mobile else 301,'}; // always a work in progress',16,PINK)
 if not mobile:
  b+=f'<path d="M810 98V284" stroke="#344367"/>'
  for i,(v,c) in enumerate([('LEARN',CYAN),('BUILD',PURPLE),('REFINE',PINK)]):
   y=128+i*63;b+=rect(854,y-24,270,44,'#111e38',c,8)+text(876,y+3,v,18,c)
   if i<2:b+=f'<path d="M990 {y+20}v19" stroke="{c}"/>'
 return svg(w,h,'Developer identity: Shivanshu Shukla, CS at PW IOI, Bengaluru, Java, JavaScript and DSA. Open to internships and collaboration.',b)
def stack(mobile=False):
 w,h=(600,820) if mobile else (1200,450);b=chrome(w,'stack.map / choose your tools')
 groups=[('01','LANGUAGES',['Java','JavaScript','Python foundations'],CYAN),('02','FRONTEND',['HTML + CSS','JavaScript + React','Responsive interfaces'],PURPLE),('03','JAVA / TOOLS',['Spring Boot + Hibernate','Maven + Servlets + ORM','Git + GitHub'],PINK),('04','PROBLEM SOLVING',['DSA','Codeforces + LeetCode','GFG + BruteForce'],'#83f4c3')]
 if not mobile:
  b+=f'<path d="M55 252H1145" stroke="#335179" stroke-width="2"/>'
 for i,(num,name,items,color) in enumerate(groups):
  x,y,cw,ch=(24,72+i*166,552,151) if mobile else (24+i*292,91,276,248)
  b+=rect(x,y,cw,ch,'#111b33',color,12)+text(x+20,y+30,num+' / '+name,12,color)
  for j,item in enumerate(items):b+=text(x+20,y+72+j*(26 if mobile else 35),item,16 if mobile else 14,FG)
  if not mobile:b+=f'<circle cx="{x+cw/2}" cy="361" r="5" fill="{color}"/>'
 if mobile:b+=text(30,774,'NEXT: REACT DEPTH / NODE.JS / SYSTEM DESIGN',13,PURPLE)
 else:b+=text(30,412,'$ next --learn   React depth  •  Node.js  •  System design',15,PURPLE)
 b+=f'<circle class="motion" r="3" fill="{CYAN}"><animateMotion dur="7s" repeatCount="indefinite" path="M30 {h-15}H{w-30}"/></circle>'
 return svg(w,h,'Technical map: Java, JavaScript, Python foundations; frontend; Java backend and tools; problem solving. Learning React depth, Node.js and system design.',b)
PROJECTS=[('portfolio','PERSONAL SPACE','Shiv&Shu','My work, skills, and learning journey.','HTML / CSS / JAVASCRIPT',CYAN),('pycosmos','PERSONAL PLATFORM','PyCosmos','Python learning and practice in the browser.','REACT / JS / PYODIDE',PURPLE),('sevarecover','AMAZON BUILDATHON','SevaRecover','Clearer next steps for rejected applications.','REACT / TYPESCRIPT / PYTHON',PINK),('innovatex','END-SEMESTER','InnovateX','A shared home for our team and its work.','HTML / CSS / JAVASCRIPT','#83f4c3'),('spendwise','END-SEMESTER','SpendWise','Exploring clearer everyday money interfaces.','HTML / CSS / FINANCE UI','#ffd487'),('bus','END-SEMESTER','Bus Reservation','Seat booking, records, and a relational database.','EXPRESS / SQLITE / JS',CYAN)]
def project(item,mobile=False):
 slug,kicker,name,desc,tech,color=item;w,h=(300,265) if mobile else (490,222);b=rect(15,15,35,25,'#19253f',color,5)+text(22,33,'</>',12,color)+text(65,33,kicker,9,MUTED)+text(w-28,35,'↗',22,color,extra='text-anchor="end"')
 b+=text(22,82,name,26 if mobile else 31,FG,'bold')
 for j,line in enumerate(textwrap.wrap(desc,27 if mobile else 47)):b+=text(22,117+j*25,line,15 if mobile else 14,MUTED)
 b+=f'<path d="M22 {h-52}H{w-22}" stroke="{color}" opacity=".5"/>'+text(22,h-25,tech,8,color)
 return svg(w,h,name+': '+desc,b)
def coding_card(key,data,mobile=False):
 names={'leetcode':('LeetCode','Shivanshu_19','LC','#ffc877'),'codeforces':('Codeforces','shivanshu_19','CF',CYAN),'gfg':('GeeksforGeeks','shivanshu19','GFG','#83f4c3'),'bruteforce':('PW IOI BruteForce','shivanshu_19','BF',PINK)};name,handle,mark,color=names[key];w,h=(300,285) if mobile else (490,260)
 value=data.get('solved','↗');b=text(20,36,name,21 if mobile else 23,FG,'bold')+text(20,59,'@'+handle,12,MUTED)+text(w-22,35,mark,10,color,extra='text-anchor="end"')
 b+=text(18,134,value,64,color,'bold')+text(20,162,'ACCEPTED PROBLEMS' if key=='codeforces' else 'PROBLEMS SOLVED',11,MUTED)
 details=data.get('breakdown');y=188
 if details:
  total=max(1,sum(details.values()));start=20
  for (k,v),c in zip(details.items(),['#83f4c3','#ffc877',PINK]):
   width=(w-40)*v/total;b+=f'<rect x="{start:.1f}" y="{y}" width="{width:.1f}" height="5" rx="2" fill="{c}"/>';start+=width
  b+=text(20,y+25,' · '.join(k[0].upper()+' '+str(v) for k,v in details.items()),12,FG)
 elif 'score' in data:b+=text(20,y+13,'CODING SCORE  '+str(data['score']),14,FG)
 else:b+=text(20,y+13,'Unique accepted problems',12,FG)
 b+=f'<path d="M20 {h-39}H{w-20}" stroke="#304263"/>'+text(20,h-15,'VERIFIED '+data.get('as_of','—'),9,MUTED)+text(w-22,h-14,'↗',20,color,extra='text-anchor="end"')
 b+=f'<circle class="motion" r="2" fill="{color}"><animateMotion dur="6s" repeatCount="indefinite" path="M20 {h-39}H{w-20}"/></circle>'
 return svg(w,h,name+': '+str(value)+' problems solved; verified '+data.get('as_of','not yet available'),b)
def activity(days,data,mobile=False):
 w,h=(600,785) if mobile else (1200,495);b=chrome(w,'activity.orbit / real public contributions')
 cx,cy=(300,308) if mobile else (275,266)
 colors=['#1c2b47','#3c6793','#66aacc',CYAN,PURPLE]
 start=date.fromisoformat(data['as_of'])-timedelta(days=364);base=start-timedelta(days=(start.weekday()+1)%7)
 for r in range(7):b+=f'<circle cx="{cx}" cy="{cy}" r="{85+r*18}" fill="none" stroke="#1b2d4c" stroke-width="1"/>'
 for d,item in sorted(days.items()):
  if isinstance(d,str):d=date.fromisoformat(d)
  offset=(d-base).days;week,weekday=divmod(offset,7);a=week/53*math.tau-math.pi/2;radius=85+weekday*18;x=cx+math.cos(a)*radius;y=cy+math.sin(a)*radius;level=item['level']
  b+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{3.1 if level==0 else 3.9}" fill="{colors[min(4,level)]}"><title>{d.isoformat()}: {item["count"]} public contributions</title></circle>'
 b+=f'<circle cx="{cx}" cy="{cy}" r="61" fill="#101b35" stroke="url(#neon)"/>'+text(cx,cy-7,'GIT',25,FG,'bold',extra='text-anchor="middle"')+text(cx,cy+18,'IN ORBIT',10,CYAN,extra='text-anchor="middle"')
 b+=f'<g class="motion"><circle cx="{cx}" cy="{cy-211}" r="4" fill="{PINK}"/><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="20s" repeatCount="indefinite"/></g>'
 if mobile:
  b+=text(30,565,'SMALL COMMITS. REAL PROGRESS.',19,CYAN)
  for i,(v,k) in enumerate([(data['public_contributions_365_days'],'CONTRIBUTIONS'),(data['public_repositories'],'PUBLIC REPOS'),(len(data['original_repository_languages']),'LANGUAGES')]):b+=text(30+i*191,620,v,39,FG,'bold')+text(30+i*191,647,k,11,MUTED)
  b+=text(30,706,'Each dot = one day / 365 public days',12,MUTED)+text(30,737,'Snapshot: '+data['as_of'],12,PURPLE)
 else:
  b+=text(555,115,'A YEAR IN PUBLIC',13,CYAN)+text(555,158,'Small commits.',32,FG,'bold')+text(555,202,'Real progress.',32,PURPLE,'bold')
  for i,(v,k) in enumerate([(data['public_contributions_365_days'],'CONTRIBUTIONS'),(data['public_repositories'],'PUBLIC REPOS'),(len(data['original_repository_languages']),'LANGUAGES')]):b+=text(555+i*205,282,v,43,FG,'bold')+text(555+i*205,308,k,10,MUTED)
  b+=text(555,365,'Each dot is one day. Colour follows real activity.',13,MUTED)+text(555,399,'PUBLIC SNAPSHOT / '+data['as_of'],11,CYAN)
  b+=text(555,438,' · '.join(data['original_repository_languages']),11,MUTED)
 return svg(w,h,'Contribution orbit: '+str(data['public_contributions_365_days'])+' real publicly visible contributions across the trailing 365 days.',b)
def lab(t,mobile=False):
 w,h=(600,620) if mobile else (1200,450);b=stars(w,h)+chrome(w,'after-hours.lab / learn → build → refine')
 if mobile:b+=text(28,91,'One more idea before logging off.',20,CYAN);transform='translate(-360 90) scale(.82)'
 else:
  b+=text(35,108,'// MY KIND OF LOOP',13,PINK)
  for i,line in enumerate(['while (curious) {','  learn();','  build();','  refine();','}']):b+=text(35,160+i*38,line,24,[PURPLE,CYAN,PINK,'#83f4c3',PURPLE][i])
  transform='translate(0 0)'
 b+=f'<g transform="{transform}">'
 # Isometric floor and illuminated workstation.
 b+='<ellipse cx="852" cy="370" rx="298" ry="55" fill="#080d24" stroke="#283c66"/>'
 for i in range(7):b+=f'<path d="M{580+i*65} 323L{710+i*65} 407M{590+i*65} 402L{720+i*65} 317" stroke="#1b3153"/>'
 b+='<path d="M570 256L851 199L1080 302L794 365Z" fill="url(#panel)" stroke="#6c76b6"/><path d="M794 365L1080 302V321L794 385Z" fill="#17234a" stroke="#3f5b92"/><path d="M570 256L794 365V385L570 277Z" fill="#101a38" stroke="#3f5b92"/><path d="M608 284V368M1028 327V387" stroke="#455c8b" stroke-width="8"/>'
 # Monitor with depth, frame and code lines.
 b+='<path d="M688 107L923 137V276L688 246Z" fill="#182a51" stroke="#a58af3"/><path d="M923 137L939 129V266L923 276Z" fill="#302757" stroke="#7051a2"/><path d="M688 107L704 98L939 129L923 137Z" fill="#403764" stroke="#a58af3"/><path d="M704 125L909 151V257L704 231Z" fill="#06192a" stroke="#45718f"/>'
 for i in range(6):
  length=[120,163,90,140,115,70][i];show=.5+.5*math.sin(t*1.8+i)
  b+=f'<path d="M719 {147+i*13}l{length*(.7+.3*show):.1f} {length*.125:.1f}" stroke="{[CYAN,PURPLE,PINK][i%3]}" stroke-width="3" opacity="{.5+.4*show:.2f}"/>'
 b+='<path d="M797 262v23l42 6v-24" stroke="#7287b7" stroke-width="6" fill="none"/><path d="M710 284L821 303L775 322L663 301Z" fill="#152243" stroke="#7196bf"/>'
 for i in range(12):
  x=686+(i%6)*16;y=296+(i//6)*8+(i%6)*2;b+=f'<path d="M{x} {y}l10 1.5" stroke="{CYAN if int(t*8)%12==i else "#4b5e87"}" stroke-width="3"/>'
 # Friendly original robot: articulated arm, eyes and antenna, all code-drawn.
 dy=math.sin(t*2)*3;b+=f'<g transform="translate(0 {dy:.2f})">'
 b+='<path d="M973 310v39l-31 12M1002 312v45l33 8" fill="none" stroke="#697aa5" stroke-width="13" stroke-linecap="round"/>'
 b+=rect(937,241,80,85,'url(#panel)','#9caee4',16)+rect(950,256,54,34,'#121d3e',CYAN,9)
 b+='<path d="M942 259L910 282L875 295" fill="none" stroke="#8ca7d2" stroke-width="12" stroke-linecap="round"/>'
 angle=math.sin(t*3)*8;b+=f'<g transform="rotate({angle:.2f} 1010 261)"><path d="M1010 262l29-25l5-32" fill="none" stroke="#8ca7d2" stroke-width="11" stroke-linecap="round"/><circle cx="1045" cy="200" r="10" fill="url(#metal)" stroke="{CYAN}"/></g>'
 b+=rect(925,164,104,81,'url(#metal)','#d2dcff',21)+rect(938,181,78,45,'#0a1530','#6d9aca',12)
 eyeh=2 if 2.8<(t%4)<3 else 11
 b+=f'<rect x="953" y="197" width="13" height="{eyeh}" rx="4" fill="{CYAN}"/><rect x="990" y="197" width="13" height="{eyeh}" rx="4" fill="{CYAN}"/><path d="M971 215h12" stroke="{PINK}" stroke-width="2"/>'
 b+=f'<path d="M976 165v-20" stroke="#9bb2e6" stroke-width="3"/><circle cx="976" cy="140" r="6" fill="{PINK}"/>'
 b+='</g>'
 # Floating idea tiles and a traveling signal.
 for i,(label,col,x,y) in enumerate([('JAVA',CYAN,555,118),('JS',PURPLE,1068,112),('DSA',PINK,1100,215)]):
  yy=y+math.sin(t*1.1+i)*7;b+=rect(x,yy,70,42,'#182348',col,9)+text(x+35,yy+27,label,15,col,extra='text-anchor="middle"')
 b+='</g>'
 b+=text(30,h-27,'IDEAS IN.  A LITTLE MORE UNDERSTANDING OUT.',11 if mobile else 12,MUTED)
 return svg(w,h,'An original animated isometric robot developer lab, with typing monitors, moving hands, floating Java, JavaScript and DSA tiles.',b)
def footer(mobile=False):
 w,h=(600,235) if mobile else (1200,220);b=chrome(w,'connection.open / let’s make something')+text(30,104,'Have an idea worth building?',26 if mobile else 35,FG,'bold')+text(30,147,'Internships · Collaborations · Good conversations',14 if mobile else 18,CYAN)+text(30,h-27,'shivanshushukla2602@gmail.com',12,PURPLE)
 return svg(w,h,'Contact Shivanshu for internships and collaboration.',b)
