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
    data={'source':'Unauthenticated public GitHub contribution calendar and public repository API','as_of':today.isoformat(),'public_contributions_365_days':total,'public_repositories':user['public_repos'],'original_repository_languages':languages}
    from visuals import activity
    from animate_activity import render_animations
    render_animations(days,data)
    (ROOT/'assets/activity-calendar.json').write_text(json.dumps({d.isoformat():v for d,v in sorted(days.items())},indent=2)+'\n')
    return activity(days,data,False),activity(days,data,True),data

def main():
    user=json.loads(fetch('https://api.github.com/users/'+USER,True));repos=json.loads(fetch('https://api.github.com/users/'+USER+'/repos?per_page=100',True));html=fetch('https://github.com/users/'+USER+'/contributions')
    desktop,mobile,data=render(user,repos,html);(ROOT/'assets/activity-v8.svg').write_text(desktop);(ROOT/'assets/activity-mobile-v8.svg').write_text(mobile);(ROOT/'assets/activity-data.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
if __name__=='__main__':main()
