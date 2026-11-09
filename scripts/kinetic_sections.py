"""Original perspective-rendered 3D loops for GitHub's image-only profile surface.

No browser, external image service, or simulated statistics. Rendered geometry
loops; verified counts remain fixed and come from coding-data.json.
"""
from pathlib import Path
from functools import lru_cache
import argparse
import colorsys
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
BG = '#0b0b0b'
FG = '#eee9df'
MUTED = '#a9a59d'
LINE = '#30302e'
TAU = math.tau
SCALE = 2


@lru_cache(maxsize=80)
def font(size, bold=False):
    return ImageFont.truetype(str(OUT / 'fonts' / ('manrope-bold.ttf' if bold else 'manrope-regular.ttf')), size * SCALE)


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new('RGB', (w * SCALE, h * SCALE), BG)
        self.d = ImageDraw.Draw(self.im)
        self.d.rounded_rectangle((1, 1, w*SCALE-2, h*SCALE-2), radius=24*SCALE, outline=LINE, width=2)

    def text(self, x, y, value, size=16, color=FG, bold=False, anchor='ls'):
        self.d.text((x*SCALE, y*SCALE), str(value), font=font(size, bold), fill=color, anchor=anchor)

    def line(self, points, fill=LINE, width=1):
        self.d.line([(int(x*SCALE), int(y*SCALE)) for x, y in points], fill=fill, width=max(1, int(width*SCALE)))

    def poly(self, points, fill, outline=None):
        self.d.polygon([(int(x*SCALE), int(y*SCALE)) for x, y in points], fill=fill)
        if outline:
            self.line(points + [points[0]], outline, .6)

    def shadow(self, x, y, rx, ry):
        layer = Image.new('RGB', self.im.size, BG)
        draw = ImageDraw.Draw(layer)
        draw.ellipse(((x-rx)*SCALE, (y-ry)*SCALE, (x+rx)*SCALE, (y+ry)*SCALE), fill='#29251f')
        layer = layer.filter(ImageFilter.GaussianBlur(12*SCALE))
        self.im = Image.composite(layer, self.im, layer.convert('L'))
        self.d = ImageDraw.Draw(self.im)

    def finish(self):
        return self.im.resize((self.w, self.h), Image.Resampling.LANCZOS)


def rotate(p, ax=0, ay=0, az=0):
    x, y, z = p
    y, z = y*math.cos(ax)-z*math.sin(ax), y*math.sin(ax)+z*math.cos(ax)
    x, z = x*math.cos(ay)+z*math.sin(ay), -x*math.sin(ay)+z*math.cos(ay)
    return (x*math.cos(az)-y*math.sin(az), x*math.sin(az)+y*math.cos(az), z)


def project(p, cx, cy, zoom=1):
    x, y, z = p
    factor = 700 / (700-z)
    return (cx+x*factor*zoom, cy+y*factor*zoom)


def material(normal, depth, hue=.12):
    # A subdued pearl metal: directional light and a shifting spectral edge.
    light = max(0, normal[0]*-.35 + normal[1]*-.65 + normal[2]*.68)
    brightness = .19 + .63*light
    spectral = (hue + normal[0]*.14 + normal[1]*.1) % 1
    return tuple(round(c*255) for c in colorsys.hsv_to_rgb(spectral, .11+.18*(1-light), brightness))


def mesh(canvas, vertices, faces, cx, cy, zoom=1, hue=.12):
    visible = []
    for face in faces:
        pts = [vertices[i] for i in face]
        a, b, c = pts[:3]
        u, v = tuple(b[i]-a[i] for i in range(3)), tuple(c[i]-a[i] for i in range(3))
        n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        length = math.sqrt(sum(t*t for t in n)) or 1
        n = tuple(t/length for t in n)
        if n[2] < 0:
            continue
        depth = sum(p[2] for p in pts)/len(pts)
        visible.append((depth, pts, material(n, depth, hue)))
    for _, pts, color in sorted(visible, key=lambda f:f[0]):
        canvas.poly([project(p,cx,cy,zoom) for p in pts], color)


def torus(canvas, cx, cy, radius, phase, tilt=.6, hue=.12, zoom=1):
    vertices, faces = [], []
    segments, sides = 64, 16
    for i in range(segments):
        u = i/segments*TAU
        # Twisted asymmetric tube gives the sculpture an articulated silhouette.
        for j in range(sides):
            v = j/sides*TAU
            tube = radius*.17*(1+.15*math.cos(u*3+phase))
            p = ((radius+tube*math.cos(v))*math.cos(u), (radius+tube*math.cos(v))*math.sin(u), tube*math.sin(v))
            vertices.append(rotate(p, tilt+.18*math.sin(phase), phase, .25*math.sin(phase)))
    for i in range(segments):
        for j in range(sides):
            faces.append((i*sides+j, ((i+1)%segments)*sides+j, ((i+1)%segments)*sides+(j+1)%sides, i*sides+(j+1)%sides))
    mesh(canvas,vertices,faces,cx,cy,zoom,hue)


def cube(canvas, cx, cy, size, phase, zoom=1, hue=.12):
    vertices = [rotate((x*size,y*size,z*size), .4+.25*math.sin(phase), phase, -.25) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    faces = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(1,2,6,5),(0,4,7,3)]
    mesh(canvas,vertices,faces,cx,cy,zoom,hue)


def orbit_line(canvas,cx,cy,rx,ry,phase):
    points = [(cx+rx*math.cos(i/100*TAU),cy+ry*math.sin(i/100*TAU)) for i in range(101)]
    canvas.line(points,'#35322d')
    for i in range(4):
        t=phase+i*TAU/4
        x,y=cx+rx*math.cos(t),cy+ry*math.sin(t)
        canvas.d.ellipse(((x-2)*SCALE,(y-2)*SCALE,(x+2)*SCALE,(y+2)*SCALE),fill='#d1c7b1')


def projects_frame(data, phase, mobile=False):
    w,h=(640,1060) if mobile else (1080,650)
    c=Canvas(w,h)
    c.text(34,43,'SELECTED WORK / SIX EXPLORATIONS',12,MUTED)
    c.text(32,112,'Built from',52 if mobile else 60,bold=True)
    c.text(32,177,'curiosity.',52 if mobile else 60,bold=True)
    c.text(34,215,'Personal ideas. Shared work. Things that move.',16,MUTED)
    cx,cy=(320,423) if mobile else (302,421)
    c.shadow(cx,cy+122,145,18)
    orbit_line(c,cx,cy+12,235,79,phase)
    orbit_line(c,cx,cy+12,191,109,-phase*.5)
    # Six project satellites orbit an actual rotating 3D core.
    bodies=[]
    for i in range(6):
        a=phase+i*TAU/6
        x,y=cx+223*math.cos(a),cy+76*math.sin(a)
        bodies.append((math.sin(a),x,y,i))
    def satellite(item):
        depth,x,y,i=item
        k=.78+(depth+1)*.12
        cube(c,x,y,22,phase+i*.7,k,.11+i*.035)
        c.text(x,y+54*k,f'{i+1:02}',14,'#ccc4b3',anchor='ms')
    for item in sorted(bodies):
        if item[0]<0:satellite(item)
    torus(c,cx,cy-10,80,phase,.6,.13)
    cube(c,cx,cy-10,24,-phase,.9,.12)
    for item in sorted(bodies):
        if item[0]>=0:satellite(item)
    c.text(cx,cy+160,'IDEA / EXPERIMENT / BUILD',12,MUTED,anchor='ms')
    x,y=(34,656) if mobile else (630,151)
    row=56 if mobile else 68
    for i,p in enumerate(data):
        top=y+i*row
        c.line([(x,top-26),(w-34,top-26)])
        c.text(x,top,f'{i+1:02}',13,MUTED)
        c.text(x+36,top,p['title'],23 if mobile else 22,bold=True)
        c.text(x+36,top+21,p['context'].upper(),10,MUTED)
        c.line([(w-48,top),(w-36,top-12)],FG,1.4)
        c.line([(w-47,top-12),(w-36,top-12),(w-36,top-1)],FG,1.4)
    c.line([(34,h-55),(w-34,h-55)])
    c.text(34,h-27,'SIX PROJECTS. ONE ONGOING PRACTICE.',11,MUTED)
    c.text(w-34,h-27,'OPEN THE REPOSITORIES BELOW',10,MUTED,anchor='rs')
    return c.finish()


PLATFORMS=[('leetcode','LeetCode'),('codeforces','Codeforces'),('gfg','GeeksforGeeks'),('bruteforce','BruteForce')]


def coding_frame(data,phase,mobile=False):
    w,h=(640,920) if mobile else (1080,520)
    c=Canvas(w,h)
    c.text(34,43,'PROBLEM SOLVING / AN ONGOING PRACTICE',12,MUTED)
    if mobile:
        c.text(32,99,'Think. Try.',43,bold=True)
        c.text(32,153,'Understand.',43,bold=True)
    else:
        c.text(32,105,'Think. Try. Understand.',45,bold=True)
    c.text(34,194 if mobile else 140,'A little more understanding with every problem.',16,MUTED)
    for i,(key,name) in enumerate(PLATFORMS):
        d=data.get(key,{})
        x=(174+(i%2)*292) if mobile else (153+i*259)
        y=(300+(i//2)*310) if mobile else 260
        t=phase+i*TAU/4
        lift=8*math.sin(t)
        c.shadow(x,y+54,70,9)
        # Decorative metal rings rotate independently of the fixed statistics.
        torus(c,x,y-8+lift,53,t,.65+i*.14,.10+i*.025)
        cube(c,x,y-8+lift,13,-t,1,.12)
        c.text(x,y+121,d.get('solved','—'),48,bold=True,anchor='ms')
        c.text(x,y+149,name,18,bold=True,anchor='ms')
        c.text(x,y+172,'PROBLEMS SOLVED',10,MUTED,anchor='ms')
        c.text(x,y+194,'VERIFIED '+d.get('as_of','UNAVAILABLE'),10,MUTED,anchor='ms')
    c.line([(34,h-52),(w-34,h-52)])
    c.text(34,h-27,'SEPARATE PLATFORM COUNTS · PUBLIC DATA',10,MUTED)
    c.text(w-34,h-27,'REFRESHED DAILY',10,MUTED,anchor='rs')
    return c.finish()


def package(kind, data, mobile=False, preview=False):
    draw = projects_frame if kind=='projects' else coding_frame
    name=kind+('-mobile' if mobile else '')+'-kinetic-v11'
    still=draw(data,0,mobile)
    still.save(OUT/(name+'-static.png'),optimize=True)
    if preview:return
    frames=[draw(data,i/60*TAU,mobile) for i in range(60)]
    # Shared palette keeps stationary labels stable throughout the loop.
    sample=Image.new('RGB',(frames[0].width,frames[0].height*4))
    for i,f in enumerate([frames[0],frames[15],frames[30],frames[45]]):sample.paste(f,(0,i*f.height))
    palette=sample.quantize(colors=192,method=Image.Quantize.MEDIANCUT)
    images=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    path=OUT/(name+'.gif')
    images[0].save(path,save_all=True,append_images=images[1:],duration=100,loop=0,optimize=True,disposal=1)
    print(path.name,round(path.stat().st_size/1024),'KB',flush=True)


def render(kind='all', preview=False):
    for key in ['projects','coding'] if kind=='all' else [kind]:
        source=ROOT/'scripts/project-data.json' if key=='projects' else OUT/'coding-data.json'
        data=json.loads(source.read_text())
        for mobile in [False,True]:package(key,data,mobile,preview)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('kind',choices=['all','projects','coding'],nargs='?',default='all')
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args()
    render(args.kind,args.preview)
