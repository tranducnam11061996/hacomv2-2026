const F=n=>`assets/figma/${n}.png`;
const S=[...document.querySelectorAll('#content>section')];
const photo=(n,cls='',alt='')=>`<img src="${F(n)}" width="600" height="400" loading="lazy" alt="${alt}" class="${cls}">`;
const svg=(kind='arrow')=>`<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">${({arrow:'<path d="M4 12h16m-6-6 6 6-6 6"/>',search:'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',box:'<path d="m3 7 9-5 9 5v11l-9 4-9-4V7Zm0 0 9 5 9-5M12 12v10"/>',menu:'<path d="M3 6h18M3 12h18M3 18h18"/>',camera:'<path d="M3 6h5l2-3h4l2 3h5v14H3Z"/><circle cx="12" cy="13" r="4"/>',mic:'<rect x="9" y="2" width="6" height="13" rx="3"/><path d="M5 10v2a7 7 0 0 0 14 0v-2M12 19v4"/>'})[kind]||'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8m-4-4v4"/>'}</svg>`;
const tile=(name,n,extra='')=>`<a href="#" class="art-tile ${extra}" style="background-image:url('${F(n)}')"><h3>${name}</h3><span class="round-arrow">${svg()}</span></a>`;
const sectionGrid=(idx,cls,html)=>{const sec=S[idx];const head=sec.firstElementChild;sec.innerHTML='';sec.append(head);sec.insertAdjacentHTML('beforeend',`<div class="${cls}">${html}</div>`)};
// Product art is now explicitly assigned by category, never by cyclic offsets.
const productSources={};document.querySelectorAll('.product-row').forEach((row,idx)=>{const kind=['flash','laptop','pc','monitor','office'][idx];row.dataset.category=kind;if(kind==='monitor')row.querySelectorAll('img').forEach((im,i)=>{im.src=F([4,5,6,52,51,3][i]);im.alt=['Màn hình Gaming','Màn hình đồ họa','Màn hình văn phòng','Màn hình OLED','Màn hình cong','Giá treo màn hình'][i];im.closest('article').querySelector('h3').textContent=im.alt});if(kind==='office')row.querySelectorAll('img').forEach(im=>{im.src=F(53);im.alt='Thiết bị văn phòng';im.closest('article').querySelector('h3').textContent='Thiết bị văn phòng chính hãng'});});
const hero = document.querySelector('.hero-bg');
hero.classList.add('figma-hero');
hero.innerHTML = `
  <img src="assets/figma/header-3.png" width="1035" height="663"
    fetchpriority="high" alt="Laptop AI — Kiến tạo tương lai. Tích hợp AI, thiết kế mỏng nhẹ, pin bền bỉ.">
  <a class="hero-discover" href="#">Khám phá ngay ${svg()}</a>
  <a class="hero-consult" href="#" aria-label="Tư vấn cấu hình"></a>
`;

const side = document.querySelector('#hero-side');
side.classList.add('figma-promos');
side.innerHTML = `
  <a href="#" class="figma-promo flash-promo">
    <h3>FLASH SALE</h3><p>GIỜ VÀNG GIÁ SỐC</p>
    <div class="promo-clock">${[['09','Giờ'],['24','Phút'],['12','Giây']].map(([number,label])=>`<span><b>${number}</b><small>${label}</small></span>`).join('')}</div>
    <span class="promo-link">Xem ngay ${svg()}</span>
  </a>
  <a href="#" class="figma-promo rtx-promo">
    <h3>RTX 50 SERIES</h3><p>SỨC MẠNH KIẾN TẠO TƯƠNG LAI</p>
    <img src="assets/figma/header-4.png" alt="NVIDIA GeForce RTX" width="448" height="135">
    <span class="promo-link">Khám phá ngay ${svg()}</span>
  </a>
  <a href="#" class="figma-promo gaming-promo">
    <h3>LAPTOP GAMING</h3><p>HIỆU NĂNG ĐỈNH CAO</p>
    <ul><li>Trả góp 0% lãi suất</li><li>Bảo hành chính hãng</li><li>Giao hàng toàn quốc</li></ul>
    <span class="promo-link">Xem ngay ${svg()}</span>
  </a>
`;
document.querySelectorAll('img[src*="hacom-ccb5b48363"]').forEach(image=>{
  image.src='assets/figma/header-15.png';
  image.width=289;
  image.height=110;
});
// Distinct category compositions.
sectionGrid(7,'parts-grid',tile('CPU',41)+tile('Mainboard',40)+tile('VGA - Card đồ họa',33)+tile('RAM',34)+tile('VỎ CASE · KIẾN TẠO PHONG CÁCH RIÊNG CỦA BẠN',35,'parts-feature')+tile('SSD',39)+tile('HDD',38)+tile('PSU - Nguồn',36)+tile('Tản nhiệt',37));
sectionGrid(8,'gear-grid',tile('NÂNG TẦM TRẢI NGHIỆM GAME',7,'gear-feature')+tile('CHUỘT GAMING',22)+tile('BÀN PHÍM GAMING',24)+tile('TAI NGHE GAMING',26)+tile('MICRO GAMING',23)+tile('GHẾ GAMING',25)+tile('PHỤ KIỆN GAMING',9));
sectionGrid(9,'console-grid',tile('PLAYSTATION',8,'console-feature')+tile('XBOX',27)+tile('NINTENDO',30)+tile('STEAM DECK',28)+tile('SIM RACING',29)+tile('VR',10)+tile('TAY CẦM',31)+tile('PHỤ KIỆN CONSOLE',17));
sectionGrid(10,'network-grid',tile('BỘ PHÁT WIFI',11,'network-wide')+tile('THIẾT BỊ CHIA MẠNG - SWITCH',12)+tile('ACCESS POINT',13)+tile('BỘ MESH WIFI',19,'network-tall')+tile('Ổ CỨNG DI ĐỘNG',21)+tile('USB',20)+tile('PHẦN MỀM BẢN QUYỀN',18)+tile('BẢO MẬT & ANTIVIRUS',14));
// Laptop: left banner, brands and compact needs at right.
const laptop=S[3];let laptopBanner=laptop.querySelector('.card-gradient');laptopBanner.className='laptop-banner';laptopBanner.innerHTML=photo(0,'w-full h-full','Laptop AI');laptopBanner.insertAdjacentHTML('afterend',`<div class="laptop-brands"><div class="brand-row">${['ASUS','msi','Lenovo','DELL','acer','Apple','Microsoft'].map(n=>`<a href="#">${n}</a>`).join('')}</div><div class="copilot">Copilot+ PC thế hệ mới đã có mặt tại HACOM</div><div class="needs">${['Laptop mỏng nhẹ','Laptop Gaming','Laptop AI','Laptop Đồ họa','Tablet','Phụ kiện Laptop'].map(n=>`<a href="#">${svg('monitor')}<b>${n}</b></a>`).join('')}</div></div>`);const split=document.createElement('div');split.className='laptop-split';laptop.insertBefore(split,laptopBanner);split.append(laptopBanner,laptop.querySelector('.laptop-brands'));
// PC builder is the original wide artwork, with live copy retained.
[S[4],S[5]].forEach((sec,i)=>{let b=sec.querySelector('.card-gradient');b.classList.add('original-banner');b.style.backgroundImage=`linear-gradient(90deg,#06080bc9,transparent),url('${F(2)}')`;b.querySelector('img')?.remove()});
const monitor=S[6].querySelector('.card-gradient');monitor.style.backgroundImage=`linear-gradient(90deg,#eee 0%,#eeea 35%,transparent),url('${F(52)}')`;monitor.style.color='#131b34';monitor.querySelector('img').remove();monitor.insertAdjacentHTML('afterend',`<div class="monitor-types">${['Màn hình 24 inch','Màn hình 27 inch','Màn hình 32 inch','Màn hình 34 inch','Màn hình cong','Màn hình theo hãng'].map((n,i)=>`<a href="#">${photo([4,5,6,52,51,3][i],'',n)}<b>${n}</b></a>`).join('')}</div>`);
const office=S[11].querySelector('.card-gradient');office.style.backgroundImage=`linear-gradient(90deg,#06111bcc,transparent),url('${F(15)}')`;office.querySelector('img').remove();
sectionGrid(12,'smart-grid',`<div><h3>NHÀ THÔNG MINH<br><em>CUỘC SỐNG TIỆN NGHI</em></h3><p>An toàn hơn mỗi ngày</p><div class="smart-cards">${[['Camera quan sát',47],['Báo cháy',46],['Khóa cửa thông minh',48]].map(x=>`<a href="#">${photo(x[1],'',x[0])}<b>${x[0]}</b></a>`).join('')}</div></div><div><h3>SẢN PHẨM NỔI BẬT</h3><div class="smart-cards">${[['Tivi',43],['Điều hòa',44],['Máy pha cafe',45],['Tủ lạnh',49],['Máy giặt',50]].map(x=>`<a href="#">${photo(x[1],'',x[0])}<b>${x[0]}</b></a>`).join('')}</div></div>`);S[12].querySelector('.smart-grid').style.backgroundImage=`url('${F(42)}')`;
const enterprise=S[13].querySelector('.card-gradient');enterprise.style.backgroundImage=`linear-gradient(90deg,#ddeeff,transparent),url('${F(16)}')`;enterprise.style.color='#111b38';enterprise.querySelector('img').remove();S[13].insertAdjacentHTML('beforeend',`<h3 class="minor-title">CÁC NHÓM DỊCH VỤ CHÍNH</h3><div class="service-groups">${[['LAPTOP & MÁY TÍNH VĂN PHÒNG',53],['SERVER & STORAGE',54],['THIẾT BỊ MẠNG & WIFI',61],['CAMERA GIÁM SÁT & AN NINH',56],['THIẾT BỊ HỘI HỌP & TRÌNH CHIẾU',57],['PHẦN MỀM & BẢN QUYỀN',59],['AI WORKSTATION & GPU SERVER',60],['HẠ TẦNG DATA CENTER',55]].map(x=>`<a href="#">${photo(x[1],'',x[0])}<b>${x[0]}</b></a>`).join('')}</div>`);
const repair=S[14].querySelector('.card-gradient');repair.style.backgroundImage=`linear-gradient(90deg,#fff 20%,transparent),url('${F(58)}')`;repair.style.color='#111b38';repair.querySelector('img').remove();S[14].insertAdjacentHTML('beforeend','<div class="process">QUY TRÌNH DỊCH VỤ　　01 Tiếp nhận thiết bị　 ›　02 Báo giá chi tiết　 ›　03 Sửa chữa / Xử lý　 ›　04 Kiểm tra & bàn giao</div>');
S[17].querySelectorAll('a').forEach((a,i)=>{const div=a.firstElementChild;div.className='video-image';div.innerHTML=photo([68,67,65,66,64,63][i],'','Video HACOM')});
const news=S[16].querySelector('.grid');news.classList.add('news-layout');
[69,70,73,72,71].forEach((n,i)=>{const a=S[19].children[i];a.classList.add('channel-card');a.style.backgroundImage=`url('${F(n)}')`;a.innerHTML=`<span class="sr-only">${a.textContent}</span><span class="channel-cta">Khám phá ngay →</span>`});
const showroomNames=['Hai Bà Trưng','Đống Đa','Hải Phòng','Cầu Giấy','Hà Đông 1','Long Biên','Từ Sơn','Đông Anh','Bắc Giang','Hà Đông 2','Phủ Lý','Vinh','Thái Nguyên','Thanh Hóa','Cầu Giấy 2','Gia Lâm','Gia Lâm 2','Định Công','Thủ Đức, TP. HCM','Gò Vấp, TP. HCM'];document.querySelector('#showrooms').innerHTML=showroomNames.map((n,i)=>`<a href="#"><strong>${String(i+1).padStart(2,'0')}</strong> HACOM - ${n} <span>+</span></a>`).join('');
document.querySelector('footer').insertAdjacentHTML('beforeend','<div class="footer-extra"><div><b>KẾT NỐI CÙNG HACOM</b><p>Facebook　YouTube　TikTok　Instagram　Zalo</p></div><div><b>THANH TOÁN AN TOÀN, TIỆN LỢI</b><p>VISA　Mastercard　VNPAY　MoMo　ZaloPay</p></div><div><b>CHỨNG NHẬN & ĐỐI TÁC</b><p>Microsoft　ASUS　acer　intel</p></div></div>');
// Focus trapping and breakpoint synchronization.
drawer.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const els=[...drawer.querySelectorAll('button,a')],first=els[0],last=els.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}});const mq=matchMedia('(max-width:767px)');mq.addEventListener('change',()=>document.querySelectorAll('.footer-links').forEach(d=>d.open=!mq.matches));matchMedia('(min-width:1280px)').addEventListener('change',e=>{if(e.matches&&drawer.classList.contains('open'))closeMenu()});
// Named images for each card replace the former positional image selection.
const categoryArt=['header-19','header-20',2,10,53,4,'header-12','header-13',24,26,11,18,25,37];S[0].querySelectorAll('.category-grid>a:not(.wide)').forEach((a,i)=>{a.querySelector('img').src=F(categoryArt[i]);a.querySelector('img').alt=a.querySelector('b').textContent;});
const laptopPhotos=assets.products.filter(x=>/\/(ltac|ltlv|ltms)/.test(x));const pcPhotos=assets.products.filter(x=>/\/pcgm/.test(x));document.querySelectorAll('.product-row').forEach(row=>{const kind=row.dataset.category;row.querySelectorAll('article').forEach((a,i)=>{const im=a.querySelector('img'),h=a.querySelector('h3');if(kind==='laptop'||kind==='pc'){let src=(kind==='laptop'?laptopPhotos:pcPhotos)[i];if(src){im.src=src;im.alt=productNames[src]||kind;h.textContent=im.alt}}if(kind==='flash'){const src=[laptopPhotos[0],pcPhotos[0],F(33),F(4),F(26),F(47)][i];im.src=src;const titles=['Laptop Gaming','PC Gaming','Card đồ họa GeForce RTX','Màn hình Gaming','Tai nghe Gaming','Camera quan sát'];im.alt=titles[i];h.textContent=titles[i]}})});
// Add the detail strips visible in the reference.
S[1].insertAdjacentHTML('beforeend',`<div class="flash-categories"><b>DANH MỤC FLASH SALE</b>${['Laptop','PC Gaming','VGA - Card đồ họa','Màn hình','Phụ kiện Gaming','Thiết bị văn phòng'].map(n=>`<a href="#">${svg('monitor')}${n} ›</a>`).join('')}</div>`);
const icons=['monitor','box','camera','mic'];document.querySelectorAll('#benefits>div>span:first-child').forEach((e,i)=>e.innerHTML=svg(icons[i%4]));document.querySelectorAll('#desktop-items a>span:first-child,#drawer-items a>span:first-child').forEach(e=>{e.innerHTML=e.innerHTML.replace('◈',svg('monitor'))});document.querySelector('#search>span').innerHTML=svg('search');document.querySelector('#query').insertAdjacentHTML('afterend',`<button type="button" class="search-extra" aria-label="Tìm bằng hình ảnh">${svg('camera')}</button><button type="button" class="search-extra" aria-label="Tìm bằng giọng nói">${svg('mic')}</button>`);document.querySelectorAll('.search-extra').forEach(b=>b.addEventListener('click',()=>toast('Tính năng demo')));
const careerCopy=[['Học tập hiệu quả','Lập trình, làm đồ án','Sẵn sàng cho tương lai'],['Hiệu năng đỉnh cao','Chiến mọi tựa Game','Trải nghiệm mượt mà'],['Làm việc hiệu quả','Di chuyển linh hoạt','Cân bằng cuộc sống'],['Thiết kế chuyên nghiệp','Màu sắc chuẩn xác','Sáng tạo không giới hạn'],['Dựng phim mượt mà','Xử lý video 4K/8K','Hiệu ứng chuyên nghiệp'],['Thiết kế không gian','Render nhanh, mượt','Kiến tạo không gian sống'],['AI, Machine Learning','Xử lý dữ liệu lớn','Đón đầu xu hướng'],['Livestream mượt mà','Thu hút mọi ánh nhìn','Sáng tạo chuyên nghiệp']];S[2].querySelectorAll('a').forEach((a,i)=>{a.querySelector('p').textContent=careerCopy[i].join(' · ')});
const saleHeader=S[1].firstElementChild;saleHeader.classList.add('flash-header');saleHeader.querySelector('b').innerHTML='<span>05</span> : <span>32</span> : <span>18</span>';
