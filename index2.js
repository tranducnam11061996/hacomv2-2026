/* Demo interactions only. All page content and layout are present in HTML/CSS. */
(() => {
  const status=document.querySelector('#demo-status');
  let timer,cart=0;
  // The reference selects its text reflow mode on entering the mobile breakpoint.
  // Keep that mode through mobile-to-mobile resizes; content remains static HTML.
  const mobile=matchMedia('(max-width:1023px)');
  function selectReflowMode(){
    const width=document.querySelector('.page').clientWidth;
    document.querySelectorAll('[data-reflow-threshold]').forEach(node=>{
      if(mobile.matches)node.dataset.reflowMode=width<Number(node.dataset.reflowThreshold)?'flow':'fixed';
      else delete node.dataset.reflowMode;
    });
  }
  document.fonts.ready.then(selectReflowMode);mobile.addEventListener('change',selectReflowMode);
  function announce(message){status.textContent=message;status.hidden=false;clearTimeout(timer);timer=setTimeout(()=>status.hidden=true,2400);}
  function rotate(button){
    if(matchMedia('(max-width:1023px)').matches)return false;
    const section=button.closest('[data-section]'),cards=JSON.parse(section.dataset.cards||'[]').sort((a,b)=>a.x-b.x);
    if(cards.length<2)return false;
    const arrows=[...section.querySelectorAll('.desktop-controls [data-action*="chevron-forward-circle-outline"]')].sort((a,b)=>a.getBoundingClientRect().x-b.getBoundingClientRect().x);
    const direction=arrows.indexOf(button)===0?-1:1;
    const position=((Number(section.dataset.position)||0)+direction+cards.length)%cards.length;
    section.dataset.position=String(position);
    let overlay=section.querySelector('.carousel-art');
    if(!overlay){overlay=document.createElement('div');overlay.className='carousel-art';overlay.setAttribute('aria-hidden','true');section.querySelector('.section-layout').prepend(overlay);}
    overlay.replaceChildren();
    for(let i=0;i<cards.length;i++){
      const card=cards[i],target=cards[(i+position)%cards.length],dx=target.x-card.x;
      const image=document.createElement('img');image.alt='';image.src=card.image;image.style.cssText=`position:absolute;left:${target.x}px;top:${card.y}px;width:${card.w}px;height:${card.h}px;background:white`;
      overlay.append(image);
      section.querySelectorAll('.copy[data-card],.desktop-controls [data-card]').forEach(node=>{if(node.dataset.card===card.id)node.style.transform=`translateX(${dx}px)`;});
    }
    return true;
  }
  function submit(form){
    const field=form.elements.search||form.elements.contact;
    if(!form.reportValidity())return;
    const value=field.value.trim();
    if(form.elements.contact&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$|^\+?\d{9,15}$/.test(value)){announce('Vui lòng nhập email hoặc số điện thoại hợp lệ');field.focus();return;}
    announce(form.elements.search?'Đã nhận từ khóa tìm kiếm · Demo':'Đăng ký thành công · Demo');
  }
  document.addEventListener('submit',event=>{event.preventDefault();submit(event.target);});
  document.addEventListener('input',event=>{
    if(event.target.matches('.desktop-search input,.desktop-newsletter>input')){
      const section=event.target.closest('[data-section]');
      for(const node of section.querySelectorAll('.copy'))if(node.textContent.includes(event.target.name==='search'?'Bạn cần tìm gì hôm nay?':'Nhập email hoặc số điện thoại'))node.style.visibility=event.target.value?'hidden':'';
    }
  });
  document.addEventListener('click',event=>{
    const slide=event.target.closest('[data-hero-slide]');
    if(slide){slide.closest('.hero-pagination').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===slide)));announce('Banner '+(Number(slide.dataset.heroSlide)+1)+' · Demo');return;}

    const button=event.target.closest('[data-action]');if(!button)return;
    const kind=button.dataset.action,name=button.getAttribute('aria-label')||button.textContent.trim();
    if(/^heart(?:_|$)/i.test(kind)){const on=button.getAttribute('aria-pressed')!=='true';button.closest('[data-section]').querySelectorAll('button[data-action]').forEach(other=>{if(other.dataset.action===kind){other.setAttribute('aria-pressed',String(on));other.setAttribute('aria-label',on?'Bỏ yêu thích':'Thêm vào yêu thích');}});announce(on?'Đã thêm vào yêu thích':'Đã bỏ yêu thích');}
    else if(/^(cart box|buy button)/i.test(kind))announce(`Đã thêm vào giỏ hàng (${++cart}) · Demo`);
    else if(/^filter(?:_|$)/i.test(kind)){button.closest('[data-section]').querySelectorAll('[aria-current]').forEach(n=>n.removeAttribute('aria-current'));button.setAttribute('aria-current','true');announce(name+' · Bộ lọc demo');}
    else if(kind.includes('chevron-forward-circle-outline')&&rotate(button))return;
    else if(name==='Tìm kiếm'||name==='Tìm kiếm sản phẩm'||kind==='Submit search')submit(document.querySelector('.desktop-search'));
    else if(name==='Email hoặc số điện thoại'||name==='Đăng ký ngay')submit(document.querySelector('.desktop-newsletter'));
    else announce(name+' · Demo');
  });
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){const details=event.target.closest('details[open]');if(details){details.open=false;details.querySelector('summary').focus();}}});
})();
