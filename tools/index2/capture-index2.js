async () => {
  const clean = svg => {
    const clone=svg.cloneNode(true);
    clone.querySelectorAll('text,foreignObject').forEach(n=>n.remove());
    clone.removeAttribute('aria-hidden'); clone.removeAttribute('inert');
    clone.querySelectorAll('image').forEach(n=>{
      for(const a of [...n.attributes]) if(a.name.endsWith('href') && a.value.startsWith('assets/')) n.setAttributeNS(a.namespaceURI,a.name,'../../'+a.value);
    });
    return new XMLSerializer().serializeToString(clone);
  };
  const read = (svg,host) => {
    const inv=svg.getScreenCTM().inverse();
    const rect=n=>{const b=n.getBBox(),m=inv.multiply(n.getScreenCTM());const pts=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y])=>new DOMPoint(x,y).matrixTransform(m));const x=Math.min(...pts.map(p=>p.x)),y=Math.min(...pts.map(p=>p.y));return {x,y,w:Math.max(...pts.map(p=>p.x))-x,h:Math.max(...pts.map(p=>p.y))-y};};
    const texts=[...svg.querySelectorAll('text')].map(t=>{
      const cs=getComputedStyle(t),box=rect(t),parts=[...t.querySelectorAll('tspan')].filter(x=>x.textContent);
      const rows=(parts.length?parts:[t]).map(n=>{
        const pos=n.getStartPositionOfChar(0),m=inv.multiply(n.getScreenCTM()),p=new DOMPoint(pos.x,pos.y).matrixTransform(m),style=getComputedStyle(n);
        return {text:n.textContent,x:p.x,y:p.y,font:style.fontFamily,size:parseFloat(style.fontSize),weight:style.fontWeight,color:style.fill,spacing:style.letterSpacing,opacity:style.opacity};
      });
      let parent=t.parentElement,card='';while(parent&&parent!==svg){if(/^Product card/i.test(parent.id)){card=parent.id;break;}parent=parent.parentElement;}
      return {key:t.dataset.key,id:t.id,text:t.textContent,box,rows,card};
    });
    const actions=[...svg.querySelectorAll('a[data-action],a[aria-label],g[role="button"]')].map(a=>({name:a.getAttribute('aria-label')||a.textContent.trim(),kind:a.dataset.action||'demo',box:rect(a),card:a.closest('g[id^="Product card"]')?.id||''}));
    return {texts,actions,background:clean(svg)};
  };
  window.exportIndex2={clean,read};
  const sections=[...document.querySelectorAll('main>section')].map(host=>({number:Number(host.dataset.section),title:host.getAttribute('aria-label'),top:Number(host.dataset.top),height:Number(host.dataset.height),...read(host.querySelector('.section-art'),host)}));
  return sections;
}
