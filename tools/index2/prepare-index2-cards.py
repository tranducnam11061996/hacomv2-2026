from pathlib import Path
import json,math
from PIL import Image
root=Path(__file__).resolve().parents[2]
def data(path,index):
    s=json.loads((root/path).read_text(encoding='utf-8'))[index]['result']['content'][0]['text']
    return json.loads(s.split('```json\n')[1].rsplit('```',1)[0])
cards=data('reference/index2-original-inspect-result.json',1)['cards']
cards+=data('reference/index2-video-inspect-result.json',0)
sources=json.loads((root/'reference/index2-desktop-source.json').read_text(encoding='utf-8'))
for i,c in enumerate(cards):
    s=next(s for s in sources if s['number']==int(c['section']))
    b=c['rect'];x,y=b['x'],b['y']-s['top'];w,h=b['width'],b['height']
    c.update(x=x,y=y,w=w,h=h,image=f'assets/index2/card-{i:02}.webp')
    image=Image.open(root/f'assets/index2/desktop-{s["number"]:02}.webp')
    image.crop((math.floor(x),math.floor(y),math.ceil(x+w),math.ceil(y+h))).save(root/c['image'],lossless=True,method=6)
(root/'reference/index2-cards.json').write_text(json.dumps(cards,ensure_ascii=False),encoding='utf-8')
print('Prepared',len(cards),'carousel items')
