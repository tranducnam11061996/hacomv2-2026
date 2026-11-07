from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
new='http://127.0.0.1:8765/index2.html?index2-audit-new';old='http://127.0.0.1:8765/index.html?index2-audit-original'
for width in [1920,390]:
    commands=[]
    for label,url in [('before',old),('after',new)]:
        commands += [{'name':'emulate','_url':url,'arguments':{'viewport':f'{width}x{6000 if width==390 else 1500}x1'}}]
        if label=='after':commands.append({'name':'navigate_page','_url':url,'arguments':{'type':'reload'}})
        commands.append({'name':'evaluate_script','_url':url,'arguments':{'function':'''async () => {await document.fonts.ready;document.querySelector('#demo-status').hidden=true;if(!document.querySelector('#capture-spacer')){const spacer=document.createElement('div');spacer.id='capture-spacer';spacer.style.height='6500px';document.body.append(spacer);}await new Promise(r=>setTimeout(r,200));return {url:location.href,width:innerWidth};}'''}})
        for n in range(1,23):
            code=f'''async () => {{const section=document.querySelector('[data-section="{n}"]');window.scrollTo(0,section.getBoundingClientRect().top+scrollY);for(const img of section.querySelectorAll('img'))if(img.checkVisibility()){{img.loading='eager';try{{await Promise.race([img.decode(),new Promise((_,reject)=>setTimeout(()=>reject(Error('decode timeout')),3000))])}}catch(e){{return {{error:img.src,message:e.message}}}}}}await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));return {{number:{n},scroll:scrollY,height:section.getBoundingClientRect().height,top:section.getBoundingClientRect().top}};}}'''
            commands += [{'name':'evaluate_script','_url':url,'arguments':{'function':code}},{'name':'take_screenshot','_url':url,'arguments':{'filePath':f'C:/Users/ADMIN/AppData/Local/Temp/index2-{width}-{label}-{n:02}.png'}}]
    (root/f'reference/index2-capture-{width}.json').write_text(json.dumps(commands),encoding='utf-8')
