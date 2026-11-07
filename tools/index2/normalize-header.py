"""Build semantic header controls and the native, initially rendered hero content."""
from pathlib import Path
from bs4 import BeautifulSoup
import re,json,base64,hashlib,xml.etree.ElementTree as ET,mimetypes
ROOT=Path(__file__).resolve().parents[2]
def decorative_header():
 source=json.loads((ROOT/'reference/index2-desktop-source.json').read_text(encoding='utf8'))[0]['background']
 root=ET.fromstring(source)
 for e in root.iter():
  for key,value in list(e.attrib.items()):
   if key.endswith('href') and value.startswith('../../assets/'):
    path=ROOT/value[6:]
    if path.name=='fcfdbbb19fa8a366fc216a4b.png':path=ROOT/'assets/index2/hero-clean.webp'
    e.set(key,'data:'+(mimetypes.guess_type(path)[0] or 'image/webp')+';base64,'+base64.b64encode(path.read_bytes()).decode())
 svg=ROOT/'assets/index2/header-decoration.svg'
 svg.write_text(ET.tostring(root,encoding='unicode'),encoding='utf8')
 digest=ROOT/'assets/index2/header-decoration.sha256'
 raster=svg.with_suffix('.webp')
 return 'assets/index2/header-decoration.webp' if raster.exists() and digest.exists() and digest.read_text().strip()==hashlib.sha256(svg.read_bytes()).hexdigest() else 'assets/index2/header-decoration.svg'
def normalize(markup):
 soup=BeautifulSoup(markup,'html.parser');header=soup.find('header')
 source_texts={t['key']:t for t in json.loads((ROOT/'reference/index2-desktop-source.json').read_text(encoding='utf8'))[0]['texts']}
 mobile_pieces=json.loads((ROOT/'reference/index2-mobile-source.json').read_text(encoding='utf8'))[0]['pieces']
 header.select_one('.desktop-art')['src']=decorative_header()
 # One native control owns its visible label at both responsive layouts.
 for piece in header.select('.layout-piece'):
  canvas=piece.select_one('.piece-canvas')
  if not canvas:continue
  classes=piece.get('class',[])
  index=next((int(c.split('-')[-1]) for c in classes if c.startswith('piece-1-')),None)
  if index==18:continue
  controls=canvas.select_one('.mobile-controls')
  if controls:
   controls.name='ul';controls['class']=['header-controls','header-items']
   for button in list(controls.select(':scope > button')):
    li=soup.new_tag('li');button.wrap(li)
  copies=canvas.select('p.copy')
  for node in copies:
   label=node.get_text(' ',strip=True)
   if not label:continue
   actionable=index in [0,1,5,6,7,8,9,10,11,12,13,14,15,16,17] or (index in [19,20,21] and label in ['Xem ngay','Khám phá ngay'])
   if not actionable:continue
   if index==1 and label=='Danh mục sản phẩm':continue
   matches=[b for b in canvas.select('button') if b.get('aria-label','')==label or (index==6 and b.get('data-action')=='heart') or (index==16 and b.get('aria-label')=='NEW SP Mới ra mắt')]
   spans=node.select('.text-run')
   def props(style):return dict(re.findall(r'(--[\w-]+):([^;]+)',style))
   positions=[props(s.get('style','')) for s in spans]
   if index==16:matches=canvas.select('button')[:1]
   if matches:
    button=matches[0]
    if not button.select('.native-control-text'):button.clear()
   else:
    button=soup.new_tag('button',type='button');button['class']=['art-control'];button['data-action']='cart box' if index==8 else 'demo';button['aria-label']=label
    p=positions[0];width=source_texts.get(node.get('data-key'),{}).get('box',{}).get('w',158)+2;button['style']=';'.join(f'{k}:{p[k]}' for k in ['--dx','--dy','--mx','--my'])+f';--dw:{width}px;--dh:36px;--mw:{width}px;--mh:36px'
    canvas.append(button)
   if index in [5,6,7,8]:
    x,y,w,h=mobile_pieces[index]['viewBox']
    button['style']=f'--dx:{x}px;--dy:{y}px;--dw:{w}px;--dh:{h}px;--mx:0px;--my:0px;--mw:{w}px;--mh:{h}px'
   button['class']=list(button.get('class',[]))+['native-header-control']
   button['aria-label']=label
   for span,p in zip(spans,positions):
    span['style']=';'.join(f'--text-{k[2:]}:{v}' for k,v in p.items())
    span['class'].append('native-control-text');button.append(span.extract());button.append(' ')
   node.decompose()
  if index in [0,1,9,10,11,12,13,14,15,16,17,22]:
   listing=soup.new_tag('ul');listing['class']=['header-items']
   for node in list(canvas.children):
    if getattr(node,'name',None) in ['p','h1','a','button']:
     li=soup.new_tag('li');li.append(node.extract());listing.append(li)
   if listing.contents:canvas.append(listing)
  if index in [19,20,21]:
   for key in {19:['t47'],20:['t59'],21:['t62']}[index]:
    node=canvas.select_one('[data-key="'+key+'"]')
    if node:node.name='h3'
   if index==21:
    listing=soup.new_tag('ul');listing['class']=['header-items']
    for key in ['t64','t65','t66']:
     node=canvas.select_one('[data-key="'+key+'"]')
     if node:li=soup.new_tag('li');li.append(node.extract());listing.append(li)
    canvas.append(listing)
 # Keep layout positions, but remove duplicate desktop action overlays.
 old=header.select_one('.desktop-controls')
 if old:old.decompose()
 # The hero is written in HTML, including all text previously burned into its PNG.
 hero=header.select_one('.piece-1-18');hero.select_one('.mobile-art')['src']='assets/index2/hero-clean-mobile.webp'
 canvas=hero.select_one('.piece-canvas');canvas.clear()
 native='''<section class="native-hero" aria-labelledby="hero-title">
 <div class="hero-surface" aria-hidden="true"></div>
 <p class="hero-brand">ROG | TUF | ZENBOOK | VIVOBOOK</p>
 <p class="hero-stock">RTX 50 SERIES · SẴN HÀNG</p>
 <h2 id="hero-title">LAPTOP <span>AI</span></h2>
 <p class="hero-tagline">KIẾN TẠO TƯƠNG LAI</p>
 <p class="hero-description">Hiệu năng đột phá | AI tăng tốc công việc | Sẵn sàng cho thế hệ mới</p>
 <ul class="hero-benefits">
 <li><span class="hero-ai" aria-hidden="true">AI</span><span>Tích hợp AI<br>hiệu suất cao</span></li>
 <li><span class="hero-laptop" aria-hidden="true"></span><span>Thiết kế mỏng nhẹ<br>sang trọng</span></li>
 <li><span class="hero-battery" aria-hidden="true"></span><span>Pin bền bỉ<br>làm việc cả ngày</span></li>
 </ul>
 <div class="hero-actions"><button type="button" data-action="demo" aria-label="Khám phá ngay">Khám phá ngay <span aria-hidden="true">→</span></button><button type="button" data-action="demo" aria-label="Tư vấn cấu hình">Tư vấn cấu hình</button></div>
 <div class="hero-pagination" role="group" aria-label="Chọn banner"><button type="button" aria-label="Banner 1" aria-pressed="true" data-hero-slide="0"></button><button type="button" aria-label="Banner 2" aria-pressed="false" data-hero-slide="1"></button><button type="button" aria-label="Banner 3" aria-pressed="false" data-hero-slide="2"></button></div>
 </section>'''
 canvas.append(BeautifulSoup(native,'html.parser'))
 # Visible search submit belongs to its form; placeholder is real input content.
 form=header.select_one('.desktop-search')
 field=form.select_one('input');field['placeholder']='Bạn cần tìm gì hôm nay? (ví dụ: Laptop ASUS, RTX 5070, Màn hình 2K...)'
 submit=form.select_one('button');submit['class']=['header-search-submit'];submit.string='Tìm kiếm'
 for key in ['t9','t10','t81','t82']:
  for node in header.select('[data-key="'+key+'"]'):node.decompose()
 # Main navigation is an actual nav landmark; the grouping preserves flex reflow.
 layout=header.select_one('.section-layout')
 nav=soup.new_tag('nav');nav['class']=['header-quick-nav'];nav['aria-label']='Điều hướng sản phẩm'
 for i in range(9,18):
  node=header.select_one('.piece-1-'+str(i))
  if node:nav.append(node.extract())
 hero.insert_before(nav)
 for b in header.select('.native-header-control'):
  if b.get('data-action')!='heart':b.attrs.pop('aria-label',None)
 return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', str(soup))
if __name__=='__main__':
 p=ROOT/'index2.html';p.write_text(normalize(p.read_text(encoding='utf8')),encoding='utf8')
