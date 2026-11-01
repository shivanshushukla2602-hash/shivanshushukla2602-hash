#!/usr/bin/env python3
"""Create self-hosted coding cards from the owner's supplied public profile links."""
from pathlib import Path
from datetime import date
from html import escape,unescape
from concurrent.futures import ThreadPoolExecutor
import json,re,ssl,urllib.request,textwrap
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets';CACHE=OUT/'coding-data.json'
CTX=ssl.create_default_context(cafile='/etc/ssl/cert.pem') if Path('/etc/ssl/cert.pem').exists() else ssl.create_default_context()
URLS={'leetcode':'https://leetcode.com/u/Shivanshu_19/','codeforces':'https://codeforces.com/profile/shivanshu_19','gfg':'https://www.geeksforgeeks.org/profile/shivanshu19?tab=activity','bruteforce':'https://bruteforce.pwioi.com/profile/shivanshu_19'}
def get(url,data=None):
 h={'User-Agent':'Mozilla/5.0 (compatible; ShivAndShu-PublicProfile/1.0)'}
 if data is not None:h['Content-Type']='application/json'
 req=urllib.request.Request(url,headers=h,data=json.dumps(data).encode() if data is not None else None)
 with urllib.request.urlopen(req,context=CTX,timeout=25) as r:return r.read().decode()
def normalized(raw):
 s=unescape(raw)
 for _ in range(5):s=s.replace('\\"','"')
 return s
def extract_number(s,key):
 m=re.search('"'+re.escape(key)+'"\\s*:\\s*(\\d+)',s)
 if not m:raise ValueError('Public stat not found: '+key)
 return int(m.group(1))
def fetch(key):
 if key=='leetcode':
  d=json.loads(get('https://leetcode.com/graphql/',{'query':'query { matchedUser(username: "Shivanshu_19") { username submitStatsGlobal { acSubmissionNum { difficulty count } } } }'}))['data']['matchedUser']
  if d['username'].lower()!='shivanshu_19':raise ValueError('Profile identity mismatch')
  counts={r['difficulty']:r['count'] for r in d['submitStatsGlobal']['acSubmissionNum']}
  return {'solved':counts['All'],'breakdown':{k.lower():counts[k] for k in ['Easy','Medium','Hard']},'source':'https://leetcode.com/graphql/'}
 if key=='codeforces':
  d=json.loads(get('https://codeforces.com/api/user.status?handle=shivanshu_19'))
  if d['status']!='OK':raise ValueError('Codeforces did not return OK')
  subs=d['result'];solved={}
  for r in subs:
   if r.get('verdict')=='OK':
    problem=r['problem'];solved[(problem.get('contestId'),problem['index'])]=problem
  distribution={}
  for problem in solved.values():
   rating=str(problem.get('rating','unrated'));distribution[rating]=distribution.get(rating,0)+1
  return {'solved':len(solved),'submissions':len(subs),'rating_distribution':distribution,'source':'https://codeforces.com/api/user.status?handle=shivanshu_19'}
 s=normalized(get(URLS[key]))
 if ('shivanshu19' if key=='gfg' else 'shivanshu_19') not in s.lower():raise ValueError('Public profile identity not found')
 if key=='gfg':
  n=s.index('"total_problems_solved"');region=s[max(0,n-120):n+100]
  return {'solved':extract_number(region,'total_problems_solved'),'score':extract_number(region,'score'),'source':URLS[key]}
 m=re.search(r'"codingStats"\s*:\s*',s)
 if not m:raise ValueError('BruteForce public codingStats not found')
 d,_=json.JSONDecoder().raw_decode(s[m.end():])
 return {'solved':d['totalSolved'],'breakdown':{k:d[k]['solved'] for k in ['easy','medium','hard']},'source':URLS[key]}
from visuals import coding_card
from verified_coding_charts import render as render_verified_chart, overview as render_overview

def render(key,data):return coding_card(key,data,False)
def render_mobile(key,data):return coding_card(key,data,True)

def main():
 cache=json.loads(CACHE.read_text()) if CACHE.exists() else {}
 def one(key):
  try:
   d=fetch(key);d.update({'as_of':date.today().isoformat(),'profile':URLS[key]});return key,d,None
  except Exception as ex:return key,cache.get(key,{'profile':URLS[key]}),type(ex).__name__
 with ThreadPoolExecutor(max_workers=4) as pool:
  for key,data,error in pool.map(one,URLS):
   cache[key]=data;(OUT/f'coding-{key}-v8.svg').write_text(render(key,data));(OUT/f'coding-{key}-mobile-v8.svg').write_text(render_mobile(key,data));print(json.dumps({'platform':key,'solved':data.get('solved'),'verified_on':data.get('as_of'),'refresh_error':error}))
 for key in ['leetcode','codeforces']:
  (OUT/f'coding-{key}-chart-v1.svg').write_text(render_verified_chart(key,cache[key]))
 for mobile in [False,True]:
  suffix='-mobile' if mobile else ''
  (OUT/f'coding-overview{suffix}-v1.svg').write_text(render_overview(cache,mobile))
 CACHE.write_text(json.dumps(cache,indent=2)+'\n')
 readme=ROOT/'README.md'
 if readme.exists():
  text=readme.read_text();rows=[]
  overview_label='Verified solved totals: '+', '.join(k+' '+str(cache.get(k,{}).get('solved','unavailable')) for k in ['leetcode','codeforces','gfg','bruteforce'])+'. Separate platform counts, refreshed daily.'
  text=re.sub(r'(<img src="assets/coding-overview-v1\.svg" alt=")[^"]*',lambda m:m.group(1)+escape(overview_label,quote=True),text)
  names={'leetcode':'LeetCode','codeforces':'Codeforces','gfg':'GeeksforGeeks','bruteforce':'PW IOI BruteForce'}
  for key,d in cache.items():
   if 'solved' not in d:continue
   label=names[key]+' — '+str(d['solved'])+' problems solved; publicly verified '+d['as_of']+'. Open my profile.'
   text=re.sub(r'(<img src="assets/coding-'+key+r'-v8\.svg(?:\?[^" ]*)?" alt=")[^"]*',lambda m:m.group(1)+escape(label,quote=True),text)
   if key in ['leetcode','codeforces']:
    text=re.sub(r'(<img src="assets/coding-'+key+r'-chart-v1\.svg" alt=")[^"]*',lambda m:m.group(1)+escape(label+' Verified-data chart, not a platform screenshot.',quote=True),text)
   rows.append('| ['+names[key]+']('+URLS[key]+') | '+str(d['solved'])+' | '+d['as_of']+' |')
  table='<!-- CODING-STATS:START -->\n<details>\n<summary><strong>View verified statistics</strong></summary>\n\n| Platform | Problems solved | Verified |\n| --- | --- | --- |\n'+'\n'.join(rows)+'\n\n</details>\n<!-- CODING-STATS:END -->'
  text=re.sub(r'<!-- CODING-STATS:START -->.*?<!-- CODING-STATS:END -->',lambda _:table,text,flags=re.S);readme.write_text(text)

if __name__=='__main__':main()
