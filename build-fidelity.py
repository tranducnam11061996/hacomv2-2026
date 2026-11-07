import argparse
from collections import deque
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
from hashlib import sha256
import base64, json, re, shutil, os
from copy import deepcopy

parser = argparse.ArgumentParser(description='Rebuild the 22 homepage layers from the Figma SVG export.')
parser.add_argument('archive', type=Path, help='ZIP exported from Figma with SVG text kept as text')
parser.add_argument('--fonts-dir', type=Path,
                    default=Path(os.environ['TEMP']) / 'hacom-fidelity-fonts' / 'node_modules')
args = parser.parse_args()

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets' / 'faithful'
OUT.mkdir(exist_ok=True)
for name in ('media', 'fonts'):
    (OUT / name).mkdir(exist_ok=True)

SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)
ns = lambda name: '{' + SVG + '}' + name
with ZipFile(args.archive) as archive:
    source = ET.fromstring(archive.read(next(n for n in archive.namelist() if n.endswith('/1920px.svg'))))
groups = list(source[0])[1:]
assert len(groups) == 22 and source.get('viewBox') == '0 0 1920 20142'
titles = [
    'Menu và banner hero', 'Ngành hàng nổi bật', 'Flash Sale', 'Chọn đúng máy theo đúng nghề',
    'Laptop - MacBook - Tablet', 'PC - Mini PC - All in One', 'HACOM PC Builder',
    'Màn hình máy tính', 'Linh kiện máy tính', 'Gaming Gear', 'Console - Sim Racing - Giải trí',
    'Mạng - Lưu trữ - Phần mềm', 'Thiết bị văn phòng', 'Nhà thông minh',
    'Khách hàng doanh nghiệp', 'HACOM dịch vụ tốt', 'HACOM in Numbers',
    'Cập nhật công nghệ mỗi ngày', 'Video Review', 'Đánh giá khách hàng', 'Kênh mua sắm', 'Footer'
]
fonts = [
    ('@fontsource-variable/inter','index.css','Inter'),
    ('@fontsource/goldman','700.css','Goldman'),
    ('@fontsource/goldman','400.css','Goldman'),
    ('@fontsource-variable/roboto-slab','index.css','Roboto Slab'),
    ('@fontsource-variable/manrope','index.css','Manrope'),
    ('@fontsource-variable/roboto-condensed','index.css','Roboto Condensed'),
    ('@fontsource-variable/roboto','index.css','Roboto')
]
packages = args.fonts_dir
font_css = []
for package, css, family in fonts:
    package_dir = packages / package
    raw = (package_dir / css).read_text(encoding='utf8')
    def local(match):
        filename = match[1]
        shutil.copyfile(package_dir / 'files' / filename, OUT / 'fonts' / filename)
        return 'url(fonts/' + filename + ')'
    raw = re.sub(r'url\(\./files/([^\)]+)\)', local, raw)
    raw = re.sub(r"font-family:\s*'[^']+'", f"font-family: '{family}'", raw)
    font_css.append(raw)
    license = next(package_dir.glob('LICENSE*'), None)
    if license:
        shutil.copyfile(license, OUT / 'fonts' / (package.split('/')[-1] + '-LICENSE.txt'))
(OUT/'fonts.css').write_text('\n'.join(font_css), encoding='utf8')

defs = {e.get('id'): e for e in source.find(ns('defs')) if e.get('id')}
def refs(tree):
    for node in tree.iter():
        for k, value in node.attrib.items():
            if k.endswith('href') and value.startswith('#'):
                yield value[1:]
            yield from re.findall(r'url\(#([^)]*)\)', value)

def externalize(tree):
    for node in tree.iter(ns('image')):
        for k,v in list(node.attrib.items()):
            if k.endswith('href') and v.startswith('data:image/'):
                kind, encoded = v.split(',', 1)
                suffix = kind.split('/')[1].split(';')[0].replace('jpeg','jpg')
                blob = base64.b64decode(encoded)
                file = sha256(blob).hexdigest()[:24] + '.' + suffix
                path = OUT / 'media' / file
                if not path.exists():
                    path.write_bytes(blob)
                node.set(k, 'media/' + file)

metadata=[]
for number,(title,group) in enumerate(zip(titles,groups),1):
    queue = deque(refs(group))
    used = {}
    while queue:
        name = queue.popleft()
        if name in defs and name not in used:
            used[name] = deepcopy(defs[name])
            queue.extend(refs(defs[name]))
    externalize(group)
    for d in used.values():
        externalize(d)
    svg = ET.Element(ns('svg'), {'id':'art', 'viewBox':'0 0 1920 20142','fill':'none','aria-label':title})
    localdefs = ET.SubElement(svg, ns('defs'))
    localdefs.extend(used.values())
    group.set('id','art-content')
    svg.append(group)
    for node in svg.iter():
        for key, value in list(node.attrib.items()):
            if key.endswith('href') and value.startswith('media/'):
                node.set(key, 'assets/faithful/' + value)
            elif key.endswith('href') and value.startswith('#') and value[1:] in used:
                node.set(key, '#' + f's{number}-' + value[1:])
            elif 'url(#' in value:
                node.set(key, re.sub(r'url\(#([^)]*)\)', lambda m: 'url(#' + f's{number}-' + m[1] + ')' if m[1] in used else m[0], value))
    for name, definition in used.items():
        definition.set('id', f's{number}-' + name)
    svg.set('class','section-art')
    del svg.attrib['id']
    group.set('class','section-content')
    del group.attrib['id']
    art = ET.tostring(svg,encoding='unicode')
    art = re.sub(r'<html:div([^>]*) />', r'<div\1></div>', art)
    art = art.replace('<html:div', '<div').replace('</html:div>', '</div>')
    text_count = sum(1 for _ in group.iter(ns('text')))
    metadata.append({'number':number,'title':title,'textLayers':text_count})
    (OUT/f'{number:02}.js').write_text(f'window.HacomArt.register({number},' + json.dumps(art,ensure_ascii=False) + ');\n',encoding='utf8')
(OUT/'sections.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf8')
print(len(metadata),sum(m['textLayers'] for m in metadata),len(list((OUT/'media').iterdir())))

