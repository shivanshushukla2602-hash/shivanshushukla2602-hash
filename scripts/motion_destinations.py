"""Six distinct motion-graphics identities, rendered as GitHub-native GIFs.

Portal architecture, a twisting code ribbon, a Newton cradle, a living helix,
an exploding origami core and an iridescent wave use different geometry and
motion. Only destination names and links appear; no inventory or statistics.
"""
import argparse
import colorsys
import math
from PIL import Image, ImageDraw, ImageFilter
from kinetic_sections import Canvas, OUT, FG, MUTED, TAU, rotate, project
from profile_destinations import arrow, button


def rgb(h,s,v):
    return tuple(round(255*x) for x in colorsys.hsv_to_rgb(h%1,min(1,s),min(1,v)))


def glow(c,x,y,color,radius=100):
    layer=Image.new('RGBA',c.im.size)
    d=ImageDraw.Draw(layer)
    for i in range(20,0,-1):
        r=radius*i/20
        d.ellipse(((x-r)*2,(y-r*.7)*2,(x+r)*2,(y+r*.7)*2),fill=(*color,round(2+(20-i)*.6)))
    layer=layer.filter(ImageFilter.GaussianBlur(24))
    c.im=Image.alpha_composite(c.im.convert('RGBA'),layer).convert('RGB')
    c.d=ImageDraw.Draw(c.im)


class Motion:
    def __init__(self,c,x,y,zoom=1):
        self.c,self.x,self.y,self.zoom=c,x,y,zoom
        self.faces=[]

    def point(self,p):return project(p,self.x,self.y,self.zoom)

    def face(self,points,hue=.12,saturation=.5,metal=False,two_sided=True):
        a,b,c=points[:3]
        u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
        n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        size=math.sqrt(sum(x*x for x in n)) or 1
        n=tuple(x/size for x in n)
        if n[2]<0:
            if not two_sided:return
            n=tuple(-x for x in n)
        diffuse=max(0,-n[0]*.35-n[1]*.55+n[2]*.73)
        specular=max(0,-n[0]*.15-n[1]*.3+n[2]*.94)**22
        value=.24+.57*diffuse+.25*specular
        h=hue+(n[0]*.15+n[1]*.12 if metal else 0)
        color=rgb(h,saturation*(1-.7*specular),value)
        self.faces.append((sum(p[2] for p in points)/len(points),points,color))

    def box(self,center,size,angles,hue=.12,saturation=.5):
        vertices=[]
        for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
            p=rotate((a*size[0]/2,b*size[1]/2,c*size[2]/2),*angles)
            vertices.append(tuple(p[i]+center[i] for i in range(3)))
        for face in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(1,2,6,5),(0,4,7,3)]:
            self.face([vertices[i] for i in face],hue,saturation,two_sided=False)

    def ball(self,center,radius,hue):
        n,m=24,14
        for i in range(m):
            a,b=-math.pi/2+i*math.pi/m,-math.pi/2+(i+1)*math.pi/m
            for j in range(n):
                u,v=j*TAU/n,(j+1)*TAU/n
                points=[tuple(center[k]+radius*p for k,p in enumerate((math.cos(t)*math.cos(s),math.sin(t),math.cos(t)*math.sin(s)))) for t,s in [(a,u),(b,u),(b,v),(a,v)]]
                self.face(points,hue,.64,metal=True,two_sided=False)

    def line(self,points,color,width=1):self.c.line([self.point(p) for p in points],color,width)

    def draw(self):
        for _,points,color in sorted(self.faces,key=lambda f:f[0]):self.c.poly([self.point(p) for p in points],color)


def portal(c,x,y,t,zoom=1):
    glow(c,x,y,(100,137,237),170*zoom)
    m=Motion(c,x,y,zoom)
    # Five independently opening architectural frames, with a luminous aperture.
    for i in range(5):
        z=-110+i*39
        tilt=.16*math.sin(t-i*.38)
        yaw=-.36+.14*math.sin(t+i*.32)
        cy=9*math.sin(t+i*.5)
        hue=.59 if i%2 else .12
        for center,size in [((-97,cy,z),(12,225,12)),((97,cy,z),(12,225,12)),((0,cy-107,z),(194,12,12)),((0,cy+107,z),(194,12,12))]:
            center=rotate(center,.12,yaw,tilt)
            m.box(center,size,(.12,yaw,tilt),hue,.17 if i%2==0 else .42)
    # A glass-like plane of light behind the frames, with racing horizontal traces.
    for j in range(12):
        y0=-80+j*14
        a=.5+.5*math.sin(t*2-j*.45)
        m.line([(-68,y0,-120),(68,y0,-120)],rgb(.59,.4,.12+a*.13),.8)
    m.draw()
    # A dimensional cursor crosses the aperture on a gently curved path.
    dx=53+20*math.sin(t);dy=58+14*math.cos(t)
    cursor=[(dx-16,dy-30,130),(dx-10,dy+26,130),(dx+3,dy+12,130),(dx+18,dy+38,130),(dx+28,dy+32,130),(dx+13,dy+6,130),(dx+34,dy+2,130)]
    c.poly([m.point(p) for p in cursor], '#f3e5c9','#8d846e')


def ribbon(c,x,y,t,zoom=1):
    glow(c,x,y,(200,102,33),130*zoom)
    m=Motion(c,x,y,zoom)
    # A helical orange strip folds through depth, rather than orbiting on a base.
    for i in range(100):
        u=i/100;v=(i+1)/100
        points=[]
        for s,side in [(u,-1),(v,-1),(v,1),(u,1)]:
            angle=s*TAU+t
            p=((s-.5)*260,math.sin(angle)*48+side*26*math.cos(angle),math.cos(angle)*58+side*26*math.sin(angle))
            points.append(rotate(p,0,-.22,-.14))
        m.face(points,.085,.78,metal=False)
    m.draw()
    # Subtle bracket marks frame the ribbon without imitating a platform logo.
    c.line([(x-145*zoom,y-42*zoom),(x-164*zoom,y),(x-145*zoom,y+42*zoom)],'#ddac67',2)
    c.line([(x+145*zoom,y-42*zoom),(x+164*zoom,y),(x+145*zoom,y+42*zoom)],'#ddac67',2)


def cradle(c,x,y,t,zoom=1):
    glow(c,x,y,(57,133,225),125*zoom)
    m=Motion(c,x,y,zoom)
    # A Newton cradle: only the outside bob on each side swings outward.
    for z in [-23,23]:m.line([(-115,87,z),(-115,-94,z),(115,-94,z),(115,87,z)],'#48677a',2.3)
    balls=[]
    for i in range(5):
        pivot=-76+i*38
        swing=max(0,math.sin(t))*.7 if i==0 else (-max(0,-math.sin(t))*.7 if i==4 else 0)
        dx=-math.sin(swing)*120
        by=-94+math.cos(swing)*120
        for z in [-23,23]:m.line([(pivot,-94,z),(pivot+dx,by,0)],'#a2c4d9',.9)
        balls.append(((pivot+dx,by,0),18,.57+i*.018))
    for center,r,hue in balls:m.ball(center,r,hue)
    m.draw()


def helix(c,x,y,t,zoom=1):
    glow(c,x,y,(52,168,115),140*zoom)
    m=Motion(c,x,y,zoom)
    # Two living strands rotate; an independently travelling pulse crosses rungs.
    strands=[]
    for side in [0,math.pi]:
        points=[]
        for i in range(81):
            f=i/80;a=f*TAU*1.4+t+side
            points.append((math.cos(a)*66,(f-.5)*205,math.sin(a)*66))
        strands.append(points)
        m.line(points,'#70bda1' if side==0 else '#355b51',2)
    for i in range(13):
        f=i/12;a=f*TAU*1.4+t
        p=(math.cos(a)*66,(f-.5)*205,math.sin(a)*66)
        q=(-p[0],p[1],-p[2])
        pulse=(.5+.5*math.cos(t-i*.52))**6
        m.line([p,q],rgb(.43,.5,.19+pulse*.5),1.2)
        for node in [p,q]:m.ball(node,4.5+2*pulse,.40)
    m.draw()


def origami(c,x,y,t,zoom=1):
    glow(c,x,y,(194,72,106),125*zoom)
    m=Motion(c,x,y,zoom)
    # Eight triangular facets unfold away from an octahedral core, then return.
    vertices=[(0,-88,0),(0,88,0),(-76,0,0),(0,0,76),(76,0,0),(0,0,-76)]
    opening=(.5-.5*math.cos(t))**2*40
    for cap in [0,1]:
        for j in range(4):
            pts=[vertices[cap],vertices[2+j],vertices[2+(j+1)%4]]
            center=tuple(sum(p[k] for p in pts)/3 for k in range(3))
            norm=math.sqrt(sum(a*a for a in center))
            pushed=[tuple(p[k]+center[k]/norm*opening for k in range(3)) for p in pts]
            turned=[rotate(p,.25,t,.16*math.sin(t)) for p in pushed]
            m.face(turned,.95 if (j+cap)%2 else .63,.65,metal=True)
    m.draw()
    # Small sparks travel independently of the unfolding surfaces.
    for i in range(6):
        a=t+i*TAU/6
        p=m.point((math.cos(a)*145,math.sin(a)*112,0))
        c.line([(p[0]-2,p[1]),(p[0]+2,p[1])],'#bd7e9e',1)


def silk(c,x,y,t,zoom=1):
    glow(c,x,y,(101,79,189),165*zoom)
    m=Motion(c,x,y,zoom)
    # A wide woven surface carries travelling waves through three-dimensional space.
    for i in range(80):
        u=i/80;v=(i+1)/80
        for j in range(14):
            a=j/14;b=(j+1)/14
            points=[]
            for s,q in [(u,a),(v,a),(v,b),(u,b)]:
                z=math.sin(s*TAU*1.4-t+q*1.3)*52+math.cos(q*math.pi)*18
                p=((s-.5)*330,(q-.5)*150+math.sin(s*TAU-t)*27,z)
                points.append(rotate(p,-.46,.25,-.34))
            m.face(points,.68+u*.2,.46,metal=True)
    m.draw()
    for i in range(16):
        a=i*2.39996
        r=100+(i%4)*18
        p=m.point((math.cos(a)*r,math.sin(a)*r*.8,-80))
        c.d.ellipse(((p[0]-1)*2,(p[1]-1)*2,(p[0]+1)*2,(p[1]+1)*2),fill='#756b8e')


def portfolio_frame(t,mobile=False):
    w,h=(640,790) if mobile else (1080,560)
    c=Canvas(w,h)
    c.text(34,45,'A DOOR TO MY WORK',12,MUTED)
    c.text(32,119,'Step into',54,bold=True)
    c.text(32,183,'my world.',54,bold=True)
    c.text(34,227,'Interfaces, experiments, and a little curiosity.',15,MUTED)
    button(c,34,260,'Explore my portfolio',250)
    portal(c,320 if mobile else 780,529 if mobile else 275,t,1.05 if mobile else 1.18)
    c.line([(34,h-61),(w-34,h-61)])
    c.text(34,h-31,'SHIV-AND-SHU-PORTFOLIO.VERCEL.APP',11,MUTED)
    arrow(c,w-35,h-44)
    return c.finish()


PLATFORMS={
    'leetcode':('LeetCode','Shivanshu_19','THE CODE RIBBON',ribbon),
    'codeforces':('Codeforces','shivanshu_19','MOMENTUM IN MOTION',cradle),
    'gfg':('GeeksforGeeks','shivanshu19','CONNECTED BY CURIOSITY',helix),
}


def practice_frame(key,t):
    title,handle,label,art=PLATFORMS[key]
    c=Canvas(540,400)
    c.text(26,48,title,29,bold=True)
    c.text(27,75,handle,13,MUTED)
    # Each card has its own silhouette, material palette and motion mechanism.
    art(c,270,215,t,.8 if key=='gfg' else 1)
    c.text(270,329,label,10,MUTED,anchor='ms')
    c.line([(27,349),(513,349)])
    c.text(27,378,'Open my profile',14)
    arrow(c,510,364,12)
    return c.finish()


def experiment_frame(t,mobile=False):
    w,h=(640,750) if mobile else (1080,500)
    c=Canvas(w,h)
    c.text(34,44,'AN EXERCISE IN MOTION',12,MUTED)
    c.text(32,116,'Follow the',49,bold=True)
    c.text(32,175,'unexpected.',49,bold=True)
    c.text(34,221,'A new angle. A different possibility.',15,MUTED)
    silk(c,320 if mobile else 780,482 if mobile else 258,t,1.05 if mobile else 1.18)
    c.line([(34,h-60),(w-34,h-60)])
    c.text(34,h-30,'KEEP EXPLORING. KEEP MAKING.',11,MUTED)
    return c.finish()


def render(name,draw,preview=False):
    still=draw(0)
    still.save(OUT/(name+'-static.png'),optimize=True)
    if preview:return
    frames=[draw(i/60*TAU) for i in range(60)]
    sample=Image.new('RGB',(still.width,still.height*4))
    for i,j in enumerate([0,15,30,45]):sample.paste(frames[j],(0,i*still.height))
    palette=sample.quantize(colors=224,method=Image.Quantize.MEDIANCUT)
    images=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    dest=OUT/(name+'.gif')
    images[0].save(dest,save_all=True,append_images=images[1:],duration=100,loop=0,optimize=True,disposal=1)
    print(name,round(dest.stat().st_size/1024),'KB',flush=True)


def main(preview=False):
    for mobile in [False,True]:
        suffix='-mobile' if mobile else ''
        render('portfolio-portal'+suffix+'-v13',lambda t:portfolio_frame(t,mobile),preview)
        render('motion-silk'+suffix+'-v13',lambda t:experiment_frame(t,mobile),preview)
    for key in PLATFORMS:render('practice-'+key+'-v13',lambda t:practice_frame(key,t),preview)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true')
    main(parser.parse_args().preview)
