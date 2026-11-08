/* The storefront is a static demo. Interactions work on the rendered components. */
(() => {
  const status = document.querySelector('#demo-status');
  const favorites = new Set();
  let cartCount = 0;
  let timer;

  function announce(message) {
    clearTimeout(timer);
    status.textContent = message;
    status.hidden = false;
    timer = setTimeout(() => { status.hidden = true; }, 2500);
  }

  const menu = document.querySelector('.departments');
  const desktop = matchMedia('(width >= 1440px)');
  function updateMenu() {
    menu.open = desktop.matches;
  }
  updateMenu();
  desktop.addEventListener('change', updateMenu);

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open && menu.contains(event.target)) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });

  document.addEventListener('submit', event => {
    const form = event.target;
    if (!form.matches('[data-form]')) return;
    event.preventDefault();
    if (form.dataset.form === 'search') {
      announce('Đã nhận từ khóa tìm kiếm · Demo');
      return;
    }
    const field = form.elements.contact;
    const value = field.value.trim();
    if (!/^(?:[^\s@]+@[^\s@]+\.[^\s@]+|\+?\d{9,15})$/.test(value)) {
      announce('Vui lòng nhập email hoặc số điện thoại hợp lệ');
      field.focus();
      return;
    }
    announce('Đăng ký thành công · Demo');
  });

  document.addEventListener('click', event => {
    const button = event.target.closest('button[data-action]');
    if (!button) return;
    switch (button.dataset.action) {
      case 'favorite': {
        const key = button.closest('[data-product]').dataset.product;
        const selected = !favorites.has(key);
        if (selected) favorites.add(key);
        else favorites.delete(key);
        button.setAttribute('aria-pressed', String(selected));
        announce(selected ? 'Đã thêm vào yêu thích' : 'Đã bỏ yêu thích');
        break;
      }
      case 'favorites':
        announce(`Yêu thích (${favorites.size}) · Demo`);
        break;
      case 'buy':
        announce(`Đã thêm vào giỏ hàng (${++cartCount}) · Demo`);
        break;
      case 'cart-summary':
        announce(`Giỏ hàng (${cartCount}) · Demo`);
        break;
      case 'filter': {
        const section = button.closest('[data-section]');
        section.querySelectorAll('[data-action="filter"]').forEach(filter => {
          filter.setAttribute('aria-pressed', String(filter === button));
        });
        announce(button.textContent.trim() + ' · Bộ lọc demo');
        break;
      }
      case 'previous':
      case 'next': {
        const list = button.closest('.catalog').querySelector('.products, .media-carousel');
        const direction = button.dataset.action === 'next' ? 1 : -1;
        const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
        list.scrollBy({ left: direction * list.clientWidth, behavior: reducedMotion ? 'instant' : 'smooth' });
        break;
      }
      default:
        announce((button.getAttribute('aria-label') || button.textContent.trim()) + ' · Demo');
    }
  });
})();
