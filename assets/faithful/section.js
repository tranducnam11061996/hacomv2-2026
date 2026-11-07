window.HacomArt.mount=function(host, art, reflow, number, top, height) {
  const content=art.querySelector(".section-content");
  const svgNS = 'http://www.w3.org/2000/svg';


  function svgElement(name) {
    return document.createElementNS(svgNS, name);
  }

  function label(layer) {
    return [...layer.querySelectorAll('text')].map(text => text.textContent.trim()).filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
  }

  function announce(text) {
    window.HacomArt.feedback(text);
  }

  let carousel;
  function shiftCarousel(link) {
    if (!carousel) {
      let cards=[...content.querySelectorAll('g[id^="Product card"]')];
      if(number===19) cards=[...content.querySelectorAll('g[id="Frame 16"] > g, g[id="Frame 16"] > a > g')];
      if(cards.length<2) return false;
      cards=cards.map(card=>({card,x:geometricBox(card).x,transform:card.getAttribute('transform')||''})).sort((a,b)=>a.x-b.x);
      carousel={cards,position:0};
    }
    const {cards}=carousel;
    const arrows=[...content.querySelectorAll('a[data-action^="famicons:chevron-forward-circle-outline"]')]
      .sort((a,b)=>geometricBox(a).x-geometricBox(b).x);
    const step=arrows.indexOf(link)===0?-1:1;
    carousel.position=(carousel.position+step+cards.length)%cards.length;
    for(let index=0;index<cards.length;index++){
      const {card,x,transform}=cards[index];
      const target=cards[(index+carousel.position)%cards.length].x;
      const axis=art.getScreenCTM().inverse().multiply(card.parentNode.getScreenCTM()).a || 1;
      card.setAttribute('transform',`translate(${(target-x)/axis} 0) ${transform}`);
    }
    return true;
  }

  function actionHandler(link,event) {
    event.preventDefault();
    const name=link.getAttribute('aria-label')||link.textContent.trim();
    const kind=link.dataset.action||'';
    if (/^heart(?:_|$)/i.test(kind)) {
      const active=link.getAttribute('aria-pressed')==='true';
      link.setAttribute('aria-pressed',String(!active));
      link.classList.toggle('selected-favorite',!active);
      announce(active?'Đã bỏ yêu thích':'Đã thêm vào yêu thích');
    } else if (/^(?:cart box|buy button)/i.test(kind)) {
      window.HacomArt.addToCart();
    } else if (/^filter(?:_|$)/i.test(kind)) {
      for(const other of host.querySelectorAll('a[aria-current]')) other.removeAttribute('aria-current');
      link.setAttribute('aria-current','true');
      announce(name+' · Bộ lọc demo');
    } else if (kind.startsWith('famicons:chevron-forward-circle-outline') && !host.classList.contains('mobile') && shiftCarousel(link)) {
      return;
    } else {
      announce(name+' · Demo');
    }
  }

  function controls() {
    const action = /^(?:button\b|buy button|cart box|heart(?:_|$)|nav item|filter(?:_|$)|showroom \/|social \/|shopping channel|(?:view|see) all|cta\b|.*chevron-forward-circle-outline|.*button \/)/i;
    const marked = new Set();
    for (const layer of content.querySelectorAll('g[id]')) {
      const department=layer.parentElement?.id==='Menu' && layer.id!=='Department menu title' && !!label(layer);
      const video=number===19 && layer.parentElement?.id==='Frame 16';
      if (!(action.test(layer.id)||department||video) || [...marked].some(parent=>parent.contains(layer))) continue;
      const name = label(layer) || layer.id.replace(/_\d+$/,'');
      const link = svgElement('a');
      link.setAttribute('href','#');
      link.setAttribute('aria-label',name);
      link.dataset.action=layer.id;
      if (/^heart(?:_|$)/i.test(layer.id)) {
        link.setAttribute('role','button');
        link.setAttribute('aria-pressed','false');
      }
      link.addEventListener('click',event=>actionHandler(link,event));
      layer.before(link);
      link.append(layer);
      marked.add(layer);
    }
  }

  function mainBannerLinks() {
    const banner=content.querySelector('g[id="Main Banner"]');
    if(!banner) return;
    for(const [name,x,width] of [['Khám phá ngay',395,218],['Tư vấn cấu hình',623,200]]){
      const link=svgElement('a');
      link.setAttribute('href','#');
      link.setAttribute('aria-label',name);
      const region=svgElement('rect');
      for(const [key,value] of Object.entries({x,y:690,width,height:54,rx:27,fill:'transparent'})){
        region.setAttribute(key,value);
      }
      link.append(region);
      link.addEventListener('click',event=>actionHandler(link,event));
      banner.append(link);
    }
  }

  const groupPatterns = [
    /^(?:block 3_flash sale|product selection|product grid|career cards|career selection|category filters|desktop types|laptop discovery|laptop categories|trust metrics|content section|news introduction|news stories|editorial value|customer introduction|community evidence|category filter|frame (?:10|14|15|16|21|25|28|29|30)$)/i,
    /^(?:HACOM \/ (?:Gaming Gear|Console|Danh m)|Group 73$)/i
  ];

  function visibleParts(container) {
    return [...container.children].filter(node=>!['defs','mask','clipPath','foreignObject'].includes(node.localName));
  }

  function flatten(node) {
    if (node.localName === 'a') return [node];
    const children = visibleParts(node);
    if (!children.length || node.localName === 'text') return [node];
    if (children.length === 1 && children[0].localName === 'g') return flatten(children[0]);
    if (groupPatterns.some(pattern=>pattern.test(node.id))) {
      const groups = children.filter(child=>['g','a','text'].includes(child.localName));
      if (groups.length) return groups.flatMap(flatten);
    }
    return [node];
  }

  function geometricBox(node) {
    const box = node.getBBox();
    const matrix = art.getScreenCTM().inverse().multiply(node.getScreenCTM());
    const points = [[box.x,box.y],[box.x+box.width,box.y],[box.x,box.y+box.height],[box.x+box.width,box.y+box.height]].map(([x,y])=>new DOMPoint(x,y).matrixTransform(matrix));
    const x=Math.min(...points.map(p=>p.x)), y=Math.min(...points.map(p=>p.y));
    return {x,y,width:Math.max(...points.map(p=>p.x))-x,height:Math.max(...points.map(p=>p.y))-y};
  }

  function copyAsText(node) {
    const text = node.localName==='text' ? node : node.querySelector('text');
    const p = document.createElement('p');
    p.className='reflow-copy';
    p.textContent=[...node.querySelectorAll('tspan')].map(t=>t.textContent.trim()).filter(Boolean).join(' ') || text.textContent;
    for (const [css,svg] of [['fontFamily','font-family'],['fontSize','font-size'],['fontWeight','font-weight'],['letterSpacing','letter-spacing'],['color','fill']]) {
      if (text.hasAttribute(svg)) p.style[css]=text.getAttribute(svg)+(svg==='font-size'?'px':'');
    }
    return p;
  }

  function addInput(text, options) {
    if (!text) return;
    const box=text.getBBox();
    const field=svgElement('foreignObject');
    field.setAttribute('x',box.x);
    field.setAttribute('y',box.y-7);
    field.setAttribute('width',options.width);
    field.setAttribute('height',box.height+14);
    const input=document.createElement('input');
    input.className='art-input';
    input.type='text';
    input.name=number===1?'search':'contact';
    input.setAttribute('aria-label',options.label);
    input.style.fontFamily=text.getAttribute('font-family');
    input.style.fontSize=text.getAttribute('font-size')+'px';
    field.append(input);
    text.after(field);
    input.addEventListener('input',()=>text.style.visibility=input.value?'hidden':'visible');
    const submit=()=>{
      const value=input.value.trim();
      if(!value){input.focus();return;}
      if(options.consent && !options.consent.checked){
        announce('Vui lòng xác nhận đồng ý nhận thông tin từ HACOM');
        options.consent.focus();
        return;
      }
      if(options.validate && !options.validate(value)){
        announce('Vui lòng nhập email hoặc số điện thoại hợp lệ');
        input.focus();
        return;
      }
      announce(options.feedback);
    };
    input.addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();submit();}});
    const button=options.button;
    if(button) {
      button.setAttribute('role','button');
      button.setAttribute('tabindex','0');
      button.setAttribute('aria-label',options.label);
      button.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();submit();});
      button.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();submit();}});
    }
  }
  function consentField() {
    const group=content.querySelector('g[id^="Checkbox / HACOM"]');
    if(!group) return null;
    const box=group.getBBox();
    const field=svgElement('foreignObject');
    field.setAttribute('x',box.x);
    field.setAttribute('y',box.y);
    field.setAttribute('width',box.width);
    field.setAttribute('height',box.height);
    const input=document.createElement('input');
    input.type='checkbox';
    input.name='consent';
    input.checked=true;
    input.className='art-check';
    input.setAttribute('aria-label','Tôi đồng ý nhận thông tin từ HACOM');
    const tick=group.querySelector('path');
    input.addEventListener('change',()=>tick.style.visibility=input.checked?'visible':'hidden');
    field.append(input);
    group.append(field);
    return input;
  }

  function desktopForms() {
    if(number===1) addInput(content.querySelector('text[id="Description_7"]'),{
      width:635,label:'Tìm kiếm sản phẩm',feedback:'Đã nhận từ khóa tìm kiếm · Demo',
      button:content.querySelector('[id="Submit search"]')
    });
    if(number===22) addInput([...content.querySelectorAll('text')].find(t=>t.textContent.trim().startsWith('Nhập email')),{
      width:275,label:'Email hoặc số điện thoại',feedback:'Đăng ký thành công · Demo',
      consent:consentField(),
      validate:value=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)||/^\+?\d{9,15}$/.test(value),
      button:[...content.querySelectorAll('g[id^="Button / HACOM"]')].find(g=>label(g).includes('Đăng ký ngay'))
    });
  }

  function mobileNewsletter(layer) {
    const panel=document.createElement('div');
    panel.className='mobile-newsletter';
    const heading=layer.querySelector('text');
    panel.append(copyAsText(heading));
    const form=document.createElement('form');
    const input=document.createElement('input');
    input.required=true;
    input.name='contact';
    input.placeholder='Nhập email hoặc số điện thoại của bạn';
    input.setAttribute('aria-label',input.placeholder);
    input.pattern='[^\\s@]+@[^\\s@]+\\.[^\\s@]+|[+]?[0-9]{9,15}';
    const button=document.createElement('button');
    button.textContent='Đăng ký ngay';
    const consent=document.createElement('label');
    const check=document.createElement('input');
    check.type='checkbox';
    check.name='consent';
    check.required=true;
    check.checked=true;
    consent.append(check,' Tôi đồng ý nhận thông tin từ HACOM');
    form.append(input,button,consent);
    form.addEventListener('submit',event=>{
      event.preventDefault();
      announce('Đăng ký thành công · Demo');
    });
    panel.append(form);
    const benefits=[...layer.children].filter(node=>node.localName==='text').slice(2);
    const list=document.createElement('div');
    list.className='mobile-newsletter-benefits';
    for(let i=0;i<benefits.length;i+=2){
      const benefit=document.createElement('div');
      benefit.append(...benefits.slice(i,i+2).map(copyAsText));
      list.append(benefit);
    }
    panel.append(list);
    return panel;
  }

  function mobileSearch() {
    const form=document.createElement('form');
    form.className='mobile-search';
    form.setAttribute('role','search');
    const input=document.createElement('input');
    input.setAttribute('aria-label','Tìm kiếm sản phẩm');
    input.name='search';
    input.placeholder='Bạn cần tìm gì hôm nay? (ví dụ: Laptop ASUS, RTX 5070, Màn hình 2K...)';
    input.required=true;
    const button=document.createElement('button');
    button.textContent='Tìm kiếm';
    form.append(input,button);
    form.addEventListener('submit',event=>{
      event.preventDefault();
      announce('Đã nhận từ khóa tìm kiếm · Demo');
    });
    return form;
  }

  function mobile() {
    host.classList.add('mobile');
    const inner = content.children.length===1 && content.firstElementChild.localName==='g' ? content.firstElementChild : content;
    const width = Math.max(260,host.clientWidth-32);
    const pieces = [7,14].includes(number) ? [inner] : visibleParts(inner).flatMap(flatten);
    const entries = pieces.filter(node=>!node.dataset?.action?.startsWith('famicons:chevron-forward-circle-outline')).map(node=>({node,...geometricBox(node)}))
      .filter(item=>item.width>8 && item.height>4)
      .sort((a,b)=>Math.abs(a.y-b.y)>25?a.y-b.y:a.x-b.x);
    const grid=document.createElement('div');
    grid.className='reflow-grid';
    for (const entry of entries) {
      const {node,x,y,width:w,height:h}=entry;
      if (w>width && (node.localName==='text' || (node.children.length===1 && node.firstElementChild.localName==='text'))) {
        grid.append(copyAsText(node));
        continue;
      }
      if(number===22 && node.id.startsWith('01 /')){
        grid.append(mobileNewsletter(node));
        continue;
      }
      if (number===1 && node.id==='Search') {
        grid.append(mobileSearch());
        continue;
      }
      if (number===1 && (node.id==='Rectangle_2' || node.id==='Rectangle_3' || node.id.startsWith('Vector 2'))) continue;
      const piece=document.createElement('div');
      piece.className='reflow-piece';
      const copy=svgElement('svg');
      copy.setAttribute('viewBox', [x,y,w,h].join(' '));
      copy.setAttribute('fill','none');
      copy.setAttribute('width',Math.ceil(w));
      copy.setAttribute('height',Math.ceil(h));
      const matrix=art.getScreenCTM().inverse().multiply(node.parentNode.getScreenCTM());
      const translated=svgElement('g');
      translated.setAttribute('transform',`matrix(${matrix.a} ${matrix.b} ${matrix.c} ${matrix.d} ${matrix.e} ${matrix.f})`);
      const layer=node.cloneNode(true);
      layer.querySelectorAll('foreignObject').forEach(object=>object.remove());
      for(const d of [layer,...layer.querySelectorAll('[id]')])d.removeAttribute('id');
      translated.append(layer);
      copy.append(translated);
      piece.append(copy);
      if (number===1 && /(?:Main Banner|^Banner )/.test(node.id)) {
        piece.classList.add('fit-original-art');
      }
      if(w>width && !piece.classList.contains('fit-original-art')) {
        piece.tabIndex=0;
        piece.setAttribute('aria-label',label(node).slice(0,120)||'Nội dung có thể cuộn ngang');
      }
      if (number===1 && node.id==='Menu') {
        const details=document.createElement('details');
        const summary=document.createElement('summary');
        summary.textContent='Danh mục sản phẩm';
        details.append(summary,piece);
        details.addEventListener('keydown',event=>{
          if(event.key==='Escape' && details.open){
            details.open=false;
            summary.focus();
          }
        });
        grid.append(details);
      } else {
        grid.append(piece);
      }
    }
    reflow.replaceChildren(grid);
    for(const a of reflow.querySelectorAll('a')){
      a.addEventListener('click',event=>actionHandler(a,event));
    }
  }

  controls();
  if(number===1) mainBannerLinks();
  let mobileMode;
  const render=()=>{
    if(mobileMode===null || mobileMode!==window.HacomArt.small.matches){
      mobileMode=window.HacomArt.small.matches;
      host.classList.toggle('mobile',mobileMode);
      art.toggleAttribute('inert',mobileMode);
      art.setAttribute('aria-hidden',String(mobileMode));
      host.dataset.layout=mobileMode?'mobile':'desktop';
      if(mobileMode){
        art.setAttribute('viewBox','0 0 1920 20142');
        mobile();
      } else {
        reflow.replaceChildren();
        art.setAttribute('viewBox',`0 ${top} 1920 ${height}`);
        if (!content.querySelector('.art-input')) desktopForms();
      }
    }
  };
  art.getBoundingClientRect();
  document.fonts.ready.then(()=>{
    mobileMode=null;
    render();
    window.HacomArt.small.addEventListener('change',render);
  });

};
