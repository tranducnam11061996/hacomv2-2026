from pathlib import Path
import json,re,hashlib,collections,html5lib,urllib.parse
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'index2.html').read_text(encoding='utf-8')
parser=html5lib.HTMLParser(namespaceHTMLElements=False);doc=parser.parse(source)
elements=list(doc.iter());headings=[e for e in elements if e.tag in ('h1','h2','h3','h4','h5','h6')]
ids=[e.get('id')for e in elements if e.get('id')]
missing=[]
for e in elements:
    for key in ('src','href'):
        path=e.get(key,'')
        if path and not urllib.parse.urlsplit(path).scheme and not path.startswith('#') and not (ROOT/path.split('?')[0]).exists():missing.append(path)
styles=(ROOT/'assets/faithful/fonts.css').read_text()
missing_fonts=[s for s in re.findall(r'url\(([^)]+)\)',styles) if not (ROOT/'assets/faithful'/s).exists()]
text=''.join(doc.itertext())+' '.join(e.get('placeholder','') for e in elements);normalized=re.sub(r'\s+','',text)
reference=json.loads((ROOT/'reference/index2-desktop-source.json').read_text(encoding='utf-8'))
missing_content=[{'section':s['number'],'text':t['text']} for s in reference for t in s['texts']if t['text'].strip()and re.sub(r'\s+','',t['text'])not in normalized]
asset_paths={ROOT/e.get('src')for e in elements if e.get('src','').startswith('assets/index2/')}
asset_paths.update(ROOT/p for p in re.findall(r'url\((assets/index2/[^)]+)\)',(ROOT/'index2.css').read_text(encoding='utf-8')))
for section in (e for e in elements if e.get('data-cards')):
    asset_paths.update(ROOT/c['image']for c in json.loads(section.get('data-cards')))
old_code=[ROOT/'index.html',ROOT/'fidelity.css',ROOT/'fidelity.js',ROOT/'assets/faithful/section.css',ROOT/'assets/faithful/section.js',*sorted((ROOT/'assets/faithful').glob('[0-9][0-9].js'))]
new_code=[ROOT/'index2.html',ROOT/'index2.css',ROOT/'index2.js']
result={'htmlParseErrors':parser.errors,'headingCounts':dict(collections.Counter(e.tag for e in headings)),'headings':[{'tag':e.tag,'text':' '.join(''.join(e.itertext()).split())}for e in headings],'duplicateIds':[k for k,v in collections.Counter(ids).items()if v>1],'missingResources':missing,'missingFonts':missing_fonts,'imagesWithoutAlt':sum(e.tag=='img'and e.get('alt')is None for e in elements),'unnamedButtons':sum(e.tag=='button'and not (e.get('aria-label')or ''.join(e.itertext()).strip())for e in elements),'placeholderAnchors':sum(e.tag=='a'and e.get('href')=='#'for e in elements),'missingOriginalText':missing_content,'nativeArticles':sum(e.tag=='article'for e in elements),'oldCodeBytes':sum(p.stat().st_size for p in old_code),'newCodeBytes':sum(p.stat().st_size for p in new_code),'oldMediaBytes':sum(p.stat().st_size for p in (ROOT/'assets/faithful/media').iterdir()),'newReferencedMediaBytes':sum(p.stat().st_size for p in asset_paths),'indexOriginalSha256':hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest(),'externalScripts':[e.get('src')for e in elements if e.tag=='script'and urllib.parse.urlsplit(e.get('src','')).scheme]}
(ROOT/'reference/index2-static-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'reference/index2-asset-manifest.json').write_text(json.dumps(sorted(p.relative_to(ROOT).as_posix()for p in asset_paths),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items()if k!='headings'},ensure_ascii=True)[:5000])
assert not parser.errors and not missing and not missing_fonts and not result['duplicateIds']
assert result['headingCounts'].get('h1')==1 and not missing_content
assert not result['imagesWithoutAlt']and not result['unnamedButtons']and not result['placeholderAnchors']and not result['externalScripts']
