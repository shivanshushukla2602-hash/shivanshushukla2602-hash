"""Render the profile's linked destinations and original isometric dioramas.

Pure offline geometry: warm materials, directional shading, articulated props,
and seamless six-second motion. No project inventory or coding statistics.
"""
import argparse
import math
from PIL import Image
from kinetic_sections import Canvas, FG, MUTED, LINE, OUT, TAU


def tint(color, amount):
    value=color.lstrip('#')
    return tuple(min(255,max(0,round(int(value[i:i+2],16)*amount))) for i in [0,2,4])


class Diorama:
    def __init__(self,canvas,x,y,scale):
        self.canvas,self.x,self.y,self.scale=canvas,x,y,scale
        self.faces=[]

    def project(self,p):
        x,y,z=p
        return self.x+(x-z)*.82*self.scale,self.y+((x+z)*.35-y)*self.scale

    def poly(self,points,color,shade=1):
        depth=sum(x+y*.8+z for x,y,z in points)/len(points)
        self.faces.append((depth,points,tint(color,shade)))

    def box(self,x,y,z,w,h,d,color,angle=0):
        def p(a,b,c):
            return (x+a*math.cos(angle)+c*math.sin(angle),y+b,z-a*math.sin(angle)+c*math.cos(angle))
        v=[p(a*w/2,b*h/2,c*d/2) for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
        for face in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(1,2,6,5),(0,4,7,3)]:
            points=[v[i] for i in face]
            self.surface(points,color)

    def surface(self,points,color):
        a,b,c=points[:3]
        u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
        n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        length=math.sqrt(sum(a*a for a in n)) or 1
        n=tuple(a/length for a in n)
        if n[0]+n[1]*.8+n[2]<-.001:return
        light=max(0,n[0]*-.3+n[1]*.85+n[2]*.4)
        self.poly(points,color,.58+.48*light)

    def sphere(self,x,y,z,rx,ry,rz,color):
        n,m=16,10
        for i in range(m):
            a,b=-math.pi/2+i*math.pi/m,-math.pi/2+(i+1)*math.pi/m
            for j in range(n):
                u,v=j*TAU/n,(j+1)*TAU/n
                points=[(x+rx*math.cos(t)*math.cos(s),y+ry*math.sin(t),z+rz*math.cos(t)*math.sin(s)) for t,s in [(a,u),(a,v),(b,v),(b,u)]]
                # Sphere winding follows outward normals.
                self.surface(list(reversed(points)),color)

    def rod(self,a,b,r,color):
        v=[b[i]-a[i] for i in range(3)]
        length=math.sqrt(sum(t*t for t in v)) or 1
        v=[t/length for t in v]
        ref=(0,1,0) if abs(v[1])<.9 else (1,0,0)
        u=[v[1]*ref[2]-v[2]*ref[1],v[2]*ref[0]-v[0]*ref[2],v[0]*ref[1]-v[1]*ref[0]]
        length=math.sqrt(sum(t*t for t in u));u=[t/length for t in u]
        w=[v[1]*u[2]-v[2]*u[1],v[2]*u[0]-v[0]*u[2],v[0]*u[1]-v[1]*u[0]]
        rings=[]
        for center in [a,b]:
            rings.append([tuple(center[k]+r*(u[k]*math.cos(i*TAU/12)+w[k]*math.sin(i*TAU/12)) for k in range(3)) for i in range(12)])
        for i in range(12):self.surface([rings[0][i],rings[0][(i+1)%12],rings[1][(i+1)%12],rings[1][i]],color)
        self.poly(rings[1],color,1.05)

    def floor(self,w=6,d=4):
        self.box(0,-.16,0,w,.25,d,'#514b60')
        self.box(0,-.015,0,w-.28,.03,d-.28,'#736b84')
        for i in range(12):
            self.box(-w/2+.35+i*(w-.7)/12,.007,0,.012,.012,d-.35,'#8b809e')

    def monitor(self,x,y,z,w,h,phase):
        start=len(self.faces)
        self.box(x,y,z,w,h,.14,'#34443d')
        # Group the thin display surfaces so the screen markings stay above
        # their coplanar backing in the painter's depth order.
        base=x+y*.8+z+.1
        frame=sorted(self.faces[start:],key=lambda f:f[0])
        self.faces[start:]=[(base+i*.00001,p,c) for i,(_,p,c) in enumerate(frame)]
        detail_start=len(self.faces)
        self.box(x,y,z+.082,w-.13,h-.13,.018,'#201f2e')
        self.box(x,y+h*.39,z+.101,w-.15,.065,.012,'#b7a4d3')
        for i in range(7):
            length=w*(.26+((i*7)%9)/22)
            self.box(x-w*.39+length/2,y+h*.25-i*h*.09,z+.11,length,.024,.012,['#c3a9df','#9bbdae','#d1ba8a'][i%3])
        self.box(x,y-h*.3,z+.111,w*.69,.04,.014,'#51475f')
        self.box(x-w*.34+w*.34*(.5+.5*math.sin(phase)),y-h*.3,z+.121,.13,.04,.012,'#e2d5b7')
        self.faces[detail_start:]=[(base+.01+i*.00001,p,c) for i,(_,p,c) in enumerate(self.faces[detail_start:])]
        self.rod((x,y-h/2,z),(x,y-h/2-.38,z),.045,'#4a4c4c')
        self.box(x,y-h/2-.38,z,.7,.045,.4,'#646071')

    def plant(self,x,z,y=0):
        self.box(x,y+.22,z,.38,.44,.38,'#cfc5ab')
        for i in range(6):
            a=i*2.4
            end=(x+.24*math.cos(a),y+.7+(i%3)*.12,z+.24*math.sin(a))
            self.rod((x,y+.4,z),end,.016,'#56735e')
            self.sphere(*end,.12,.2,.09,'#8cac84')

    def robot(self,x,z,phase,y=0):
        # Rounded, articulated little workshop companion.
        self.box(x,y+.8,z,.72,.67,.48,'#9c8caf')
        self.sphere(x,y+1.4+.025*math.sin(phase),z,.43,.36,.34,'#c6b5d5')
        self.box(x,y+1.42,z+.308,.59,.17,.075,'#293c36')
        for dx in [-.14,.14]:self.box(x+dx,y+1.44,z+.354,.063,.055,.02,'#dcf0ca')
        self.rod((x,y+1.72,z),(x,y+1.94,z),.025,'#c8b38c')
        self.sphere(x,y+1.97,z,.07,.07,.07,'#c6d8a7')
        for side in [-1,1]:
            self.rod((x+side*.21,y+.56,z),(x+side*.24,y+.2,z+.05),.1,'#53645b')
            self.box(x+side*.24,y+.13,z+.15,.25,.18,.43,'#d8d5c5')
            shoulder=(x+side*.39,y+1.03,z)
            elbow=(x+side*.59,y+.83+.06*math.sin(phase+side),z+.18)
            hand=(x+side*(.62+.09*math.sin(phase)),y+1.12+.13*math.sin(phase+side),z+.45)
            self.rod(shoulder,elbow,.085,'#9583a8');self.rod(elbow,hand,.07,'#c2b0cd')
            self.sphere(*hand,.095,.095,.095,'#d8d0b7')

    def draw(self):
        for _,points,color in sorted(self.faces,key=lambda f:f[0]):self.canvas.poly([self.project(p) for p in points],color)


def arrow(c,x,y,size=13):
    c.line([(x-size,y+size),(x,y)],FG,1.4)
    c.line([(x-size,y),(x,y),(x,y+size)],FG,1.4)


def button(c,x,y,label,w):
    c.d.rounded_rectangle((x*2,y*2,(x+w)*2,(y+48)*2),radius=24*2,fill='#20221e',outline='#716b5a',width=2)
    c.text(x+20,y+30,label,15,bold=True)
    arrow(c,x+w-22,y+17,11)


def portfolio_frame(phase,mobile=False):
    w,h=(640,760) if mobile else (1080,540)
    c=Canvas(w,h)
    c.text(34,44,'MY DIGITAL HOME',12,MUTED)
    c.text(32,115,'A little more',46 if mobile else 52,bold=True)
    c.text(32,175,'of what I build.',46 if mobile else 52,bold=True)
    c.text(34,218,'Ideas, experiments, and the details between.',15,MUTED)
    button(c,34,248,'Explore my portfolio',250)
    d=Diorama(c,320 if mobile else 769,563 if mobile else 345,62 if mobile else 67)
    d.floor(5.8,4.2)
    d.box(0,1.38,-.4,4.5,.16,1.9,'#c3ad86')
    for x in [-1.9,1.9]:
        for z in [-1.1,.3]:d.box(x,.65,z,.08,1.35,.08,'#38453d')
    d.monitor(.15,2.55,-.93,2.6,1.55,phase)
    # Side tablet, keyboard, moving cursor and notebooks.
    d.monitor(-1.65,2.12,-.65,.72,1.05,phase+1)
    d.box(0,1.5,.04,1.18,.065,.4,'#b8c2af')
    for i in range(12):
        for j in range(3):d.box(-.5+i*.088,1.54,-.09+j*.11,.06,.024,.07,'#e1ddcd')
    d.box(1.22,1.49,.03,.53,.025,.48,'#63755f')
    d.sphere(1.22+.04*math.sin(phase),1.55,.04,.09,.05,.13,'#d7d6c6')
    for i in range(3):d.box(-1.65,1.54+i*.08,.13,.5,.07,.34,['#a799b5','#d6c7a3','#9db299'][i])
    d.plant(-2.1,1.18)
    # A friendly robot at the desk, with floating design components behind it.
    d.robot(.2,1.15,phase)
    for i in range(3):
        d.box(1.45+i*.18,2.2+i*.35+.08*math.sin(phase+i),.6,.4,.4,.4,['#a291bd','#a7b894','#d7bc89'][i],.3*math.sin(phase+i))
    d.draw()
    c.line([(34,h-60),(w-34,h-60)])
    c.text(34,h-30,'SHIV-AND-SHU-PORTFOLIO.VERCEL.APP',11,MUTED)
    arrow(c,w-35,h-43)
    return c.finish()


PLATFORMS={
    'leetcode':('LeetCode','Shivanshu_19'),
    'codeforces':('Codeforces','shivanshu_19'),
    'gfg':('GeeksforGeeks','shivanshu19'),
    'bruteforce':('BruteForce','shivanshu_19'),
}


def practice_frame(key,phase):
    c=Canvas(540,350)
    name,handle=PLATFORMS[key]
    c.text(26,49,name,28,bold=True)
    c.text(27,76,handle,13,MUTED)
    d=Diorama(c,281,221,45)
    d.floor(3.4,2.5)
    if key=='leetcode':
        d.monitor(0,1.05,-.3,2.05,1.15,phase)
        d.box(0,.16,.4,2.1,.09,1.2,'#9a8ca8')
        for row in range(3):
            for col in range(8):d.box(-.75+col*.21,.22,.16+row*.2,.14,.035,.11,'#c7c5b6')
        d.box(1.2,1.2+.18*math.sin(phase),.4,.4,.4,.4,'#c6b18c',.5*math.sin(phase))
    elif key=='codeforces':
        for i,height in enumerate([.55,1.1,.75]):
            d.box(-.8+i*.8,height/2,0,.57,height,.6,['#9bab8d','#b3a0c7','#d4bb8c'][i])
            d.sphere(-.8+i*.8,height+.31+.12*math.sin(phase+i),0,.16,.16,.16,'#e2d6bc')
        # Sculpture only: there are no ratings, ranks or chart values.
        d.rod((-.9,1.55,-.5),(.9,1.55,-.5),.035,'#a4b7a1')
    elif key=='gfg':
        nodes=[(0,1.85,-.2),(-.8,1.05,0),(.8,1.05,0),(-1.1,.4,.25),(-.5,.4,.25),(.5,.4,.25),(1.1,.4,.25)]
        for a,b in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]:d.rod(nodes[a],nodes[b],.035,'#a9b69e')
        for i,p in enumerate(nodes):
            d.sphere(*p,.16+.025*math.sin(phase-i),.16+.025*math.sin(phase-i),.16,['#b3c29b','#b3a3c5'][i%2])
    else:
        for row in range(2):
            for col in range(2):
                for level in range(2):
                    lift=.15*(1+math.sin(phase+col*math.pi+row*math.pi)) if level else 0
                    d.box((col-.5)*.68,.34+level*.72+lift,(row-.5)*.68,.59,.59,.59,['#baa5ce','#a6b898','#d2ba8d'][(row+col+level)%3],.08*math.sin(phase))
    d.draw()
    c.line([(27,295),(513,295)])
    c.text(27,326,'Open my profile',14)
    arrow(c,510,312,12)
    return c.finish()


def playground_frame(phase,mobile=False):
    w,h=(640,735) if mobile else (1080,500)
    c=Canvas(w,h)
    c.text(34,44,'THE LEARNING PLAYGROUND',12,MUTED)
    c.text(32,116,'Small steps.',48,bold=True)
    c.text(32,174,'New ideas.',48,bold=True)
    c.text(34,219,'Try something. Take it apart.',16,MUTED)
    c.text(34,246,'Find another way.',16,MUTED)
    d=Diorama(c,320 if mobile else 778,537 if mobile else 310,62 if mobile else 65)
    d.floor(5.5,4.2)
    # A robot builds playful structures at a miniature workbench.
    d.box(.8,1.05,-.6,2.8,.14,1.55,'#c9b58f')
    for x in [-.35,1.95]:
        for z in [-1.15,-.03]:d.box(x,.48,z,.09,.98,.09,'#4f5b50')
    d.robot(-.9,.85,phase)
    for i in range(4):
        a=phase+i*TAU/4
        d.box(.8+.65*math.cos(a),1.95+.28*math.sin(a*2),-.55+.5*math.sin(a),.43,.43,.43,['#a8b993','#c2a4d1','#d7b983','#92b6b4'][i],a)
    # Articulating desk lamp and pinboard.
    d.box(-1.5,.07,-.9,.7,.09,.5,'#454b43')
    d.rod((-1.5,.12,-.9),(-1.65,1.6,-.9),.045,'#97a884')
    end=(-1.1+.09*math.sin(phase),2.18,-.9)
    d.rod((-1.65,1.6,-.9),end,.045,'#97a884')
    d.sphere(*end,.26,.12,.2,'#d8c7a2')
    d.box(.1,2.2,-1.8,2.65,1.35,.1,'#454838')
    for i in range(4):
        d.box(-.65+(i%2)*1.0,2.5-(i//2)*.6,-1.73,.7,.4,.015,['#b1a0c7','#b9c59f','#cdb78c','#a2b8b0'][i])
    d.plant(2.1,1.1)
    for i in range(3):d.box(.1+i*.38,.2,1.2,.27,.34,.27,'#ad9dc2',.2*math.sin(phase+i))
    d.draw()
    c.line([(34,h-60),(w-34,h-60)])
    c.text(34,h-30,'CURIOSITY IS A GOOD PLACE TO START.',11,MUTED)
    return c.finish()


def render(name,draw,preview=False):
    still=draw(0)
    still.save(OUT/(name+'-static.png'),optimize=True)
    if preview:return
    frames=[draw(i/50*TAU) for i in range(50)]
    sample=Image.new('RGB',(still.width,still.height*4))
    for i,index in enumerate([0,12,25,37]):sample.paste(frames[index],(0,i*still.height))
    palette=sample.quantize(colors=192,method=Image.Quantize.MEDIANCUT)
    quantized=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    dest=OUT/(name+'.gif')
    quantized[0].save(dest,save_all=True,append_images=quantized[1:],duration=120,loop=0,optimize=True,disposal=1)
    print(name,round(dest.stat().st_size/1024),'KB',flush=True)


def main(preview=False):
    for mobile in [False,True]:
        suffix='-mobile' if mobile else ''
        render('portfolio-portal'+suffix+'-v12',lambda t:portfolio_frame(t,mobile),preview)
        render('learning-playground'+suffix+'-v12',lambda t:playground_frame(t,mobile),preview)
    for key in PLATFORMS:render('practice-'+key+'-v12',lambda t:practice_frame(key,t),preview)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true')
    main(parser.parse_args().preview)
