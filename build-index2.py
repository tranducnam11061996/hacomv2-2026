"""Reproduce the measured layouts with native text and decorative SVG artwork.

Run only when the captured reference geometry is deliberately updated.
The generated page itself needs no build step or framework.
"""
from pathlib import Path
import json, re, html, base64, mimetypes, math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets' / 'index2'
OUT.mkdir(exist_ok=True)
desktop = json.loads((ROOT/'reference/index2-desktop-source.json').read_text(encoding='utf-8'))
mobile = json.loads((ROOT/'reference/index2-mobile-source.json').read_text(encoding='utf-8'))
baselines = json.loads((ROOT/'reference/index2-font-baselines.json').read_text(encoding='utf-8'))
carousel_cards = json.loads((ROOT/'reference/index2-cards.json').read_text(encoding='utf-8'))
video_card_by_text={name:c['id'] for c in carousel_cards if c['section']=='19' for name in c.get('texts',[])}
video_title_ids={c['texts'][2] for c in carousel_cards if c['section']=='19' and len(c.get('texts',[]))>2}
news_title_ids={'Heading_32',*(f'Description_{i}' for i in [255,257,259,261,263,265,268,271,274,277,280])}
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
esc = lambda s: html.escape(re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]','',str(s)), quote=True)
num = lambda n: f'{n:.5f}'.rstrip('0').rstrip('.') if isinstance(n, (int,float)) else str(n)
typography={}
responsive_rules=[]
titles = {2:'NGÀNH HÀNG NỔI BẬT',3:'FLASH',4:'CHỌN ĐÚNG MÁY',5:'LAPTOP - MACBOOK',6:'PC - MINI',7:'HACOM PC BUILDER',8:'MÀN HÌNH MÁY TÍNH',9:'LINH KIỆN MÁY TÍNH',10:'GAMING GEAR',11:'CONSOLE - SIM',12:'MẠNG',13:'THIẾT BỊ VĂN PHÒNG',14:'NHÀ THÔNG MINH & GIA DỤNG',15:'KHÁCH HÀNG',16:'DỊCH VỤ TỐT',17:'HACOM IN NUMBERS',18:'CẬP NHẬT CÔNG NGHỆ MỖI NGÀY',19:'VIDEO REVIEW',20:'K H Á C H',21:'CHƯA CHẮC',22:'NHẬN ƯU ĐÃI'}

def artwork(source, filename, prefer_vector=False):
    raster=OUT/filename.replace('.svg','.webp')
    root=ET.fromstring(source)
    defs=root.find('{http://www.w3.org/2000/svg}defs')
    if defs is not None:
        by_id={n.get('id'):n for n in defs if n.get('id')}
        def refs(nodes):
            result=set()
            for node in nodes:
                for el in node.iter():
                    for k,v in el.attrib.items():
                        result.update(re.findall(r'url\(#([^)]*)\)',v))
                        if k.endswith('href') and v.startswith('#'): result.add(v[1:])
            return result
        used=refs([n for n in root if n is not defs]); todo=list(used)
        while todo:
            key=todo.pop()
            if key in by_id:
                for ref in refs([by_id[key]])-used: used.add(ref);todo.append(ref)
        for node in list(defs):
            if node.get('id') not in used: defs.remove(node)
    primitives={'path','rect','circle','ellipse','image','use','line','polyline','polygon','foreignObject'}
    if not any(el.tag.split('}')[-1] in primitives for child in root if child is not defs for el in child.iter()):return ''
    if raster.exists() and not prefer_vector:return 'assets/index2/'+raster.name
    for n in root.iter():
        for key,value in list(n.attrib.items()):
            if key.endswith('href') and value.startswith('../../assets/'):
                path=ROOT/value[6:]
                mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
                n.set(key,'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode())
        for key in list(n.attrib):
            if key.startswith('data-') or key in ('tabindex','role','aria-label','aria-hidden','inert','class'): del n.attrib[key]
    data=ET.tostring(root,encoding='unicode')
    (OUT/filename).write_text(data,encoding='utf-8')
    return 'assets/index2/'+filename

def text_html(t,n,offset=(0,0), desktop_rows=None, hidden_mobile=False):
    txt=t['text'].strip()
    if not txt:return ''
    tag='p'
    if n==1 and txt.startswith('HACOM.VN -'):tag='h1'
    elif t.get('key')==heading_keys.get(n):tag='h2'
    elif t.get('card') and t.get('id','').startswith('Product name'):tag='h3'
    elif (n==18 and t.get('id') in news_title_ids) or (n==19 and t.get('id') in video_title_ids):tag='h3'
    rows=[]
    for i,r in enumerate(t['rows']):
        d=(desktop_rows or t['rows'])[min(i,len(desktop_rows or t['rows'])-1)]
        key=f"{r['font']}|{num(r['size'])}px|{r['weight']}"
        base=baselines.get(key,r['size']*.85)
        dkey=f"{d['font']}|{num(d['size'])}px|{d['weight']}"
        db=baselines.get(dkey,d['size']*.85)
        font_style=f"font-family:{r['font']};font-size:{num(r['size'])}px;font-weight:{r['weight']};color:{r['color']};letter-spacing:{r['spacing']};opacity:{r['opacity']}"
        if font_style not in typography:typography[font_style]=f'type-{len(typography)+1}'
        style=f"--dx:{num(d['x'])}px;--dy:{num(d['y']-db)}px;--mx:{num(r['x']-offset[0])}px;--my:{num(r['y']-offset[1]-base)}px"
        rows.append(f'<span class="text-run {typography[font_style]}" style="{esc(style)}">{esc(r["text"])}</span>')
    card=t.get('card','') or (video_card_by_text.get(t.get('id',''),'') if n==19 else '')
    href=''
    if txt=='1900 1903':tag='a';href=' href="tel:19001903"'
    elif txt=='info@hacom.vn':tag='a';href=' href="mailto:info@hacom.vn"'
    elif txt=='www.hacom.vn':tag='a';href=' href="https://www.hacom.vn/"'
    return f'<{tag} class="copy{ " desktop-only" if hidden_mobile else ""}" data-card="{esc(card)}" data-key="{esc(t.get("key",""))}"{href}>{" ".join(rows)}</{tag}>'

def controls(actions, offset=(0,0), desktop_actions=None):
    out=[]
    seen=set()
    for i,a in enumerate(actions):
        b=a['box']; d=(desktop_actions[i]['box'] if desktop_actions and i<len(desktop_actions) else b)
        if b['w']<=0 or b['h']<=0:continue
        location=tuple(round(b[k],1) for k in ('x','y','w','h'))
        if location in seen:continue
        seen.add(location)
        # Expand invisible hit areas within the existing row; artwork stays unchanged.
        minimum=36
        if d['h']<minimum:d=dict(d,y=d['y']-(minimum-d['h'])/2,h=minimum)
        if d['w']<minimum:d=dict(d,x=d['x']-(minimum-d['w'])/2,w=minimum)
        style=f"--dx:{num(d['x'])}px;--dy:{num(d['y'])}px;--dw:{num(d['w'])}px;--dh:{num(d['h'])}px;--mx:{num(b['x']-offset[0])}px;--my:{num(b['y']-offset[1])}px;--mw:{num(b['w'])}px;--mh:{num(b['h'])}px"
        pressed=' aria-pressed="false"' if a['kind'].lower().startswith('heart') else ''
        if pressed:style+=f';--icon-w:{num(b["w"]+2)}px;--icon-h:{num(b["h"]+2)}px'
        name='Thêm vào yêu thích' if pressed else a['name'] or 'Xem thêm'
        if 'chevron-forward-circle-outline' in a['kind']:name='Chuyển nội dung'
        out.append(f'<button type="button" class="art-control" style="{style}" data-action="{esc(a["kind"])}" data-card="{esc(a.get("card",""))}" aria-label="{esc(name)}"{pressed}></button>')
    return ''.join(out)

parts=['<!doctype html>','<html lang="vi">','<head>','  <meta charset="utf-8">','  <meta name="viewport" content="width=device-width, initial-scale=1">','  <title>HACOM - Laptop, PC Gaming và thiết bị công nghệ</title>','  <meta name="description" content="Khám phá laptop, PC Gaming, linh kiện máy tính và thiết bị công nghệ tại HACOM. Tìm hiểu sản phẩm, giải pháp công nghệ và hệ thống showroom toàn quốc.">','  <link rel="stylesheet" href="assets/faithful/fonts.css">','  <link rel="stylesheet" href="index2.css">','  <script src="index2.js" defer></script>','</head>','<body>','<div class="page">']
heading_keys={s['number']:next((t['key'] for t in s['texts'] if titles.get(s['number'],'NOT A TITLE') in t['text'].strip()),None) for s in desktop}
for s,m in zip(desktop,mobile):
    n=s['number'];top=s['top'];h=s['height']; tag='header' if n==1 else 'footer' if n==22 else 'section'
    if n==2:parts.append('<main id="main-content">')
    if n==22:parts.append('</main>')
    section_cards=[{k:c[k] for k in ('id','x','y','w','h','image')} for c in carousel_cards if int(c['section'])==n]
    parts.append(f'<{tag} class="design-section" aria-label="{esc(s["title"])}" data-section="{n}" data-cards="{esc(json.dumps(section_cards,ensure_ascii=False,separators=(",",":")))}" style="--section-height:{h}">')
    bg=artwork(s['background'],f'desktop-{n:02}.svg')
    parts.append(f'  <img class="desktop-art" src="{bg}" alt="" aria-hidden="true" width="1920" height="{h}" loading="{"eager" if n==1 else "lazy"}">')
    parts.append('  <div class="section-layout">')
    bykey={t['key']:t for t in s['texts']};used=set()
    product_list_open=False
    for i,p in enumerate(m['pieces']):
        if 'background' not in p:
            reflow_threshold=''
            special=p['html'].replace('type="checkbox"','type="checkbox" checked')
            heading=next((t for t in s['texts'] if t['key']==heading_keys.get(n)),None)
            plain=html.unescape(re.sub('<[^>]+>','',special))
            if heading and re.sub(r'\s+',' ',heading['text']).strip() in re.sub(r'\s+',' ',plain).strip():
                special=special.replace('<p ','<h2 ',1).replace('</p>','</h2>',1)
            match=next((t for t in s['texts'] if re.sub(r'\s+','',t['text'])==re.sub(r'\s+','',plain)),None) if '<form' not in special else None
            special_class=f'special-{n}-{i}'
            if match:
                box=match['box'];fw=math.ceil(box['w']);fh=math.ceil(box['h'])
                reflow_threshold=f' data-reflow-threshold="{num(box["w"]+32)}"'
                fixed=f'<div class="flow-fixed layout-piece" style="--piece-width:{fw}px;--piece-height:{fh}px"><div class="piece-canvas" style="--canvas-width:{fw}px">'+text_html(match,n,(box['x'],box['y']))+'</div></div>'
                special+=fixed
                responsive_rules.append(f'@media(max-width:1023px){{.{special_class}>.flow-fixed{{display:none}}}}@container(min-width:{num(box["w"]+32)}px){{@media(max-width:1023px){{.{special_class}>.reflow-copy{{display:none}}.{special_class}>.flow-fixed{{display:block}}}}}}')
            parts.append(f'<div class="mobile-special {special_class}"{reflow_threshold}>'+special+'</div>');continue
        x,y,w,vh=p['viewBox'];pw=p['width'];ph=p['height']
        bg=artwork(p['background'],f'mobile-{n:02}-{i:02}.svg',prefer_vector=(pw<=500 and ph<=200))
        cards={bykey[t['key']]['card'] for t in p['texts'] if t.get('key') in bykey and bykey[t['key']]['card']}
        card=next(iter(cards)) if len(cards)==1 else ''
        if card and not product_list_open:parts.append('<ul class="product-list" aria-label="Sản phẩm">');product_list_open=True
        if not card and product_list_open:parts.append('</ul>');product_list_open=False
        piece_tag='li' if card else 'div';canvas_tag='article' if card else 'div'
        piece_class=f'piece-{n}-{i}'
        cls='layout-piece '+piece_class+(' product-card' if card else '')+(' fit-piece' if p['fit'] else '')+(' menu-piece' if p['menu'] else '')
        reflow_threshold=''
        if n==15 and len(p['texts'])==1 and p['texts'][0]['text'].strip()=='KHÁCH HÀNG TIÊU BIỂU':
            reflow_threshold=f' data-reflow-threshold="{num(w+32)}"'
            responsive_rules.append(f'@container(max-width:{num(w+31.999)}px){{@media(max-width:1023px){{.{piece_class}{{width:auto;height:auto!important;overflow:visible}}.{piece_class}>.piece-canvas{{width:auto;height:auto!important}}.{piece_class} .copy{{position:relative;inset:auto;width:auto;height:auto}}.{piece_class} .text-run{{position:static;white-space:normal;line-height:1.5}}}}}}')
        if p['menu']:parts.append('<nav class="department-nav" aria-label="Danh mục sản phẩm"><details class="department-menu"><summary>Danh mục sản phẩm</summary>')
        parts.append(f'<{piece_tag} class="{cls}" data-card="{esc(card)}"{reflow_threshold} style="--piece-width:{pw}px;--piece-height:{ph}px;--piece-ratio:{pw}/{ph};--art-x:{num(x)}px;--art-y:{num(y-top)}px">')
        image=f'<img class="mobile-art" src="{bg}" alt="" aria-hidden="true" width="{pw}" height="{ph}" loading="lazy">' if bg else ''
        if p['fit']:parts.append(image)
        parts.append(f'<{canvas_tag} class="piece-canvas" style="--canvas-width:{pw}px">')
        if not p['fit']:parts.append(image)
        current_card=''
        for t in p['texts']:
            original=bykey.get(t.get('key'))
            if not original:continue
            if t['key'] in used:continue
            group_card=original['card'] if not card else ''
            if group_card!=current_card:
                if current_card:parts.append('</article></li></ul>')
                if group_card:parts.append('<ul class="product-list"><li class="product-content"><article>')
                current_card=group_card
            used.add(t['key']);dr=[dict(r,y=r['y']-top) for r in original['rows']]
            if n==3 and original['key']==heading_keys.get(3):
                sale=next((t2 for t2 in p['texts'] if t2['text'].strip()=='SALE'),None)
                if sale:
                    sale_original=bykey[sale['key']];used.add(sale['key'])
                    t=dict(t,rows=t['rows']+sale['rows'],text=t['text']+' '+sale['text'])
                    dr.extend(dict(r,y=r['y']-top) for r in sale_original['rows'])
            parts.append(text_html(dict(t,card=original['card'],id=original['id']),n,(x,y),dr))
        if current_card:parts.append('</article></li></ul>')
        # Mobile controls are native buttons; desktop controls are added once below.
        parts.append('<div class="mobile-controls">'+controls(p['actions'],(x,y))+'</div>')
        parts.append(f'</{canvas_tag}></{piece_tag}>')
        if p['menu']:parts.append('</details></nav>')
    if product_list_open:parts.append('</ul>')
    # Text omitted by the original mobile reflow remains available on desktop.
    for t in s['texts']:
        if t['key'] not in used:
            t=dict(t,rows=[dict(r,y=r['y']-top) for r in t['rows']]);parts.append(text_html(t,n,hidden_mobile=True))
    da=[dict(a,box=dict(a['box'],y=a['box']['y']-top)) for a in s['actions']]
    parts.append('<div class="desktop-controls">'+controls(da)+'</div>')
    parts.append('</div>')
    if n==1:
        parts.append('<form class="desktop-search" role="search" aria-label="Tìm kiếm sản phẩm"><label class="sr-only" for="desktop-search">Tìm kiếm sản phẩm</label><input id="desktop-search" name="search" required aria-label="Tìm kiếm sản phẩm"><button class="sr-only" type="submit">Tìm kiếm</button></form>')
    if n==22:
        parts.append('<form class="desktop-newsletter" aria-label="Đăng ký nhận tin"><label class="sr-only" for="desktop-contact">Email hoặc số điện thoại</label><input id="desktop-contact" name="contact" required aria-label="Email hoặc số điện thoại"><label class="consent"><input name="consent" type="checkbox" checked required><span class="sr-only">Tôi đồng ý nhận thông tin từ HACOM</span></label><button class="sr-only" type="submit">Đăng ký ngay</button></form>')
    parts.append(f'</{tag}>')
parts+=['</div>','<div id="demo-status" role="status" aria-live="polite" hidden></div>','</body>','</html>']
import runpy
normalize_header=runpy.run_path(str(ROOT/'tools/index2/normalize-header.py'))['normalize']
(ROOT/'index2.html').write_text(normalize_header('\n'.join(parts)+'\n'),encoding='utf-8')
css_path=ROOT/'index2.css'
base_css=css_path.read_text(encoding='utf-8').split('/* Generated typography tokens. */')[0].rstrip()
tokens='\n'.join('.'+name+'{'+style+'}' for style,name in typography.items())
css_path.write_text(base_css+'\n\n/* Generated typography tokens. */\n'+tokens+'\n\n/* Measured text reflow thresholds. */\n'+'\n'.join(responsive_rules)+'\n',encoding='utf-8')
print('Generated index2.html with',len(list(OUT.glob('*.webp'))),'lossless graphics')

# The active favorite uses the original vector path, rather than a replacement glyph.
raw=(ROOT/'assets/faithful/03.js').read_text(encoding='utf-8')
svg=ET.fromstring(json.loads(raw[raw.index(',')+1:raw.rfind(')')].strip()))
heart=next(e for e in svg.iter() if e.get('id')=='heart_2')
active=ET.Element('{http://www.w3.org/2000/svg}svg',{'viewBox':'298.163 1907.33667 20.33032 17.59448'})
for path in heart:
    path.attrib.pop('id',None);path.set('fill','#ed1c24');path.set('stroke','#ed1c24');active.append(path)
(OUT/'favorite-active.svg').write_text(ET.tostring(active,encoding='unicode'),encoding='utf-8')
