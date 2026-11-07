from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[2];temp=Path('C:/Users/ADMIN/AppData/Local/Temp')
sections=json.loads((root/'reference/index2-mobile-heights.json').read_text())
for label in ['before','after']:
    for section in sections:
        n=section['number'];h=round(section['height']);image=Image.new('RGB',(390,h),'white')
        for tile,offset in enumerate(range(0,h,1080)):
            path=temp/f'index2-390-{label}-{n:02}-{tile:02}.png'
            part=Image.open(path).convert('RGB');image.paste(part.crop((0,0,390,min(1080,h-offset))),(0,offset))
        image.save(temp/f'index2-390-{label}-{n:02}.png')
values=[{'result':{'content':[{'text':'```json\n'+json.dumps({'number':s['number'],'height':s['height']})+'\n```'}]}} for s in sections]
(root/'reference/index2-capture-390-results.json').write_text(json.dumps(values),encoding='utf-8')
print('Stitched 44 mobile section screenshots')
