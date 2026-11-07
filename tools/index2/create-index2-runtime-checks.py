from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
html=(root/'index2.html').read_text(encoding='utf-8')
html=html.replace('<head>','<head>\n<base href="file:///D:/hacomv2-2026/">\n<meta http-equiv="Content-Security-Policy" content="script-src \'none\'">',1)
Path('C:/Users/ADMIN/AppData/Local/Temp/index2-nojs-verification.html').write_text(html,encoding='utf-8')
url='file:///C:/Users/ADMIN/AppData/Local/Temp/index2-nojs-verification.html'
commands=[{'name':'emulate','_url':url,'arguments':{'viewport':'1920x1080x1'}},{'name':'evaluate_script','_url':url,'arguments':{'function':'''async () => {await document.fonts.ready;const button=document.querySelector('button[aria-pressed]');button.click();return {url:location.href,csp:document.querySelector('[http-equiv="Content-Security-Policy"]').content,headings:document.querySelectorAll('h1,h2,h3').length,sections:document.querySelectorAll('[data-section]').length,textRuns:document.querySelectorAll('.text-run').length,height:document.body.scrollHeight,favoriteRemainsInactive:button.getAttribute('aria-pressed')==='false',statusRemainsEmpty:document.querySelector('#demo-status').textContent===''};}'''}},{'name':'take_screenshot','_url':url,'arguments':{'filePath':'C:/Users/ADMIN/AppData/Local/Temp/index2-nojs-hero.png'}},{'name':'list_console_messages','_url':url,'arguments':{'types':['error']}}]
(root/'reference/index2-nojs-commands.json').write_text(json.dumps(commands),encoding='utf-8')
commands=[]
for name in ['index','index2']:
    url=f'http://127.0.0.1:8765/{name}.html?index2-load-measurement'
    commands += [{'name':'emulate','_url':url,'arguments':{'viewport':'1920x1080x1'}},{'name':'navigate_page','_url':url,'arguments':{'type':'reload'}},{'name':'evaluate_script','_url':url,'arguments':{'function':'''async () => {await document.fonts.ready;let lcp=null;const observer=new PerformanceObserver(list=>{const entries=list.getEntries();lcp=entries.at(-1)?.startTime??null;});observer.observe({type:'largest-contentful-paint',buffered:true});await new Promise(r=>setTimeout(r,250));observer.disconnect();const nav=performance.getEntriesByType('navigation')[0],resources=performance.getEntriesByType('resource');return {url:location.href,paint:performance.getEntriesByType('paint').map(e=>({name:e.name,time:e.startTime})),largestContentfulPaint:lcp,domContentLoaded:nav.domContentLoadedEventEnd,load:nav.loadEventEnd,requests:resources.length,transferredResourceBytes:resources.reduce((n,r)=>n+r.encodedBodySize,0),nodes:document.querySelectorAll('*').length};}'''}}]
(root/'reference/index2-load-commands.json').write_text(json.dumps(commands),encoding='utf-8')
