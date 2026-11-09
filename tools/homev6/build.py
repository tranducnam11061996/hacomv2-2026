"""Capture and rebuild the public homev6 page with local resources."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import argparse
import base64
import json
import mimetypes
import re
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "https://web-dev.hacom.vn/homev6"
DIRECTORY = ROOT / "assets/homev6"
SNAPSHOT = ROOT / "reference/homev6"
URL_PATTERN = re.compile(r"url\(\s*([\"\']?)(.*?)\1\s*\)")


def capture():
    SNAPSHOT.mkdir(exist_ok=True)
    response = requests.get(SOURCE, timeout=30)
    response.raise_for_status()
    (SNAPSHOT / "source.html").write_bytes(response.content)
    (SNAPSHOT / "capture.json").write_text(json.dumps({
        "url": SOURCE, "capturedAt": datetime.now(timezone.utc).isoformat(),
        "sha256": sha256(response.content).hexdigest()
    }, indent=2), encoding="utf-8")


def build():
    DIRECTORY.mkdir(exist_ok=True)
    soup = BeautifulSoup((SNAPSHOT / "source.html").read_bytes(), "html5lib")
    urls = set()
    css_urls = []
    for link in soup.select('link[rel~="stylesheet"]'):
        css_urls.append(urljoin(SOURCE, link["href"]))
    css_text = {}
    for url in css_urls:
        source_path = SNAPSHOT / (sha256(url.encode()).hexdigest()[:24] + ".css")
        if not source_path.exists():
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            source_path.write_text(response.text, encoding="utf-8")
        css_text[url] = source_path.read_text(encoding="utf-8")
        urls.add(url)
        for match in URL_PATTERN.finditer(css_text[url]):
            if not match[2].startswith(("data:", "#")):
                urls.add(urljoin(url, match[2]))
    for node in soup.find_all(True):
        for attribute in ("src", "poster"):
            value = node.get(attribute, "")
            if value and not value.startswith(("data:", "#")) and node.name != "script":
                urls.add(urljoin(SOURCE, value))
        for attribute in ("srcset", "imagesrcset"):
            for item in node.get(attribute, "").split(","):
                if item.strip() and not item.lstrip().startswith("data:"):
                    urls.add(urljoin(SOURCE, item.strip().split()[0]))
        for match in URL_PATTERN.finditer(node.get("style", "")):
            if not match[2].startswith(("data:", "#")):
                urls.add(urljoin(SOURCE, match[2]))
    manifest_path = SNAPSHOT / "assets.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    errors = []

    def download(url):
        existing = manifest.get(url)
        if existing and (ROOT / existing).is_file():
            return url, existing, None
        try:
            response = requests.get(url, timeout=30)
            if response.status_code >= 400 and urlsplit(url).hostname == "cdn-transformations.hacom.vn":
                encoded = urlsplit(url).path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                original = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode()
                response = requests.get(original, timeout=30)
            response.raise_for_status()
            extension = mimetypes.guess_extension(response.headers.get("Content-Type", "").split(";")[0]) or Path(urlsplit(url).path).suffix.lower()
            if extension not in (".css", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".woff", ".woff2", ".gif", ".avif", ".ico", ".mp4"):
                extension = mimetypes.guess_extension(response.headers.get("Content-Type", "").split(";")[0]) or ".bin"
            path = DIRECTORY / (sha256(url.encode()).hexdigest()[:24] + extension)
            path.write_bytes(response.content)
            return url, path.relative_to(ROOT).as_posix(), None
        except Exception as error:
            return url, None, str(error)
    with ThreadPoolExecutor(max_workers=12) as pool:
        for url, path, error in pool.map(download, sorted(urls)):
            if error:
                errors.append({"url": url, "error": error})
            else:
                manifest[url] = path
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (SNAPSHOT / "download-errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    if errors:
        raise RuntimeError(f"{len(errors)} resource downloads failed; see download-errors.json")

    def local(value, base=SOURCE, css=False):
        if not value or value.startswith(("data:", "#")):
            return value
        path = manifest[urljoin(base, value)]
        return Path(path).name if css else path

    def rewrite_urls(text, base=SOURCE, css=False):
        return URL_PATTERN.sub(lambda match: 'url("' + local(match[2], base, css) + '")', text)

    for url, text in css_text.items():
        (ROOT / manifest[url]).write_text(rewrite_urls(text, url, True), encoding="utf-8")
    for node in list(soup.select("script, link[rel=preload], link[rel=modulepreload], link[rel=prefetch], base")):
        node.decompose()
    for node in soup.find_all(True):
        for attribute in list(node.attrs):
            if attribute.startswith("on"):
                del node[attribute]
        for attribute in ("src", "poster"):
            if node.get(attribute):
                node[attribute] = local(node[attribute])
        for attribute in ("srcset", "imagesrcset"):
            if node.get(attribute):
                node[attribute] = ", ".join(local(item.strip().split()[0]) + (" " + " ".join(item.strip().split()[1:]) if len(item.strip().split()) > 1 else "") for item in node[attribute].split(",") if item.strip())
        if node.get("style"):
            node["style"] = rewrite_urls(node["style"])
        if node.name == "link" and "stylesheet" in node.get("rel", []):
            node["href"] = local(node["href"])
        if node.name == "a" and node.get("href") and not node["href"].startswith(("#", "tel:", "mailto:")):
            node["data-source-href"] = urljoin(SOURCE, node["href"])
            node["href"] = "#"
    for node in soup.select('meta[property="og:url"], link[rel=canonical]'):
        node.decompose()
    for node in soup.select("[data-nextjs-scroll-focus-boundary]"):
        node.attrs.pop("data-nextjs-scroll-focus-boundary", None)
    style = soup.new_tag("link", rel="stylesheet", href="homev6-local.css")
    soup.head.append(style)
    script = soup.new_tag("script", src="homev6-local.js", defer=True)
    soup.head.append(script)
    status = soup.new_tag("div", id="local-status", role="status", **{"aria-live": "polite", "hidden": ""})
    soup.body.append(status)
    (ROOT / "index2.html").write_text("\n".join(line.rstrip() for line in str(soup).splitlines()) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"assets": len(urls), "stylesheets": len(css_urls), "images": len(soup.select("img")), "sections": len(soup.select("main section"))}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()
    if args.capture:
        capture()
    build()
