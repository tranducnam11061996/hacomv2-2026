from pathlib import Path
from PIL import Image,ImageChops,ImageStat,ImageEnhance,ImageDraw
import json,math,sys
root=Path(__file__).resolve().parents[2]
temp=Path('C:/Users/ADMIN/AppData/Local/Temp')
source=json.loads((root/'reference/index2-desktop-source.json').read_text(encoding='utf-8'))
def parse(path):
    out=[]
    for r in json.loads(path.read_text(encoding='utf-8')):
        for c in r.get('result',{}).get('content',[]):
            s=c.get('text','')
            if '```json\n' in s:
                data=json.JSONDecoder().raw_decode(s.split('```json\n')[1].lstrip())[0]
                if isinstance(data,dict) and 'height' in data and 'number' in data:out.append(data)
    return out
widths=[int(sys.argv[1])] if len(sys.argv)>1 else [1920,390]
selected_sections={int(s) for s in sys.argv[2:]}
report=[]
if len(widths)==1 and (root/'reference/index2-visual-results.json').exists():report=[r for r in json.loads((root/'reference/index2-visual-results.json').read_text())if r['width']not in widths or (selected_sections and r['section']not in selected_sections)]
for width in widths:
    meta_path=root/f'reference/index2-capture-{width}-results.json'
    if width==1920:
        heights={s['number']:s['height'] for s in source}
    else:
        if not meta_path.exists():continue
        values=parse(meta_path);heights={d['number']:d['height'] for d in values}
    out=root/f'reference/index2-visual/{width}';out.mkdir(parents=True,exist_ok=True)
    thumbs=[]
    for n,h in heights.items():
        if selected_sections and n not in selected_sections:continue
        before_path=temp/f'index2-{width}-before-{n:02}.png';after_path=temp/f'index2-{width}-after-{n:02}.png'
        if not before_path.exists() or not after_path.exists():continue
        before=Image.open(before_path).convert('RGB').crop((0,0,width,round(h)))
        after=Image.open(after_path).convert('RGB').crop((0,0,width,round(h)))
        diff=ImageChops.difference(before,after)
        mean=sum(ImageStat.Stat(diff).mean)/3
        gray=diff.convert('L');hist=gray.histogram();fraction=sum(hist[17:])/(width*round(h))
        report.append({'width':width,'section':n,'height':h,'meanAbsoluteError':round(mean,5),'changedOver16Percent':round(fraction*100,4),'pixelIdentical':diff.getbbox() is None})
        before.save(out/f'before-{n:02}.webp',lossless=True,method=3)
        after.save(out/f'after-{n:02}.webp',lossless=True,method=3)
        overlay=Image.blend(before,after,.5);overlay.save(out/f'overlay-{n:02}.webp',lossless=True,method=3)
        diff.save(out/f'diff-{n:02}.webp',lossless=True,method=3)
        # Three columns per section: before / after / amplified difference.
        w=250 if width==390 else 400;th=round(h*w/width)
        panel=Image.new('RGB',(w*3,th+28),'white');draw=ImageDraw.Draw(panel)
        for i,(label,im) in enumerate([('BEFORE',before),('AFTER',after),('DIFF x3',ImageEnhance.Brightness(diff).enhance(3))]):
            draw.text((i*w+8,8),f'{n:02} {label}',fill='black');panel.paste(im.resize((w,th)),(i*w,28))
        thumbs.append(panel)
    if thumbs and not selected_sections:
        contact=Image.new('RGB',(thumbs[0].width,sum(t.height for t in thumbs)), '#dddddd');y=0
        for t in thumbs:contact.paste(t,(0,y));y+=t.height
        contact.save(out/'comparison.jpg',quality=90)
(root/'reference/index2-visual-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Compared',len(report),'section pairs')
print(sorted(report,key=lambda r:r['meanAbsoluteError'],reverse=True)[:8])
