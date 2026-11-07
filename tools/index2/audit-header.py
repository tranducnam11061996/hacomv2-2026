"""Verify semantic header, measured geometry and image evidence; write a scoped report."""
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageChops,ImageStat,ImageDraw
import json,re,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
def values(name):
 result=[]
 for r in json.loads((ROOT/'reference'/name).read_text(encoding='utf8')):
  for c in r.get('result',{}).get('content',[]):
   text=c.get('text','')
   if '```json'in text:result.append(json.loads(text.split('```json')[1].split('```')[0]))
 return result
soup=BeautifulSoup((ROOT/'index2.html').read_text(encoding='utf8'),'html.parser');header=soup.header
normalized=re.sub(r'\s+','',header.get_text())
expected=['ROG | TUF | ZENBOOK | VIVOBOOK','RTX 50 SERIES · SẴN HÀNG','LAPTOP AI','KIẾN TẠO TƯƠNG LAI','Hiệu năng đột phá | AI tăng tốc công việc | Sẵn sàng cho thế hệ mới','Tích hợp AI','hiệu suất cao','Thiết kế mỏng nhẹ','sang trọng','Pin bền bỉ','làm việc cả ngày','Khám phá ngay','Tư vấn cấu hình']
missing=[s for s in expected if re.sub(r'\s+','',s)not in normalized]
assert not missing
assert len(soup.select('h1'))==1 and header.select_one('#hero-title').name=='h2'
assert not header.select('.desktop-controls,.mobile-controls')
assert not [b for b in header.select('button')if not b.get_text(strip=True)and not b.has_attr('data-hero-slide')]
assert 'desktop-01.webp'not in str(header)and 'mobile-01-18.webp'not in str(header)
assert hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest()=='4a4aebb09a52f89a9d0dc04fa0a8d6e63b412982d9da9cb285b90d0df7d395ce'
original={v['width']:v for v in values('header-matrix-results.json')if isinstance(v,dict)and 'sections'in v and '/index.html?'in v['url']}
new={v['width']:v for f in ['header-final-results.json','header-raster-proof-results.json']for v in values(f)if isinstance(v,dict)and 'sections'in v}
geometry=[]
for w,o in original.items():
 n=new[w];diffs=[{'section':a['number'],'delta':b['height']-a['height']}for a,b in zip(o['sections'],n['sections'])if abs(a['height']-b['height'])>.1]
 assert not diffs and n['overflow']==0 and n['height']==o['height']
 geometry.append({'width':w,'height':n['height'],'sectionHeightDifferences':diffs,'overflow':n['overflow']})
trans=[v for v in values('header-breakpoint-results.json')if isinstance(v,dict)and 'sections'in v]
assert len(trans)==12
for a,b in zip(trans[:6],trans[6:]):assert a['height']==b['height']and all(abs(x['height']-y['height'])<.1 for x,y in zip(a['sections'],b['sections']))
visual=[];folder=ROOT/'reference/header-native-visual'
for w,o in original.items():
 a=Image.open(folder/f'{w}-index.html.webp').convert('RGB');b=Image.open(folder/f'{w}-index2.html.webp').convert('RGB')
 height=min(round(o['sections'][0]['height']),a.height,b.height);a=a.crop((0,0,w,height));b=b.crop((0,0,w,height));d=ImageChops.difference(a,b)
 mean=sum(ImageStat.Stat(d).mean)/3;hist=d.convert('L').histogram();changed=sum(hist[17:])/sum(hist)*100
 Image.blend(a,b,.5).save(folder/f'{w}-overlay.webp',lossless=True);d.point(lambda x:min(255,x*4)).save(folder/f'{w}-diff.webp',lossless=True)
 visual.append({'width':w,'headerHeight':height,'meanAbsoluteError255':mean,'changedLuminanceOver16Percent':changed})
 if w in [390,1920]:
  scale=min(1,960/w);size=(round(w*scale),round(height*scale));sheet=Image.new('RGB',(size[0]*2,size[1]+28),'white');sheet.paste(a.resize(size),(0,28));sheet.paste(b.resize(size),(size[0],28));draw=ImageDraw.Draw(sheet);draw.text((10,7),'Original',fill='black');draw.text((size[0]+10,7),'Native HTML',fill='black');sheet.save(folder/f'{w}-comparison.jpg',quality=92)
static=json.loads((ROOT/'reference/index2-static-audit.json').read_text(encoding='utf8'))
result={'burnedInTextInventory':expected,'missingText':missing,'nativeHeroHeading':header.select_one('#hero-title').get_text(' ',strip=True),'nativeHeaderButtons':len(header.select('button')),'geometry':geometry,'breakpointChecks':6,'visual':visual,'originalUnchanged':True}
(ROOT/'reference/header-native-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'reference/header-visual-results.json').write_text(json.dumps(visual,indent=2),encoding='utf8')
# Preserve the actual final Lighthouse reports alongside the visual evidence.
scores={}
for device,r in zip(['desktop','mobile'],json.loads((ROOT/'reference/header-lighthouse-final-results.json').read_text(encoding='utf8'))):
 text='\n'.join(c.get('text','')for c in r['result']['content']);out=ROOT/'reference/header-native-lighthouse'/device;out.mkdir(parents=True,exist_ok=True)
 for ext in ['json','html']:
  path=re.search(r'- (C:\\[^\n]+report\.'+ext+r')',text).group(1);shutil.copyfile(path,out/('report.'+ext))
 report=json.loads((out/'report.json').read_text(encoding='utf8'));scores[device]={k:round(report['categories'][k]['score']*100)for k in ['seo','best-practices','accessibility']}
rows='\n'.join(f"| {v['width']} | {v['height']} | 0 | 0 |"for v in geometry)
diffs='\n'.join(f"| {v['width']} | {v['meanAbsoluteError255']:.3f} | {v['changedLuminanceOver16Percent']:.2f}% |"for v in visual)
report=f'''# Hiệu chỉnh header và banner thành HTML — 07/11/2026

Đã hoàn thiện phần header, menu, banner chính, ba banner phụ và chính sách trong ảnh người dùng. Bản gốc được giữ nguyên. Không xác nhận trùng pixel 100%; các khác biệt đo được được công bố dưới đây.

## Nội dung đã sửa

- Chữ trong PNG banner chính đã trở thành HTML hiển thị: nhãn ROG/TUF/Zenbook/Vivobook, tình trạng RTX, tiêu đề LAPTOP AI, tagline, mô tả, ba lợi ích và nút tư vấn. Tiêu đề dùng H2, lợi ích dùng ul/li; hai CTA chứa chính nhãn hiển thị.
- Header và danh mục dùng button chứa chữ thay cho đoạn chữ và nút phủ tách rời; bỏ cả hai nhóm overlay cũ. Điều hướng có nav và danh sách. Ba banner phụ dùng H3 và nút HTML. Tìm kiếm dùng placeholder và nút submit thực trong form.
- Ảnh nền ba banner phụ vốn không có chữ; giữ nguyên các ảnh này. Banner chính không có nền sạch tương đương trong tài nguyên đã khảo sát. Đã loại bỏ chữ và icon khỏi PNG bằng phục hồi từ vùng ảnh lân cận; giữ phần laptop, ánh sáng và nền kính. HTML/CSS dựng lại chữ, icon AI/laptop/pin, viền kính, nút và điều khiển dấu slide.
- Không dùng lại banner còn chữ rồi phủ HTML trùng lên. Logo HACOM/NVIDIA được giữ dưới dạng đồ họa theo phạm vi cho phép. Đã kiểm kê thủ công chữ trong ảnh nguồn và đưa danh sách vào kiểm tra tự động, khắc phục điểm thiếu của audit SVG trước đó.
- Bộ sinh gọi normalize-header.py; build tiếp theo giữ các thành phần mới. Trang triển khai vẫn chỉ cần HTML/CSS/JS và assets, không yêu cầu framework hoặc build.

## Kiểm thử thực tế

Chrome DevTools MCP chạy qua managed launcher, profile chuyên dụng; chỉ thao tác tab của tác vụ. Kết nối cũ không hoạt động đã được khôi phục qua launcher. Ảnh chụp được lấy trực tiếp từ MCP; không dùng browser automation thay thế.

| Viewport | Chiều cao toàn trang | Section lệch >0,1px | Tràn ngang |
|---|---:|---:|---:|
{rows}

Chuỗi resize 1920 → 390 → 768 → 1024 → 360 → 1920 cũng khớp với bản gốc ở cả 22 section. Chiều cao 768px trong chuỗi resize là 45.142px; khi tải mới ở 768px là 45.130px, phù hợp hành vi reflow của bản gốc.

Đã kiểm tra yêu thích bật/tắt, giỏ hàng, CTA, chọn dấu carousel, tìm kiếm, menu, bộ lọc, carousel sản phẩm và đăng ký email/điện thoại hợp lệ/không hợp lệ cùng consent. Chuột thật qua MCP click, phím Space, Enter và Escape đều có bằng chứng trong các file kết quả. Không tạo giao dịch hoặc kết nối dịch vụ bên ngoài.

Bản kiểm tra qua HTTP cùng origin với CSP script-src 'none' vẫn có tiêu đề và lợi ích banner đang hiển thị, một H1 và đủ 22 section. Console xác nhận index2.js bị CSP chặn, không có lỗi tải font trong phép kiểm tra này.

## SEO, HTML và accessibility

HTML5 parser không báo lỗi; không có ID trùng, ảnh thiếu alt, nút thiếu tên truy cập, liên kết # hoặc script ngoài. Còn đúng một H1; source có 25 H2 (bao gồm các biến thể responsive) và 51 H3. Không thêm heading ẩn để thay thế chữ trong ảnh.

| Thiết bị | SEO | Best Practices | Accessibility |
|---|---:|---:|---:|
| Desktop | {scores['desktop']['seo']} | {scores['desktop']['best-practices']} | {scores['desktop']['accessibility']} |
| Mobile | {scores['mobile']['seo']} | {scores['mobile']['best-practices']} | {scores['mobile']['accessibility']} |

Hai nhóm cảnh báo còn lại là tương phản và vùng bấm. Chữ trắng trên đỏ #ed1c24 đạt khoảng 4,38:1, thấp hơn yêu cầu 4,5:1 cho chữ nhỏ; dấu slide và các hàng khi co nhỏ có mục tiêu bấm sát nhau. Đã giữ thiết kế hiển thị theo yêu cầu; không coi điểm SEO là bằng chứng index trên production. Canonical/OG URL/robots/schema vẫn cần dữ liệu triển khai thực tế như báo cáo nền. Không truy cập GA, GTM hoặc Search Console.

## Bằng chứng thị giác

Ảnh trước/sau, overlay và diff ở reference/header-native-visual/. Mobile 360/390/768 được chụp đủ chiều cao header; các viewport khác được cắt theo chiều cao header khi tính diff. Cùng Chrome, DPR 1, chờ font và ảnh sẵn sàng.

| Viewport | Sai số trung bình /255 | Pixel có sai khác độ sáng >16 |
|---|---:|---:|
{diffs}

Sai lệch tập trung ở raster chữ được thay bằng font HTML, viền icon/nút và texture kính sau khi bỏ chữ khỏi PNG. Texture đã phục hồi không thể được coi là nền gốc không chữ chính xác. Không xác nhận giống 100% bằng cảm nhận hoặc suy diễn từ việc khớp chiều cao.

![Đối chiếu desktop](reference/header-native-visual/1920-comparison.jpg)

![Đối chiếu mobile](reference/header-native-visual/390-comparison.jpg)

## Dung lượng và bản gốc

Mã HTML/CSS/JS hiện tại: {static['newCodeBytes']:,} B so với {static['oldCodeBytes']:,} B của bản gốc, giảm {(1-static['newCodeBytes']/static['oldCodeBytes'])*100:.1f}%. Đồ họa được trang tham chiếu: {static['newReferencedMediaBytes']:,} B so với {static['oldMediaBytes']:,} B, giảm {(1-static['newReferencedMediaBytes']/static['oldMediaBytes'])*100:.1f}%. Không suy diễn mức giảm này thành tốc độ render; số đo tải trong báo cáo nền thuộc bản trước hiệu chỉnh header.

SHA-256 index.html không đổi: {static['indexOriginalSha256']}.

Bằng chứng máy đọc: reference/header-native-audit.json, header-matrix-results.json, header-final-results.json, header-raster-proof-results.json, header-breakpoint-results.json, header-interaction-results.json, header-full-interaction-results.json, header-mouse-results.json, header-keyboard-results.json và header-nojs-final-results.json. Lighthouse HTML/JSON ở reference/header-native-lighthouse/.
'''
(ROOT/'HEADER-HTML-AUDIT.md').write_text(report,encoding='utf8')
print(json.dumps({'geometryChecks':len(geometry),'missingBurnedInText':missing,'scores':scores,'visualMAE':[(v['width'],round(v['meanAbsoluteError255'],3))for v in visual]}))
