"""Render the static storefront from the captured content fixtures."""
from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
REF = ROOT / 'reference'
IMAGE_MANIFEST = ROOT / 'tools/index2/content-images.json'
UI_ARTWORK = {
    '0572b922c75f142561342af4', '65db706c653148c97b0c8613',
    '6f9819d3cbe4aa6e04a1344d', '6fbed8f1e3c215f6cd6e3c1e',
    'a3c44929d193910aa003469a', 'aa9304e49fe7108f1ccf4daf',
    'ab08a6231d2808489ec28441', 'ba0e89dfe4c28a10b5795675',
    'd41998771353696f26139df4', 'eefc0e9968e5997631705733',
}
IMAGE_INFO = {}



def fixture(name):
    return json.loads((REF / f'index2-{name}.json').read_text(encoding='utf-8'))


def clean(value):
    return ' '.join(value.split())


def label(value):
    return escape(clean(value))


def button(value, action='demo', extra=''):
    return f'<button type="button" data-action="{action}"{extra}>{label(value)}</button>'


def image(path, alt='', eager=False):
    priority = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    src, width, height = IMAGE_INFO.get(path, (path, None, None))
    dimensions = f' width="{width}" height="{height}"' if width else ''
    return f'<img src="{escape(src)}" alt="{escape(alt)}"{dimensions} {priority}>'


def source_images(svg):
    """Follow only SVG references reachable from the visible artwork."""
    root = ET.fromstring(svg)
    ids = {node.get('id'): node for node in root.iter() if node.get('id')}
    pending = [node for node in root if not node.tag.endswith('}defs')]
    visited, paths = set(), {}
    while pending:
        node = pending.pop()
        if node in visited:
            continue
        visited.add(node)
        pending.extend(reversed(list(node)))
        for key, value in node.attrib.items():
            if key.endswith('href') and value.startswith('../../assets/'):
                if Path(value).stem not in UI_ARTWORK:
                    paths[value[6:]] = None
            refs = re.findall(r'url\(#([^)]*)\)', value)
            if key.endswith('href') and value.startswith('#'):
                refs.append(value[1:])
            pending.extend(ids[ref] for ref in refs if ref in ids)
    return list(paths)


ICONS = {
    'menu': 'M4 6h16M4 12h16M4 18h16',
    'search': 'M16 16l5 5M18 11a7 7 0 1 1-14 0 7 7 0 0 1 14 0',
    'camera': 'M3 7h4l2-3h6l2 3h4v13H3zM15 13a3 3 0 1 1-6 0 3 3 0 0 1 6 0',
    'mic': 'M9 5a3 3 0 0 1 6 0v7a3 3 0 0 1-6 0zM5 11v1a7 7 0 0 0 14 0v-1M12 19v4',
    'user': 'M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0M4 22v-2a8 8 0 0 1 16 0v2',
    'heart': 'M12 21 3 12C-2 6 6 1 12 7c6-6 14-1 9 5z',
    'scale': 'M12 3v18M7 21h10M3 7h18M6 7l-4 8h8zm12 0-4 8h8z',
    'cart': 'M2 3h3l3 13h11l3-9H6m4 13h1m6 0h1',
    'pin': 'M12 22S5 14 5 9a7 7 0 0 1 14 0c0 5-7 13-7 13zM14 9a2 2 0 1 1-4 0 2 2 0 0 1 4 0',
    'crown': 'm2 6 5 4 5-7 5 7 5-4-3 13H5z',
    'laptop': 'M5 4h14v12H5zM2 20h20l-3-4H5z',
    'screen': 'M3 4h18v13H3zM12 17v4m-5 0h10',
    'chip': 'M6 6h12v12H6zM9 9h6v6H9zM2 9h4m-4 6h4m12-6h4m-4 6h4M9 2v4m6-4v4m-6 12v4m6-4v4',
    'server': 'M6 3h12v18H6zM9 7h6m-6 4h6m-6 6h1',
    'game': 'M7 6h10c3 0 5 6 5 10s-4 2-6 0H8c-2 2-6 4-6 0S4 6 7 6zm0 4v5m-2-2h4m6-1h1m2 2h1',
    'flash': 'm14 2-10 12h7l-1 8 10-12h-7z',
    'battery': 'M8 5h8v16H8zM10 2h4v3m-3 4h2m-2 3h2m-2 3h2',
    'keyboard': 'M2 6h20v12H2zM5 10h2m2 0h2m2 0h2m2 0h2M7 14h10',
    'network': 'M10 2h4v5h-4zM3 17h5v5H3zm13 0h5v5h-5zM12 7v5H5v5m7-5h7v5',
    'wifi': 'M2 8a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0m-10 4a5 5 0 0 1 6 0m-3 3h.01',
    'printer': 'M6 8V3h12v5M6 17H3V8h18v9h-3M6 14h12v7H6z',
    'home': 'm2 11 10-8 10 8m-3-2v12H5V9m5 12v-7h4v7',
    'tool': 'm14 6 4 4 4-4c1 6-2 9-7 8l-8 8-4-4 8-8c-1-5 3-8 8-7z',
    'fan': 'M12 12c-8-9 4-13 3-4l-3 4c11-5 11 8 4 5l-4-5c-2 12-12 5-6 1z',
    'apple': 'M12 8c-9-6-12 7-5 13 2 2 3 0 5 0s3 2 5 0c7-6 4-19-5-13zm0 0c0-4 2-5 5-6',
    'cable': 'M6 2v5m-2 0h4v4H4zm2 4v6a4 4 0 0 0 8 0v-5m-2-4h4v4h-4zm2-6v6',
    'grid': 'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z',
    'chevron': 'm9 5 7 7-7 7',
    'truck': 'M2 5h13v12H2zM15 9h4l3 4v4h-7M5 17v3h3v-3m9 0v3h3v-3',
    'shield': 'M12 2l8 4v6c0 5-8 10-8 10S4 17 4 12V6zM8 12l3 3 5-6',
    'percent': 'M4 20 20 4M7 4a3 3 0 1 0 0 6 3 3 0 0 0 0-6m10 10a3 3 0 1 0 0 6 3 3 0 0 0 0-6',
    'box': 'm3 7 9-5 9 5v10l-9 5-9-5zM3 7l9 5 9-5m-9 5v10',
    'store': 'M4 10v11h16V10M2 10l3-7h14l3 7zM9 21v-7h6v7',
    'gift': 'M3 8h18v4H3zM5 12h14v9H5zM12 8v13m0-13C4 8 5 2 8 3c2 0 4 5 4 5s2-5 4-5c3-1 4 5-4 5',
    'phone': 'M3 14v-2a9 9 0 0 1 18 0v2M3 13h4v7H3zm14 0h4v7h-4zm4 7-4 2h-4',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="{ICONS[name]}"/></svg>'


def render_header(section, mobile):
    values = {row['key']: row['text'] for row in section['texts']}

    def value(index):
        return label(values[f't{index}'])

    def control(i, symbol=None, action='demo'):
        glyph = icon(symbol) if symbol else ''
        caption = '<br>'.join(label(line) for line in values[f't{i}'].splitlines()) if 5 <= i <= 8 else value(i)
        return f'<button type="button" data-action="{action}">{glyph}<span>{caption}</span></button>'

    utility_icons = ('cart','pin','pin','pin','pin','search','phone','user')
    utility = ''.join(control(i, symbol) for i, symbol in enumerate(utility_icons, 1))
    account = ''.join(control(i, symbol, {44:'favorites',46:'cart-summary'}.get(i,'demo'))
                      for i, symbol in enumerate(('user','heart','scale','cart'),43))
    category_icons = dict(zip(range(12,33), ('shield','apple','laptop','server','screen','tool','chip','screen','keyboard','network','game','phone','camera','printer','store','wifi','home','cable','tool','box','fan')))

    def menu_item(i):
        target = {14:5,15:6,17:7,18:9,19:8,20:10,21:12,22:11,25:13,27:12,28:14,30:16}.get(i)
        content = f'{icon(category_icons[i])}<span>{value(i)}</span>{icon("chevron")}'
        control = f'<a href="#section-{target}">{content}</a>' if target else f'<button type="button" data-action="demo">{content}</button>'
        featured = ' class="featured"' if i == 17 else ''
        return f'<li{featured}>{control}</li>'

    menu = ''.join(menu_item(i) for i in [*range(12, 21), 32, *range(21, 32)])
    benefits = ''.join(
        f'<li>{icon(symbol)}<div><strong>{value(i if i != 79 else 80)}</strong><small>{value(i+1 if i != 79 else 79)}</small></div></li>'
        for i, symbol in zip(range(67, 81, 2), ('truck','shield','percent','box','store','gift','phone'))
    )
    promo = []
    for piece, title, subtitle, cta in ((19,47,48,49),(20,59,60,58),(21,62,63,61)):
        photos = source_images(mobile['pieces'][piece]['background'])
        if piece == 19:
            info = '<div class="promo-clock">' + ''.join(
                f'<span><b>{value(i)}</b>{value(i+1)}</span>' for i in (50,52,54)
            ) + '</div>'
        elif piece == 20:
            info = image('assets/faithful/media/e56bf8eaf512e13f70f4dcd7.png', 'NVIDIA GeForce RTX')
        else:
            info = '<ul>' + ''.join(f'<li>{value(i)}</li>' for i in range(64,67)) + '</ul>'
        flash_icon = icon('flash') if piece == 19 else ''
        promo.append(f'<article class="promo">{image(photos[0])}<div>{flash_icon}<h3>{value(title)}</h3><strong>{value(subtitle)}</strong>{info}{button(values[f"t{cta}"] + " →")}</div></article>')

    quick_targets = {33:3, 36:6, 37:7, 38:8, 39:11}
    quick = []
    for i, symbol in zip(range(33,43), ('flash','laptop','chip','screen','box','screen','game','gift','gift','box')):
        if i == 40:
            continue
        glyph = '<small>NEW</small>' if i == 41 else icon(symbol)
        name = f'{glyph}<span>{value(i)}</span>'
        action = f'<a href="#section-{quick_targets[i]}">{name}</a>' if i in quick_targets else f'<button type="button" data-action="demo">{name}</button>'
        quick.append(f'<li>{action}</li>')
    quick_items = ''.join(quick)
    return f"""<header id="section-1" data-section="1" class="site-header">
    <div class="utility"><h1>{icon("crown")}{value(0)}</h1><div>{utility}</div></div>
    <div class="masthead">
      <a class="brand" href="#section-1">{image('assets/faithful/media/a0b447bc21525f0e867822fc.png', 'HACOM')}<span>{value(83)}</span></a>
      <form class="search" role="search" data-form="search"><div class="search-field">{icon("search")}<input name="search" type="search" required aria-label="{value(10)}" placeholder="{value(9)}"><button type="button" data-action="demo" aria-label="Tìm bằng hình ảnh">{icon('camera')}</button><button type="button" data-action="demo" aria-label="Tìm bằng giọng nói">{icon('mic')}</button></div><button type="submit">{value(10)}</button></form>
      <nav aria-label="Tài khoản và mua sắm" class="account">{account}</nav>
    </div>
    <div class="header-grid">
      <nav aria-label="{value(11)}"><details class="departments"><summary>{icon('menu')}{value(11)}</summary><ul>{menu}</ul></details></nav>
      <nav class="quick-nav" aria-label="Điều hướng sản phẩm"><ul>{quick_items}</ul></nav>
      <section class="hero" aria-labelledby="hero-title">
        <img class="hero-art" src="assets/index2/hero-clean.webp" width="1035" height="663" alt="" fetchpriority="high">
        <p class="hero-stock">RTX 50 SERIES · SẴN HÀNG</p>
        <div class="hero-copy">
          <p class="hero-brand">ROG | TUF | ZENBOOK | VIVOBOOK</p>
          <h2 id="hero-title">LAPTOP <span>AI</span></h2><strong>KIẾN TẠO TƯƠNG LAI</strong>
          <p class="hero-description">Hiệu năng đột phá | AI tăng tốc công việc | Sẵn sàng cho thế hệ mới</p>
          <ul><li><b>AI</b>Tích hợp AI<br>hiệu suất cao</li><li>{icon('laptop')}Thiết kế mỏng nhẹ<br>sang trọng</li><li>{icon('battery')}Pin bền bỉ<br>làm việc cả ngày</li></ul>
          <div class="actions">{button('Khám phá ngay →')}{button('Tư vấn cấu hình')}</div>
        </div>
        <span class="hero-pagination" aria-hidden="true"><i></i><i></i><i></i></span>
      </section>
      <div class="promotions">{''.join(promo)}</div>
    </div>
    <ul class="benefits" aria-label="Cam kết dịch vụ">{benefits}</ul>
</header>"""


def render_product(number, index, rows, product_photos):
    title = next(row for row in rows if row['id'].startswith('Product name'))
    details = []
    for row in rows:
        text = clean(row['text'])
        if row is title or not text or text == 'Mua ngay':
            continue
        tag, cls = 'p', ''
        if row['id'].startswith('Original price'):
            tag, cls = 'del', 'original-price'
        elif row['id'].startswith('Price'):
            tag, cls = 'strong', 'price'
        elif text.startswith('-') and text.endswith('%'):
            tag, cls = 'span', 'badge'
        details.append(f'<{tag} class="{cls}">{label(text)}</{tag}>')
    key = f'{number}-{index + 1}'
    return f"""<li><article class="product" data-product="{key}">
      {image(product_photos[key], clean(title['text']))}
      <h3>{label(title['text'])}</h3>
      <div class="product-details">{''.join(details)}</div>
      <div class="actions">{button('Yêu thích', 'favorite', ' aria-pressed="false"')}{button('Mua ngay', 'buy')}</div>
    </article></li>"""


def render_section(section, mobile, product_photos):
    number = section['number']
    rows = {row['key']: row for row in section['texts'] if clean(row['text'])}
    products = defaultdict(list)
    for row in rows.values():
        if row['card'] and row['card'].startswith('Product card'):
            products[row['card']].append(row)
    used = {row['key'] for group in products.values() for row in group}
    used_images = set()
    cards = []
    introductions = []
    filters = [
        action['name'] for action in section['actions']
        if action['kind'].lower().startswith('filter') and action['name']
    ]
    action_labels = {
        clean(action['name']) for action in section['actions']
        if action['name'] and not action['card'] and action['kind'].lower().startswith(('button', 'cta'))
    }

    def render_row(row):
        value = clean(row['text'])
        if value in filters:
            return button(value, 'filter', ' aria-pressed="false"')
        if value in action_labels or value.startswith(('Xem thêm', 'Xem tất cả', 'Khám phá ngay')) or value.endswith('→'):
            return button(value)
        if row['id'].startswith(('Heading','Category name','Channel title','Title','Metric value')):
            return f'<h3>{label(value)}</h3>'
        return f'<p>{label(value)}</p>'

    def add_card(texts, photos, piece_actions=()):
        if not (texts or photos):
            return
        if not photos and number != 3 and len(texts) <= 2 and all(
            len(clean(row['text'])) < 140 and not row['id'].startswith(('Metric', 'Title', 'Channel title'))
            for row in texts
        ):
            introductions.extend(render_row(row) for row in texts)
            return
        if number == 3 and texts and clean(texts[0]['text']) == 'FLASH':
            content = ''.join(
                button(row['text']) if clean(row['text']) in action_labels else f'<span>{label(row["text"])}</span>'
                for row in texts
            )
            introductions.append(f'<div class="flash-banner">{content}</div>')
            return
        content = ''.join(
            f'<h3>{label(row["text"])}</h3>'
            if i == 0 and photos and clean(row['text']) not in action_labels
            else render_row(row)
            for i, row in enumerate(texts)
        )
        media = ''.join(image(path) for path in photos)
        if number == 12 and photos and texts and piece_actions:
            content += button('Khám phá ' + clean(texts[0]['text']))
        if number == 19 and photos and texts:
            content += button('Xem video')
        cards.append(f'<article class="content-card">{media}{content}</article>')

    for index, piece in enumerate(mobile['pieces']):
        keys = list(dict.fromkeys(text['key'] for text in piece.get('texts', []) if text['key'] in rows and text['key'] not in used))
        used.update(keys)
        if piece.get('background') and number != 3:
            photos = [path for path in source_images(piece['background']) if path not in used_images]
            used_images.update(photos)
        else:
            photos = []
        if number == 20 and 3 <= index <= 12:
            photos = [f'assets/index2/content/customer-{index-2:02}.webp']
        if number == 18 and index == 8:
            photos = ['assets/index2/content/article-featured.webp']
        if number == 18 and index == 9:
            for article in range(6):
                article_keys = [f't{882+article*3+offset}' for offset in (1,0,2)]
                add_card([rows[key] for key in article_keys if key in rows],
                         [f'assets/index2/content/article-{article+1:02}.webp'])
            continue
        add_card([rows[key] for key in keys], photos, piece.get('actions', []))

    # A few labels are present only in the desktop capture.
    missing = [row for key, row in rows.items() if key not in used]
    if missing:
        add_card(missing, [])

    catalog = ''
    if products:
        items = ''.join(render_product(number, i, group, product_photos) for i, group in enumerate(products.values()))
        catalog = f"""<div class="catalog">
        <div class="carousel-controls" aria-label="Điều khiển danh sách sản phẩm">
        {button('‹', 'previous', ' aria-label="Sản phẩm trước"')}{button('›', 'next', ' aria-label="Sản phẩm tiếp theo"')}
        </div><ul class="products" aria-label="Sản phẩm" tabindex="0">{items}</ul></div>"""
    content = f'<div class="content-grid">{"".join(cards)}</div>'
    if number in (19, 20):
        controls = button('‹', 'previous', ' aria-label="Mục trước"') + button('›', 'next', ' aria-label="Mục tiếp theo"')
        content = f'<div class="catalog"><div class="carousel-controls">{controls}</div><div class="content-grid media-carousel" tabindex="0" role="region" aria-label="{label(section["title"])}">{"".join(cards)}</div></div>'
    return f"""<section id="section-{number}" data-section="{number}" class="store-section">
    <h2>{label(section['title'])}</h2>
    {f'<div class="section-intro">{"".join(introductions)}</div>' if introductions else ''}
    {content}
    {catalog}
</section>"""


def render_footer(section):
    texts = {int(row['key'][1:]): row['text'] for row in section['texts']}

    def value(i):
        return label(texts[i])

    perks = ''.join(f'<li><strong>{value(i)}</strong><p>{value(i+1)}</p></li>' for i in range(1013,1019,2))
    metrics = ''.join(f'<li><strong>{value(i)}</strong> {value(i+1)}</li>' for i in range(1023,1031,2))
    locations = ''.join(f'<li>{value(i+1)}</li>' for i in range(1031,1071,2))
    groups = ''.join(
        f'<section><h3>{value(start)}</h3><ul>' +
        ''.join(f'<li>{button(texts[i])}</li>' for i in range(start+1,end)) +
        '</ul></section>' for start,end in [(1073,1079),(1079,1085),(1085,1091),(1091,1101)]
    )
    photos = ''.join(image(path) for path in source_images(section['background']))
    return f"""<footer id="section-22" data-section="22" class="store-footer">
    <section class="newsletter"><h2>{value(1009)}</h2>
      <form data-form="newsletter"><input name="contact" required aria-label="{value(1010)}" placeholder="{value(1010)}">
      <button type="submit">{value(1011)}</button><label><input name="consent" type="checkbox" checked required> {value(1012)}</label></form>
      <ul class="footer-grid">{perks}</ul>
    </section>
    <section><h2>{value(1021)}</h2><p>{value(1019)} {value(1020)}</p><p>{value(1022)} · {value(1072)}</p>
      <ul class="footer-grid">{metrics}</ul><ol class="locations">{locations}</ol>{button(texts[1071])}
    </section>
    <nav aria-label="Thông tin HACOM" class="footer-grid">{groups}</nav>
    <div class="footer-grid">
      <section><h3>{value(1101)}</h3><p>{value(1102)}</p><p>{value(1103)} {value(1104)} · {value(1105)} {value(1106)}</p></section>
      <section><h3>{value(1107)}</h3><p>{value(1108)} · {value(1109)} · {value(1110)} · {value(1111)}</p></section>
      <section><h3>{value(1112)}</h3><p>{value(1113)} {value(1114)}</p><h3>{value(1124)}</h3></section>
    </div>
    <div class="footer-media">{photos}</div>
    <section><h2>{value(1115)}</h2><p>{value(1116)} · {value(1117)}</p>
      <p>{value(1118)} <a href="tel:19001903">{value(1119)}</a> · {value(1120)} <a href="mailto:info@hacom.vn">{value(1121)}</a> · {value(1122)} <a href="https://www.hacom.vn">{value(1123)}</a></p>
      <p>{value(1125)} · {value(1126)}</p><div class="actions">{''.join(button(texts[i]) for i in range(1127,1130))}</div>
    </section>
</footer>"""


def main():
    if IMAGE_MANIFEST.exists():
        IMAGE_INFO.update(json.loads(IMAGE_MANIFEST.read_text(encoding='utf-8')))
    desktop, mobile = fixture('desktop-source'), fixture('mobile-source')
    product_photos = json.loads((ROOT / 'tools/index2/product-photos.json').read_text(encoding='utf-8'))
    header = render_header(desktop[0], mobile[0])
    sections = '\n'.join(render_section(s, m, product_photos) for s, m in zip(desktop[1:-1], mobile[1:-1], strict=True))
    footer = render_footer(desktop[-1])
    html = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HACOM - Laptop, PC Gaming và thiết bị công nghệ</title>
  <meta name="description" content="Khám phá laptop, PC Gaming, linh kiện máy tính và thiết bị công nghệ tại HACOM. Tìm hiểu sản phẩm, giải pháp công nghệ và hệ thống showroom toàn quốc.">
  <link rel="stylesheet" href="index2.css">
  <link rel="stylesheet" href="index2-header.css">
  <script src="index2.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main-content">Đến nội dung chính</a>
{header}
<main id="main-content">
{sections}
</main>
{footer}
<div id="demo-status" role="status" hidden></div>
</body>
</html>
"""
    (ROOT / 'index2.html').write_text('\n'.join(line.rstrip() for line in html.splitlines()) + '\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
