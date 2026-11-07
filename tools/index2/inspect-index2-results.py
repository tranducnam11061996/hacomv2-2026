from pathlib import Path
import json,collections
root=Path(__file__).resolve().parents[2]
def values(path):
    out=[]
    for r in json.loads((root/path).read_text(encoding='utf-8')):
        for block in r.get('result',{}).get('content',[]):
            s=block.get('text','')
            if '```json\n' in s:
                out.append(json.JSONDecoder().raw_decode(s.split('```json\n')[1].lstrip())[0])
    return out
if __name__=='__main__':
    import re
    print(collections.Counter(re.findall(r'data-action="([^"]*)',(root/'index2.html').read_text(encoding='utf-8'))).most_common(12))
    rows=[r for r in values('reference/index2-matrix-results.json') if 'sections' in r]
    for a,b in zip(rows[::2],rows[1::2]):
        print(a['width'],'height',a['height'],b['height'],'overflow',b['overflow'],'diffs',[(x['number'],round(y['height']-x['height'],2))for x,y in zip(a['sections'],b['sections']) if abs(y['height']-x['height'])>.1])
