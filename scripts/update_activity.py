#!/usr/bin/env python3
"""Render a self-hosted activity card from public GitHub data only."""
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json, os, re, urllib.request, ssl
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
USER='shivanshushukla2602-hash'
CTX=ssl.create_default_context(cafile='/etc/ssl/cert.pem') if Path('/etc/ssl/cert.pem').exists() else ssl.create_default_context()
def fetch(url,api=False):
    headers={'User-Agent':'ShivAndShu-Profile','Accept':'application/vnd.github+json' if api else 'text/html'}
    token=os.environ.get('GITHUB_TOKEN')
    if api and token: headers['Authorization']='Bearer '+token
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),context=CTX,timeout=30) as r:return r.read().decode()
class Calendar(HTMLParser):
    def __init__(self):super().__init__();self.cells={};self.tips={};self.current=None
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='td' and 'data-date' in a:self.cells[a['id']]={'date':a['data-date'],'level':int(a.get('data-level',0))}
        if t=='tool-tip':self.current=a.get('for');self.tips[self.current]=''
    def handle_data(self,data):
        if self.current:self.tips[self.current]+=data
    def handle_endtag(self,t):
        if t=='tool-tip':self.current=None

def render(user,repos,html):
    cal=Calendar();cal.feed(html);today=date.today();start=today-timedelta(days=364)
    days={}
    for key,cell in cal.cells.items():
        tip=cal.tips.get(key,'').strip();m=re.match(r'([\d,]+) contributions?\b',tip)
        count=int(m.group(1).replace(',','')) if m else 0
        if not m and not tip.startswith('No contributions'):raise ValueError('Unknown public contribution tooltip; preserve the prior card.')
        d=date.fromisoformat(cell['date'])
        if start<=d<=today:days[d]={'count':count,'level':cell['level']}
    if len(days)<350:raise ValueError('Incomplete public contribution calendar; preserve the prior card.')
    total=sum(d['count'] for d in days.values())
    languages=sorted({r['language'] for r in repos if not r['fork'] and r.get('language')})
    e=escape
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="392" viewBox="0 0 1200 392" role="img" aria-labelledby="title desc">',f'<title id="title">Shivanshu’s public GitHub activity</title><desc id="desc">{total} publicly visible contributions over the trailing 365 days, {user["public_repos"]} public repositories, {len(languages)} languages across original public repositories. Calendar fetched from the unauthenticated public GitHub contribution page.</desc>','<rect x="1" y="1" width="1198" height="390" rx="20" fill="#111210" stroke="#45483c"/>','<text x="40" y="48" font-family="Arial,sans-serif" font-size="11" letter-spacing="3" fill="#b0b6a7">THE PUBLIC SIGNAL</text>','<text x="40" y="97" font-family="Georgia,serif" font-style="italic" font-size="34" fill="#eee2c6">Small commits. Real progress.</text>']
    for x,value,label in [(680,total,'PUBLIC CONTRIBUTIONS'),(870,user['public_repos'],'PUBLIC REPOSITORIES'),(1060,len(languages),'LANGUAGES')]:
        svg.append(f'<text x="{x}" y="75" font-family="Arial,sans-serif" font-weight="bold" font-size="34" fill="#f5f4ef">{value}</text><text x="{x}" y="98" font-family="Arial,sans-serif" font-size="8" letter-spacing="1" fill="#aeb4a6">{label}</text>')
    base=start-timedelta(days=(start.weekday()+1)%7);colors=['#252821','#625e4a','#9d916d','#c9b984','#eee2c6']
    for d,item in sorted(days.items()):
        offset=(d-base).days;col,row=divmod(offset,7);x=70+col*20;y=151+row*21
        svg.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="4" fill="{colors[min(4,item["level"])]}"><title>{d.isoformat()}: {item["count"]} public contributions</title></rect>')
    svg.extend(['<path d="M46 322H1154" stroke="#393e31"/>',f'<text x="40" y="355" font-family="Arial,sans-serif" font-size="10" fill="#aeb4a6">PUBLIC GITHUB CALENDAR · TRAILING 365 DAYS · {today.isoformat()}</text>',f'<text x="1160" y="355" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="#d2d7c6">{e(" · ".join(languages))}</text>','</svg>'])
    return ''.join(svg),{'source':'Unauthenticated public GitHub contribution calendar and public repository API','as_of':today.isoformat(),'public_contributions_365_days':total,'public_repositories':user['public_repos'],'original_repository_languages':languages}
def mobile(svg,data):
    root=ET.fromstring(svg);ns={'s':'http://www.w3.org/2000/svg'}
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="400" height="370" viewBox="0 0 400 370" role="img" aria-labelledby="title desc"><title id="title">Public GitHub activity</title><desc id="desc">Verified public contribution calendar and repository statistics.</desc><rect x="1" y="1" width="398" height="368" rx="16" fill="#111210" stroke="#45483c"/>','<text x="22" y="34" font-family="Arial,sans-serif" font-size="9" letter-spacing="1.5" fill="#b0b6a7">THE PUBLIC SIGNAL</text><text x="22" y="73" font-family="Georgia,serif" font-style="italic" font-size="28" fill="#eee2c6">Small commits.</text><text x="22" y="108" font-family="Georgia,serif" font-style="italic" font-size="28" fill="#eee2c6">Real progress.</text>']
    for x,v,label in [(22,data['public_contributions_365_days'],'CONTRIBUTIONS'),(157,data['public_repositories'],'PUBLIC REPOS'),(290,len(data['original_repository_languages']),'LANGUAGES')]:
        parts.append(f'<text x="{x}" y="160" font-family="Arial,sans-serif" font-size="32" font-weight="bold" fill="#f5f4ef">{v}</text><text x="{x}" y="181" font-family="Arial,sans-serif" font-size="8" fill="#b0b6a7">{label}</text>')
    for rect in root.findall('s:rect',ns):
        title=rect.find('s:title',ns)
        if title is None:continue
        x=25+(float(rect.attrib['x'])-70)/20*6.6;y=215+(float(rect.attrib['y'])-151)/21*9
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="4.8" height="6" rx="1.4" fill="{rect.attrib["fill"]}"><title>{escape(title.text)}</title></rect>')
    parts.append('<path d="M22 302H378" stroke="#393e31"/>')
    parts.append(f'<text x="22" y="326" font-family="Arial,sans-serif" font-size="9" fill="#b0b6a7">PUBLIC CALENDAR · TRAILING 365 DAYS · {data["as_of"]}</text>')
    parts.append(f'<text x="22" y="348" font-family="Arial,sans-serif" font-size="9" fill="#d2d7c6">{escape(" · ".join(data["original_repository_languages"]))}</text></svg>')
    return ''.join(parts)

def main():
    user=json.loads(fetch('https://api.github.com/users/'+USER,True));repos=json.loads(fetch('https://api.github.com/users/'+USER+'/repos?per_page=100',True));html=fetch('https://github.com/users/'+USER+'/contributions')
    svg,data=render(user,repos,html);(ROOT/'assets/activity.svg').write_text(svg);(ROOT/'assets/activity-mobile.svg').write_text(mobile(svg,data));(ROOT/'assets/activity-data.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
if __name__=='__main__':main()
