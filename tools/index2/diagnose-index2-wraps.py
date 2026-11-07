from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
matrix=json.loads((root/'reference/index2-matrix-commands.json').read_text())
out=[]
for start in [0,16]:
    commands=matrix[start:start+8]
    for c in commands:
        if c['name']=='evaluate_script' and 'sections:' in c['arguments']['function']:
            c['arguments']['function']='''() => ({url:location.href,width:innerWidth,items:[...document.querySelectorAll('[data-section="15"] .reflow-copy,[data-section="4"] .reflow-copy')].map(n=>({section:n.closest('[data-section]').dataset.section,text:n.textContent,style:n.getAttribute('style'),font:getComputedStyle(n).font,lineHeight:getComputedStyle(n).lineHeight,rect:n.getBoundingClientRect().toJSON()}))})'''
    out.extend(commands)
(root/'reference/index2-wrap-commands.json').write_text(json.dumps(out),encoding='utf-8')
