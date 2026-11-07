from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[2]
sections=json.loads((root/'reference/index2-mobile-heights.json').read_text())
commands=[]
for section in sections:
    n=section['number'];url=f'http://127.0.0.1:8765/index2.html?index2-final-section-{n}'
    commands.append({'name':'emulate','_url':url,'arguments':{'viewport':'390x1080x1'}})
    commands.append({'name':'evaluate_script','_url':url,'arguments':{'function':'''async () => {await document.fonts.ready;const el=document.createElement('div');el.style.height='2000px';document.body.append(el);return {url:location.href};}'''}})
    for tile in range(math.ceil(section['height']/1080)):
        code=f'''async () => {{const s=document.querySelector('[data-section="{n}"]');window.scrollTo(0,s.getBoundingClientRect().top+scrollY+{tile*1080});for(const image of s.querySelectorAll('img'))if(image.checkVisibility()){{image.loading='eager';try{{await Promise.race([image.decode(),new Promise((_,reject)=>setTimeout(reject,2000))])}}catch(e){{}}}}await new Promise(r=>setTimeout(r,100));return {{number:{n},tile:{tile},height:s.getBoundingClientRect().height}};}}'''
        commands += [{'name':'evaluate_script','_url':url,'arguments':{'function':code}},{'name':'take_screenshot','_url':url,'arguments':{'filePath':f'C:/Users/ADMIN/AppData/Local/Temp/index2-390-after-{n:02}-{tile:02}.png'}}]
    commands.append({'name':'close_page','_url':url,'arguments':{}})
(root/'reference/index2-final-mobile-capture.json').write_text(json.dumps(commands),encoding='utf-8')
