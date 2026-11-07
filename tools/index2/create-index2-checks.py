from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
new='http://127.0.0.1:8765/index2.html?index2-audit-new'
old='http://127.0.0.1:8765/index.html?index2-audit-original'
def cmd(name,url,args):return {'name':name,'_url':url,'arguments':args}
read="""async () => {await document.fonts.ready;await new Promise(r=>setTimeout(r,120));return {url:location.href,width:innerWidth,height:document.body.scrollHeight,overflow:document.documentElement.scrollWidth-innerWidth,nodes:document.querySelectorAll('*').length,headings:[...document.querySelectorAll('h1,h2,h3')].filter(n=>n.checkVisibility()).map(n=>({tag:n.tagName,text:n.textContent.trim()})),sections:[...document.querySelectorAll('[data-section]')].map(s=>({number:Number(s.dataset.section),top:s.getBoundingClientRect().top+scrollY,height:s.getBoundingClientRect().height})),resources:performance.getEntriesByType('resource').map(r=>({name:r.name,bytes:r.encodedBodySize,duration:r.duration})),navigation:performance.getEntriesByType('navigation').map(r=>({domContentLoaded:r.domContentLoadedEventEnd,load:r.loadEventEnd})),schema:document.querySelectorAll('script[type="application/ld+json"]').length};}"""
commands=[]
for width in [360,390,768,1023,1024,1280,1440,1920,2560,3440]:
    for url in [old,new]:
        ready="""async () => {if(window.HacomArt){if(typeof observe!=='undefined')observe.disconnect();await Promise.all([...document.querySelectorAll('section')].map(s=>s.dataset.loaded?null:new Promise((r,j)=>{const src='assets/faithful/'+s.dataset.section.padStart(2,'0')+'.js';let el=[...document.scripts].find(el=>el.src.endsWith('/'+src));if(el){el.addEventListener('load',r,{once:true});el.addEventListener('error',j,{once:true});}else{el=document.createElement('script');el.src=src;el.onload=r;el.onerror=j;document.head.append(el)}})));}await document.fonts.ready;await new Promise(r=>setTimeout(r,200));return {ready:true};}"""
        ready=ready.replace("if(window.HacomArt){", "if(window.HacomArt){const register=HacomArt.register;HacomArt.register=function(number,markup){const host=document.querySelector('[data-section=\"'+number+'\"]');if(host?.dataset.loaded)return;return register.call(this,number,markup)};")
        commands+=[cmd('emulate',url,{'viewport':f'{width}x1080x1'}),cmd('navigate_page',url,{'type':'reload'}),cmd('evaluate_script',url,{'function':ready}),cmd('evaluate_script',url,{'function':read})]
(root/'reference/index2-matrix-commands.json').write_text(json.dumps(commands),encoding='utf-8')

test="""async () => {
 const result={url:location.href};
 const q=s=>document.querySelector(s),click=s=>q(s).click();
 const favorite=q('.desktop-controls button[aria-pressed]');favorite.click();result.favoriteOn=favorite.getAttribute('aria-pressed');favorite.click();result.favoriteOff=favorite.getAttribute('aria-pressed');
 click('.desktop-controls [data-action^="Buy button"],.desktop-controls [data-action^="Cart box"]');result.cart=q('#demo-status').textContent;
 const filter=q('.desktop-controls [data-action^="Filter"]');filter.click();result.filter=filter.getAttribute('aria-current');
 const arrow=q('.desktop-controls [data-action*="chevron-forward-circle-outline"]');arrow.click();result.carousel={position:arrow.closest('[data-section]').dataset.position,images:arrow.closest('[data-section]').querySelectorAll('.carousel-art img').length};
 const search=q('.desktop-search');search.elements.search.value='Laptop ASUS';search.requestSubmit();result.search=q('#demo-status').textContent;
 const form=q('.desktop-newsletter');form.elements.contact.value='invalid';form.requestSubmit();result.invalidContact=q('#demo-status').textContent;
 form.elements.contact.value='test@example.com';form.elements.consent.checked=false;result.consentRequired=!form.checkValidity();form.elements.consent.checked=true;form.requestSubmit();result.validContact=q('#demo-status').textContent;
 return result;
}"""
mobiletest="""async () => {const result={url:location.href};const menu=document.querySelector('.department-menu');menu.querySelector('summary').click();result.open=menu.open;menu.querySelector('summary').dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));result.closed=!menu.open;result.returnedFocus=document.activeElement===menu.querySelector('summary');const form=document.querySelector('.mobile-search');form.elements.search.value='Laptop';form.requestSubmit();result.search=document.querySelector('#demo-status').textContent;const news=document.querySelector('.mobile-newsletter form');result.initialConsent=news.elements.consent.checked;news.elements.contact.value='0901234567';news.requestSubmit();result.newsletter=document.querySelector('#demo-status').textContent;return result;}"""
commands=[cmd('emulate',new,{'viewport':'1920x1080x1'}),cmd('navigate_page',new,{'type':'reload'}),cmd('evaluate_script',new,{'function':test}),cmd('emulate',new,{'viewport':'390x844x1'}),cmd('evaluate_script',new,{'function':mobiletest})]
(root/'reference/index2-interaction-commands.json').write_text(json.dumps(commands),encoding='utf-8')
