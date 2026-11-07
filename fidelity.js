const sections = [...document.querySelectorAll('.design-page section')];
const small = matchMedia('(max-width: 1023px)');
const status = document.querySelector('#demo-status');
let dismiss;
let cartCount=0;

function feedback(text) {
  status.textContent=text;
  status.hidden=false;
  clearTimeout(dismiss);
  dismiss=setTimeout(()=>status.hidden=true,2400);
}

window.HacomArt = {
  small,
  feedback,
  addToCart() { feedback('Đã thêm vào giỏ hàng ('+(++cartCount)+') · Demo'); },
  register(number, markup) {
    const host=sections[number-1];
    host.innerHTML=markup+'<div class="section-reflow"></div>';
    const art=host.querySelector('.section-art');
    const {top,height}=host.dataset;
    art.setAttribute('viewBox',`0 ${top} 1920 ${height}`);
    HacomArt.mount(host,art,host.querySelector('.section-reflow'),number,top,height);
    host.dataset.loaded='true';
  }
};

const observe = new IntersectionObserver(entries=>{
  for (const entry of entries) {
    if(!entry.isIntersecting) continue;
    const host=entry.target;
    observe.unobserve(host);
    const script=document.createElement('script');
    script.src='assets/faithful/'+host.dataset.section.padStart(2,'0')+'.js';
    script.onerror=()=>{
      host.dataset.error='true';
      host.textContent='Không tải được phần '+host.getAttribute('aria-label');
    };
    document.head.append(script);
  }
},{rootMargin:'900px'});
sections.forEach(host=>observe.observe(host));
