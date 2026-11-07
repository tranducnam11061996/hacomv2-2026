from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
new='http://127.0.0.1:8765/index2.html?index2-audit-new';old='http://127.0.0.1:8765/index.html?index2-audit-original'
commands=[]
for url in [old,new]:
    commands += [{'name':'emulate','_url':url,'arguments':{'viewport':'390x844x1'}},{'name':'evaluate_script','_url':url,'arguments':{'function':'''async () => {await document.fonts.ready;await new Promise(r=>setTimeout(r,100));const section=document.querySelector('[data-section="12"]');return [...section.querySelectorAll('.reflow-grid>.reflow-copy,.mobile-special')].map(n=>({text:n.textContent,rect:n.getBoundingClientRect().toJSON(),style:n.getAttribute('style'),child:n.firstElementChild?.outerHTML}));}'''}}]
(root/'reference/index2-diagnostic-commands.json').write_text(json.dumps(commands),encoding='utf-8')
commands=[{'name':'lighthouse_audit','_url':new,'arguments':{'device':'desktop','mode':'navigation','outputDirPath':'C:/Users/ADMIN/AppData/Local/Temp/index2-lighthouse-desktop'}},{'name':'lighthouse_audit','_url':new,'arguments':{'device':'mobile','mode':'navigation','outputDirPath':'C:/Users/ADMIN/AppData/Local/Temp/index2-lighthouse-mobile'}}]
(root/'reference/index2-lighthouse-commands.json').write_text(json.dumps(commands),encoding='utf-8')
