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
  subs=d['result'];solved={(r['problem'].get('contestId'),r['problem']['index']) for r in subs if r.get('verdict')=='OK'}
  return {'solved':len(solved),'submissions':len(subs),'source':'https://codeforces.com/api/user.status?handle=shivanshu_19'}
 s=normalized(get(URLS[key]))
 if ('shivanshu19' if key=='gfg' else 'shivanshu_19') not in s.lower():raise ValueError('Public profile identity not found')
 if key=='gfg':
  n=s.index('"total_problems_solved"');region=s[max(0,n-120):n+100]
  return {'solved':extract_number(region,'total_problems_solved'),'score':extract_number(region,'score'),'source':URLS[key]}
 m=re.search(r'"codingStats"\s*:\s*',s)
 if not m:raise ValueError('BruteForce public codingStats not found')
 d,_=json.JSONDecoder().raw_decode(s[m.end():])
 return {'solved':d['totalSolved'],'breakdown':{k:d[k]['solved'] for k in ['easy','medium','hard']},'source':URLS[key]}
def render(key,data):
 names={'leetcode':('LeetCode','Shivanshu_19','LC'),'codeforces':('Codeforces','shivanshu_19','CF'),'gfg':('GeeksforGeeks','shivanshu19','GFG'),'bruteforce':('PW IOI BruteForce','shivanshu_19','BF')};name,handle,mark=names[key];e=escape
 solved=data.get('solved');value=str(solved) if solved is not None else '↗';label='ACCEPTED PROBLEMS' if key=='codeforces' else 'PROBLEMS SOLVED'
 if solved is None:label='EXPLORE MY PRACTICE'
 if data.get('breakdown'):detail=' · '.join(k.title()+' '+str(v) for k,v in data['breakdown'].items())
 elif 'score' in data:detail='Coding score '+str(data['score'])
 elif key=='codeforces' and solved is not None:detail='Unique problems with an accepted solution'
 else:detail='Open the public profile'
 stamp=data.get('as_of');foot='VERIFIED '+stamp if stamp else 'OPEN PROFILE ↗'
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="220" viewBox="0 0 490 220" role="img" aria-labelledby="title desc"><title id="title">{e(name)} — {e(handle)}</title><desc id="desc">{e(str(solved)+' problems solved. '+detail+'. Public source verified '+str(stamp) if solved is not None else 'Open my public coding profile.')}</desc><style>@media(prefers-reduced-motion:reduce){{.signal{{display:none}}}}</style><rect x="1" y="1" width="488" height="218" rx="16" fill="#151513" stroke="#4d4a3d"/><text x="26" y="36" font-family="Arial,sans-serif" font-size="15" font-weight="bold" fill="#f5f4ef">{e(name)}</text><text x="26" y="58" font-family="Arial,sans-serif" font-size="10" fill="#b5b1a4">@{e(handle)}</text><rect x="407" y="22" width="56" height="38" rx="10" fill="#eee2c60c" stroke="#57513f"/><text x="435" y="46" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#eee2c6">{mark}</text><text x="24" y="126" font-family="Arial,sans-serif" font-size="57" font-weight="bold" fill="#eee2c6">{e(value)}</text><text x="130" y="116" font-family="Arial,sans-serif" font-size="9" letter-spacing="1.1" fill="#b5b1a4">{label}</text><text x="26" y="157" font-family="Arial,sans-serif" font-size="11" fill="#d2cec2">{e(detail)}</text><path d="M26 179H464" stroke="#464236"/><circle class="signal" r="2" fill="#eee2c6"><animateMotion dur="6s" repeatCount="indefinite" path="M26 179H464"/></circle><text x="26" y="201" font-family="Arial,sans-serif" font-size="8" letter-spacing="1" fill="#a6a295">{foot}</text><text x="461" y="202" text-anchor="end" font-family="Arial,sans-serif" font-size="18" fill="#eee2c6">↗</text></svg>'''
def render_mobile(key,data):
    names={'leetcode':('LeetCode','Shivanshu_19'),'codeforces':('Codeforces','shivanshu_19'),'gfg':('GeeksforGeeks','shivanshu19'),'bruteforce':('PW IOI BruteForce','shivanshu_19')};name,handle=names[key];e=escape
    value=str(data['solved']) if 'solved' in data else '↗'
    if data.get('breakdown'):detail=' · '.join(k.title()+' '+str(v) for k,v in data['breakdown'].items())
    elif 'score' in data:detail='Coding score '+str(data['score'])
    else:detail='Unique accepted problems' if key=='codeforces' else 'Open my coding profile'
    label='ACCEPTED PROBLEMS' if key=='codeforces' else 'PROBLEMS SOLVED'
    body=f'<svg xmlns="http://www.w3.org/2000/svg" width="280" height="272" viewBox="0 0 280 272" role="img" aria-labelledby="title"><title id="title">{e(name)}: {e(value)} problems solved</title><rect x="1" y="1" width="278" height="270" rx="14" fill="#151513" stroke="#4d4a3d"/><text x="18" y="35" font-family="Arial,sans-serif" font-size="22" font-weight="bold" fill="#f5f4ef">{e(name)}</text><text x="18" y="58" font-family="Arial,sans-serif" font-size="13" fill="#b5b1a4">@{handle}</text><text x="16" y="130" font-family="Arial,sans-serif" font-size="60" font-weight="bold" fill="#eee2c6">{e(value)}</text><text x="18" y="158" font-family="Arial,sans-serif" font-size="11" fill="#b5b1a4">{label}</text>'
    for j,line in enumerate(textwrap.wrap(detail,29)):body+=f'<text x="18" y="{188+j*20}" font-family="Arial,sans-serif" font-size="13" fill="#d2cec2">{e(line)}</text>'
    stamp=data.get('as_of','OPEN PROFILE');body+=f'<path d="M18 233H262" stroke="#464236"/><text x="18" y="255" font-family="Arial,sans-serif" font-size="10" fill="#a6a295">{stamp}</text><text x="260" y="256" text-anchor="end" font-family="Arial,sans-serif" font-size="22" fill="#eee2c6">↗</text></svg>'
    return body

def main():
 cache=json.loads(CACHE.read_text()) if CACHE.exists() else {}
 def one(key):
  try:
   d=fetch(key);d.update({'as_of':date.today().isoformat(),'profile':URLS[key]});return key,d,None
  except Exception as ex:return key,cache.get(key,{'profile':URLS[key]}),type(ex).__name__
 with ThreadPoolExecutor(max_workers=4) as pool:
  for key,data,error in pool.map(one,URLS):
   cache[key]=data;(OUT/f'coding-{key}.svg').write_text(render(key,data));(OUT/f'coding-{key}-mobile.svg').write_text(render_mobile(key,data));print(json.dumps({'platform':key,'solved':data.get('solved'),'verified_on':data.get('as_of'),'refresh_error':error}))
 CACHE.write_text(json.dumps(cache,indent=2)+'\n')
 readme=ROOT/'README.md'
 if readme.exists():
  text=readme.read_text();rows=[]
  names={'leetcode':'LeetCode','codeforces':'Codeforces','gfg':'GeeksforGeeks','bruteforce':'PW IOI BruteForce'}
  for key,d in cache.items():
   if 'solved' not in d:continue
   label=names[key]+' — '+str(d['solved'])+' problems solved; publicly verified '+d['as_of']+'. Open my profile.'
   text=re.sub(r'(<img src="assets/coding-'+key+r'.svg" alt=")[^"]*',lambda m:m.group(1)+escape(label,quote=True),text)
   rows.append('| ['+names[key]+']('+URLS[key]+') | '+str(d['solved'])+' | '+d['as_of']+' |')
  table='<!-- CODING-STATS:START -->\n<details>\n<summary><strong>Verified statistics — text version</strong></summary>\n\n| Platform | Problems solved | Verified |\n| --- | --- | --- |\n'+'\n'.join(rows)+'\n\n</details>\n<!-- CODING-STATS:END -->'
  text=re.sub(r'<!-- CODING-STATS:START -->.*?<!-- CODING-STATS:END -->',lambda _:table,text,flags=re.S);readme.write_text(text)

if __name__=='__main__':main()
