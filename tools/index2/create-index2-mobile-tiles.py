from pathlib import Path
import json,math,runpy
root=Path(__file__).resolve().parents[2]
values=runpy.run_path(str(Path(__file__).with_name('inspect-index2-results.py')))['values']
row=next(r for r in values('reference/index2-matrix-results.json') if r.get('width')==390 and 'index.html?' in r['url'])
commands=[]
for label,url in [('before','http://127.0.0.1:8765/index.html?index2-audit-mobile-before'),('after','http://127.0.0.1:8765/index2.html?index2-audit-mobile-after')]:
    commands.append({'name':'emulate','_url':url,'arguments':{'viewport':'390x1080x1'}})
    prepare='''async () => {if(window.HacomArt){await Promise.all([...document.querySelectorAll('section')].map(s=>s.dataset.loaded?null:new Promise((r,j)=>{const el=document.createElement('script');el.src='assets/faithful/'+s.dataset.section.padStart(2,'0')+'.js';el.onload=r;el.onerror=j;document.head.append(el)})));}await document.fonts.ready;if(!document.querySelector('#capture-spacer')){const el=document.createElement('div');el.id='capture-spacer';el.style.height='2000px';document.body.append(el);}await new Promise(r=>setTimeout(r,200));return {url:location.href,width:innerWidth};}'''
    commands.append({'name':'evaluate_script','_url':url,'arguments':{'function':prepare}})
    for section in row['sections']:
        n=section['number'];height=section['height']
        for tile in range(math.ceil(height/1080)):
            offset=tile*1080
            code=f'''async () => {{const s=document.querySelector('[data-section="{n}"]');window.scrollTo(0,s.getBoundingClientRect().top+scrollY+{offset});for(const image of s.querySelectorAll('img'))if(image.checkVisibility()){{image.loading='eager';try{{await Promise.race([image.decode(),new Promise((_,reject)=>setTimeout(reject,2500))])}}catch(e){{}}}}await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));return {{number:{n},tile:{tile},height:s.getBoundingClientRect().height,scroll:scrollY,top:s.getBoundingClientRect().top}};}}'''
            commands += [{'name':'evaluate_script','_url':url,'arguments':{'function':code}},{'name':'take_screenshot','_url':url,'arguments':{'filePath':f'C:/Users/ADMIN/AppData/Local/Temp/index2-390-{label}-{n:02}-{tile:02}.png'}}]
(root/'reference/index2-mobile-tiles.json').write_text(json.dumps(commands),encoding='utf-8')
(root/'reference/index2-mobile-heights.json').write_text(json.dumps(row['sections']),encoding='utf-8')
print('Prepared',len(commands),'MCP operations')
