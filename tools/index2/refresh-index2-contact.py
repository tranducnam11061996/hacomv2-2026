from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance
root=Path(__file__).resolve().parents[2]
for width in [1920,390]:
    folder=root/f'reference/index2-visual/{width}';panels=[];w=400 if width==1920 else 250
    for n in range(1,23):
        before=Image.open(folder/f'before-{n:02}.webp').convert('RGB');after=Image.open(folder/f'after-{n:02}.webp').convert('RGB');diff=Image.open(folder/f'diff-{n:02}.webp').convert('RGB')
        h=round(before.height*w/width);panel=Image.new('RGB',(3*w,h+28),'white');draw=ImageDraw.Draw(panel)
        for i,(label,im)in enumerate([('BEFORE',before),('AFTER',after),('DIFF x3',ImageEnhance.Brightness(diff).enhance(3))]):draw.text((i*w+8,8),f'{n:02} {label}',fill='black');panel.paste(im.resize((w,h)),(i*w,28))
        panels.append(panel)
    out=Image.new('RGB',(3*w,sum(p.height for p in panels)),'#ddd');y=0
    for panel in panels:out.paste(panel,(0,y));y+=panel.height
    out.save(folder/'comparison.jpg',quality=90)
print('Refreshed desktop and mobile contact sheets')
