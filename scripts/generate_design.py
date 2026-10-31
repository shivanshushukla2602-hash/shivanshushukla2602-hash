#!/usr/bin/env python3
"""Original, code-drawn artwork. No reference-profile assets or third-party cards."""
from pathlib import Path
from html import escape
from PIL import Image,ImageDraw,ImageFont
import math,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
BG='#101010';FG='#f5f4ef';ACC='#eee2c6';MUTED='#b7b6af';LINE='#44433e'
def font(size,bold=False,serif=False):
    candidates=([('/System/Library/Fonts/Supplemental/Georgia Italic.ttf'),'/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'] if serif else ['/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for p in candidates:
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default(size=size)
def header(frame):
    im=Image.new('RGB',(1200,440),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,1198,438),radius=22,outline=LINE,width=2)
    for x in range(800,1190,24):
        for y in range(110,418,24):d.ellipse((x,y,x+1,y+1),fill='#282827')
    d.text((46,34),'SHIV&SHU / A DEVELOPER IN PROGRESS',font=font(12),fill=MUTED)
    d.text((42,83),'SHIVANSHU',font=font(83,True),fill=FG)
    d.text((42,174),'SHUKLA.',font=font(83,True),fill=FG)
    d.text((46,279),'A curious mind. A builder by habit.',font=font(29,serif=True),fill=ACC)
    roles=['Java & backend development','Interfaces with intent','DSA. One problem at a time.'];phase=frame//24;progress=(frame%24)/24;role=roles[phase%3];count=min(len(role),int(progress*len(role)*2.4));text=role[:count]
    d.text((48,341),text,font=font(22),fill='#d5d2c8')
    if frame%8<4:
        x=48+d.textlength(text,font=font(22));d.rectangle((x+5,344,x+7,364),fill=ACC)
    d.text((48,398),'PW IOI  /  COMPUTER SCIENCE  /  BENGALURU',font=font(11),fill=MUTED)
    d.rounded_rectangle((904,28,1153,64),radius=18,fill=ACC)
    d.text((926,39),'OPEN TO INTERNSHIPS',font=font(12,True),fill='#211e18')
    # A moving signal travels through an abstract, original stack of work surfaces.
    points=[(758,372),(824,372),(874,323),(1068,323),(1127,265)]
    d.line(points,fill='#706d62',width=2)
    phase=(frame/72)%1;segments=[math.dist(a,b) for a,b in zip(points,points[1:])];dist=sum(segments)*phase
    for i,length in enumerate(segments):
        if dist<=length:
            a,b=points[i],points[i+1];q=dist/length;x=a[0]+(b[0]-a[0])*q;y=a[1]+(b[1]-a[1])*q;d.ellipse((x-4,y-4,x+4,y+4),fill=ACC);break
        dist-=length
    dy=math.sin(frame/72*math.tau)*5
    for offset,fill in [(22,'#171716'),(11,'#20201e'),(0,'#2a2925')]:
        y=130+dy-offset;d.rounded_rectangle((864+offset,y,1104+offset,y+167),radius=12,fill=fill,outline='#767064',width=1)
    d.text((884,147+dy),'IDEA → CODE → REFINE',font=font(10),fill=MUTED)
    d.text((918,175+dy),'</>',font=font(70,True),fill=ACC)
    d.line((887,268+dy,1081,268+dy),fill='#797365',width=1)
    d.text((887,279+dy),'JAVA  /  JS  /  DSA',font=font(9),fill=MUTED)
    d.text((823,400),'LEARNING BY BUILDING, IN PUBLIC.',font=font(11),fill=MUTED)
    return im
frames=[header(i) for i in range(72)];frames[-1].save(OUT/'header-static.png');frames[0].save(OUT/'header.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
def svg(w,h,title,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="#141413" stroke="{LINE}"/>{body}</svg>'
def text(x,y,t,size=14,fill=FG,weight='normal',extra=''):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{escape(t)}</text>'
body=text(36,42,'THE PERSON / NOT JUST THE CODE',10,MUTED,extra='letter-spacing="2"')+text(36,91,'Shivanshu Shukla',34,FG,'bold')+text(36,125,'CS student at PW IOI · Bengaluru · 2025–2029',16,MUTED)
body+='<path d="M36 154H1164" stroke="#414039"/>'
for x,kicker,first,second in [(36,'MY FOCUS','Java + JavaScript','Frontend + DSA'),(433,'MY APPROACH','Learn something.','Put it to work.'),(830,'LOOKING FOR','Internships','People to build with')]:
    body+=text(x,187,kicker,10,MUTED,extra='letter-spacing="1.5"')+text(x,221,first,19,ACC)+text(x,249,second,17,FG)
(OUT/'about.svg').write_text(svg(1200,282,'About Shivanshu: CS student at PW IOI, Bengaluru; Java, JavaScript, frontend, DSA; open to internships and collaboration.',body))
groups=[('LANGUAGES',['Java','JavaScript','Python foundations']),('FRONTEND',['HTML · CSS','JavaScript · React','Responsive interfaces']),('JAVA & TOOLS',['Spring Boot · Hibernate','Maven · Servlets · ORM','Git · GitHub']),('PROBLEM SOLVING',['Data structures','Algorithms','Codeforces · LeetCode · GFG'])]
body=text(36,40,'TOOLS I USE. THINGS I’M LEARNING.',11,MUTED,extra='letter-spacing="2"')
for i,(label,items) in enumerate(groups):
    x=25+i*290;body+=f'<rect x="{x}" y="65" width="280" height="174" rx="12" fill="#1d1c19" stroke="#474438"/>'
    body+=text(x+20,96,f'0{i+1} / {label}',10,ACC)
    for j,item in enumerate(items):body+=text(x+20,135+j*29,item,14,FG)
body+=text(36,277,'EXPLORING NEXT',9,MUTED,extra='letter-spacing="1.5"')+text(230,277,'Deeper React · Node.js · System design',14,ACC)
(OUT/'stack.svg').write_text(svg(1200,312,'Skill map: Java, JavaScript, Python foundations, frontend, Java backend tools and DSA. Next: React, Node.js and system design.',body))
projects=[('portfolio','01 / MY PORTFOLIO','Shiv&Shu','A personal space for my work,','skills, and learning journey.','HTML · CSS · JAVASCRIPT'),('pycosmos','02 / PERSONAL PLATFORM','PyCosmos','Python learning and practice,','together in the browser.','REACT · JAVASCRIPT · PYODIDE'),('sevarecover','03 / AMAZON BUILDATHON','SevaRecover','Understand rejected applications.','Explore clearer next steps.','REACT · TYPESCRIPT · PYTHON'),('innovatex','04 / END-SEMESTER','InnovateX','A shared home for our team','and the work we make together.','HTML · CSS · JAVASCRIPT'),('spendwise','05 / END-SEMESTER','SpendWise','A clearer interface for budgets','and everyday money information.','HTML · CSS · FINANCE UI'),('bus','06 / END-SEMESTER','Bus Reservation','Connect seat booking, passenger','records, and a relational database.','EXPRESS · SQLITE · JAVASCRIPT')]
for slug,kicker,name,a,b,stack in projects:
    body=text(26,33,kicker,9,MUTED,extra='letter-spacing="1.4"')+text(26,77,name,31,ACC,'bold')+text(26,113,a,14,FG)+text(26,135,b,14,FG)+text(26,181,stack,9,MUTED,extra='letter-spacing=".5"')+text(445,40,'↗',23,ACC)
    (OUT/f'project-{slug}.svg').write_text(svg(490,205,name+': '+a+' '+b,body))
body=text(36,43,'SOMETHING WORTH BUILDING?',10,MUTED,extra='letter-spacing="2"')+text(36,92,'Let’s make the next thing.',36,ACC,'bold')+text(36,133,'An internship. A collaboration. A good conversation.',17,FG)
body+='<path d="M36 163H1164" stroke="#474438"/>'+text(36,197,'SHIV&SHU / BENGALURU, INDIA',11,MUTED)+text(1160,197,'ALWAYS A WORK IN PROGRESS.',11,MUTED,extra='text-anchor="end"')
(OUT/'footer.svg').write_text(svg(1200,230,'Get in touch: open to internships and collaboration.',body))
print('Generated animated header, static fallback, about, skills, project cards, and footer.')

# Compact artwork keeps the important text readable on narrow profile screens.
def header_mobile(frame):
    im=Image.new('RGB',(600,540),BG);d=ImageDraw.Draw(im);d.rounded_rectangle((1,1,598,538),radius=22,outline=LINE,width=2)
    d.text((30,28),'SHIV&SHU / BUILDING IN PUBLIC',font=font(12),fill=MUTED)
    d.rounded_rectangle((30,69,252,100),radius=15,fill=ACC);d.text((47,78),'OPEN TO INTERNSHIPS',font=font(11,True),fill='#211e18')
    d.text((25,132),'SHIVANSHU',font=font(66,True),fill=FG);d.text((25,207),'SHUKLA.',font=font(66,True),fill=FG)
    d.text((30,300),'A curious mind.',font=font(29,serif=True),fill=ACC);d.text((30,340),'A builder by habit.',font=font(29,serif=True),fill=ACC)
    roles=['Java & backend development','Interfaces with intent','DSA. One problem at a time.'];role=roles[(frame//24)%3];count=min(len(role),int((frame%24)/24*len(role)*2.4));v=role[:count];d.text((30,414),v,font=font(20),fill='#d5d2c8')
    if frame%8<4:
        x=30+d.textlength(v,font=font(20));d.rectangle((x+5,417,x+7,435),fill=ACC)
    d.line((30,469,570,469),fill=LINE,width=1);x=30+540*(frame/72);d.ellipse((x-3,466,x+3,472),fill=ACC);d.text((30,501),'PW IOI · COMPUTER SCIENCE · BENGALURU',font=font(12),fill=MUTED)
    return im
mframes=[header_mobile(i) for i in range(72)];mframes[-1].save(OUT/'header-mobile-static.png');mframes[0].save(OUT/'header-mobile.gif',save_all=True,append_images=mframes[1:],duration=100,loop=0,optimize=True)
body=text(26,37,'THE PERSON BEHIND THE COMMITS',10,MUTED,extra='letter-spacing="1"')+text(26,87,'Shivanshu Shukla',31,FG,'bold')+text(26,122,'CS student · PW IOI · Bengaluru',15,MUTED)+text(26,148,'2025–2029',13,MUTED)
for y,kicker,a,b in [(196,'MY FOCUS','Java + JavaScript','Frontend + DSA'),(310,'MY APPROACH','Learn something.','Put it to work.'),(424,'LOOKING FOR','Internships','People to build with')]:
    body+=f'<path d="M26 {y-21}H454" stroke="#414039"/>'+text(26,y,kicker,9,MUTED,extra='letter-spacing="1.5"')+text(26,y+32,a,21,ACC)+text(26,y+61,b,18,FG)
(OUT/'about-mobile.svg').write_text(svg(480,516,'Shivanshu Shukla: CS student at PW IOI in Bengaluru, 2025–2029. Java, JavaScript, frontend and DSA. Open to internships.',body))
body=text(26,38,'MY WORKING TOOLKIT',11,MUTED,extra='letter-spacing="1.5"')
for i,(label,items) in enumerate(groups):
    y=62+i*145;body+=f'<rect x="22" y="{y}" width="436" height="132" rx="12" fill="#1d1c19" stroke="#474438"/>'+text(42,y+28,f'0{i+1} / {label}',10,ACC)
    for j,item in enumerate(items):body+=text(42,y+57+j*25,item,17,FG)
body+=text(26,680,'LEARNING NEXT',10,MUTED)+text(26,711,'Deeper React · Node.js · System design',15,ACC)
(OUT/'stack-mobile.svg').write_text(svg(480,742,'Java, JavaScript, Python foundations; HTML, CSS and React; Spring Boot, Hibernate, Maven, Servlets, ORM, Git and GitHub; DSA. Learning deeper React, Node.js and system design.',body))

# Compact project cards retain readable titles when GitHub uses two columns on phones.
import textwrap
for slug,kicker,name,a,b,stack in projects:
    body=text(18,29,kicker,8,MUTED,extra='letter-spacing=".4"')+text(18,71,name,25,ACC,'bold')
    for j,line in enumerate(textwrap.wrap(a+' '+b,28)):body+=text(18,108+j*25,line,16,FG)
    body+=text(18,221,stack,7,MUTED)+text(255,30,'↗',19,ACC)
    (OUT/f'project-{slug}-mobile.svg').write_text(svg(280,242,name+': '+a+' '+b,body))
