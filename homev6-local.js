/* Local interactions for the captured HACOM homev6 DOM. */
(() => {
  const status = document.querySelector('#local-status');
  let statusTimer;
  let cart = 0;
  function announce(message) {
    status.textContent = message;
    status.hidden = false;
    clearTimeout(statusTimer);
    statusTimer = setTimeout(() => { status.hidden = true; }, 3000);
  }
  const scrollable = element => element && [...element.querySelectorAll('div')].find(node =>
    getComputedStyle(node).overflowX === 'auto' && node.scrollWidth > node.clientWidth + 2);
  function nearbyScroller(button) {
    for (let parent = button.parentElement; parent && parent !== document.body; parent = parent.parentElement) {
      const found = scrollable(parent);
      if (found) return found;
    }
  }
  document.querySelectorAll('.swiper').forEach(swiper => {
    const slides = [...swiper.querySelector('.swiper-wrapper').children];
    let current = 0;
    function show(index) {
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, i) => { slide.hidden = i !== current; });
      swiper.parentElement.querySelectorAll('[aria-label^="Chuyển tới slide"]').forEach((button, i) => {
        button.setAttribute('aria-pressed', String(i === current));
      });
    }
    show(0);
    swiper.parentElement.querySelectorAll('button').forEach(button => {
      const label = button.getAttribute('aria-label') || '';
      if (label.startsWith('Chuyển tới slide')) button.addEventListener('click', () => show(Number(label.match(/\d+/)[0]) - 1));
      if (label === 'Slide trước') button.addEventListener('click', () => show(current - 1));
      if (label === 'Slide tiếp theo') button.addEventListener('click', () => show(current + 1));
    });
  });
  document.querySelectorAll('[class*="overflow-x-auto"]').forEach(element => {
    let start;
    let left;
    let dragged = false;
    element.tabIndex = element.tabIndex >= 0 ? element.tabIndex : 0;
    element.addEventListener('pointerdown', event => {
      if (event.pointerType !== 'mouse' || event.target.closest('button,input')) return;
      start = event.clientX;
      left = element.scrollLeft;
      dragged = false;
    });
    element.addEventListener('pointermove', event => {
      if (start === undefined || !event.buttons) return;
      if (Math.abs(event.clientX - start) > 6) {
        dragged = true;
        element.scrollLeft = left - (event.clientX - start);
      }
    });
    window.addEventListener('pointerup', () => { start = undefined; });
    element.addEventListener('click', event => {
      if (dragged) { event.preventDefault(); event.stopPropagation(); dragged = false; }
    }, true);
  });
  document.addEventListener('submit', event => {
    event.preventDefault();
    const input = event.target.querySelector('input');
    if (!event.target.reportValidity()) return;
    announce(input ? 'Đã nhận ' + input.value.trim() + ' · Demo' : 'Đã nhận thông tin · Demo');
  });
  function productCards(section) {
    const scroller = [...section.querySelectorAll('[class*="overflow-x-auto"]')].find(node =>
      node.querySelector('button[aria-label="Thêm vào yêu thích"]'));
    if (!scroller) return [];
    return [...scroller.children].filter(node => node.querySelector('img'));
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    const anchor = event.target.closest('a');
    if (!button) {
      if (anchor && anchor.getAttribute('href') === '#') {
        event.preventDefault();
        announce((anchor.textContent.trim() || anchor.getAttribute('aria-label') || 'Liên kết') + ' · Demo');
      }
      return;
    }
    const label = button.getAttribute('aria-label') || button.textContent.trim();
    if (/^(Slide |Chuyển tới slide)/.test(label)) return;
    if (/yêu thích/i.test(label)) {
      const selected = button.getAttribute('aria-pressed') !== 'true';
      button.setAttribute('aria-pressed', String(selected));
      button.style.color = selected ? '#e72429' : '';
      announce(selected ? 'Đã thêm vào yêu thích · Demo' : 'Đã bỏ yêu thích · Demo');
      return;
    }
    if (/giỏ hàng|mua ngay/i.test(label)) {
      announce('Giỏ hàng (' + (++cart) + ') · Demo');
      return;
    }
    if (/Sản phẩm (trước|tiếp)|Trang (trước|tiếp)|Cuộn tiếp/.test(label)) {
      const scroller = nearbyScroller(button);
      if (scroller) scroller.scrollBy({left: (label.includes('trước') ? -1 : 1) * scroller.clientWidth, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
      return;
    }
    if (label === 'Mở danh mục sản phẩm') {
      const panel = document.querySelector('#local-mobile-menu');
      panel.showModal();
      return;
    }
    const section = button.closest('section');
    if (section && label && !button.querySelector('svg') && label.length < 50) {
      const cards = productCards(section);
      if (cards.length) {
        const terms = label.toLocaleLowerCase('vi').split(/\s+/);
        const matches = cards.filter(card => terms.some(term => term.length > 2 && card.textContent.toLocaleLowerCase('vi').includes(term)));
        if (cards.length) {
          cards.forEach(card => { card.hidden = !/tất cả/i.test(label) && !matches.includes(card); });
          section.querySelectorAll('button[data-local-filter]').forEach(other => other.removeAttribute('aria-pressed'));
          button.dataset.localFilter = '';
          button.setAttribute('aria-pressed', 'true');
          announce('Đang hiển thị ' + (/tất cả/i.test(label) ? cards.length : matches.length) + ' sản phẩm · Demo');
          return;
        }
      }
    }
    announce((label || 'Thao tác') + ' · Demo');
  });
  document.querySelectorAll('span').forEach(label => {
    if (label.textContent.trim() !== 'KẾT THÚC SAU') return;
    const group = label.parentElement.parentElement;
    const numbers = [...group.querySelectorAll('div')].filter(node =>
      node.children.length === 0 && /^\d{2}$/.test(node.textContent.trim()));
    if (numbers.length !== 3) return;
    let remaining = Number(numbers[0].textContent) * 3600 + Number(numbers[1].textContent) * 60 + Number(numbers[2].textContent);
    const deadline = Date.now() + remaining * 1000;
    const interval = setInterval(() => {
      remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      [Math.floor(remaining / 3600), Math.floor(remaining / 60) % 60, remaining % 60].forEach((value, i) => {
        numbers[i].textContent = String(value).padStart(2, '0');
      });
      if (!remaining) clearInterval(interval);
    }, 1000);
  });
  const menu = document.createElement('dialog');
  menu.id = 'local-mobile-menu';
  const close = document.createElement('button');
  close.textContent = 'Đóng danh mục';
  close.addEventListener('click', () => menu.close());
  menu.append(close);
  const sourceMenu = document.querySelector('#menu-page-home-v6');
  if (sourceMenu) {
    const links = [...sourceMenu.querySelectorAll('a')].filter(link => link.textContent.trim()).slice(0, 30);
    links.forEach(link => { const copy = link.cloneNode(true); menu.append(copy); });
  }
  document.body.append(menu);
})();
