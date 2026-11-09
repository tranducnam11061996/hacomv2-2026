"""Build native category text over the original graphics-only artwork."""
from html import escape
from pathlib import Path
import re
import base64
import mimetypes
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]


def render_featured_categories(section, mobile):
    rows = {row["key"]: row for row in section["texts"]}
    output = []
    directory = ROOT / "assets/index2/featured"
    directory.mkdir(exist_ok=True)
    for index, piece in enumerate(mobile["pieces"]):
        x, y, width, height = piece["viewBox"]
        svg = ET.fromstring(piece["background"])
        # Retain only definitions reachable from visible graphics.
        definitions = {node.get("id"): node for node in svg.iter() if node.get("id")}
        pending = [node for node in svg if not node.tag.endswith("}defs")]
        reached = set()
        while pending:
            node = pending.pop()
            if node in reached:
                continue
            reached.add(node)
            pending.extend(list(node))
            for key, value in node.attrib.items():
                references = re.findall(r"url\(#([^)]*)\)", value)
                if key.endswith("href") and value.startswith("#"):
                    references.append(value[1:])
                pending.extend(definitions[key] for key in references if key in definitions)
        for defs in list(svg):
            if defs.tag.endswith("}defs"):
                for node in list(defs):
                    if node not in reached:
                        defs.remove(node)
        # Remove container shadows while preserving the source artwork.
        shadow_ids = {
            node.get("id") for node in svg.iter()
            if node.tag.endswith("}filter") and any(child.tag.endswith("}feOffset") for child in node.iter())
        }
        for node in svg.iter():
            if any(f"url(#{key})" in node.get("filter", "") for key in shadow_ids):
                node.attrib.pop("filter", None)
            if node.tag.endswith("}rect") and node.get("fill", "").lower() == "#f3f6f9":
                node.set("fill", "#fff")
            if (node.tag.endswith("}rect") and node.get("rx")
                    and float(node.get("width", "0")) >= 200
                    and float(node.get("height", "0")) >= 60):
                node.set("rx", "20")
                node.set("ry", "20")
            for key, value in list(node.attrib.items()):
                if key.endswith("href") and value.startswith("../../assets/"):
                    # SVG images cannot load external image resources in img mode.
                    image_path = ROOT / value[len("../../"):]
                    mime = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
                    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
                    node.set(key, f"data:{mime};base64,{encoded}")
        svg.set("aria-hidden", "true")
        path = directory / f"{index:02}.svg"
        path.write_text(ET.tostring(svg, encoding="unicode"), encoding="utf-8")
        text = []
        items = sorted(piece["texts"], key=lambda item: item["key"] != "t86") if index == 0 else piece["texts"]
        for item in items:
            row = rows[item["key"]]
            tag = "h2" if row["key"] == "t86" else ("h3" if index >= 3 and item == piece["texts"][0] else "p")
            if row["key"] in ("t84", "t89"):
                tag = "button"
            attributes = ' type="button" data-action="demo"' if tag == "button" else ""
            lines = []
            line_height = row["box"]["h"] / max(1, len(row["rows"]))
            for line in row["rows"]:
                top = row["box"]["y"] - y + line["y"] - row["rows"][0]["y"]
                style = (
                    f'left:{line["x"] - x:.6f}px;top:{top:.6f}px;'
                    f'font-family:{line["font"]};font-size:{line["size"]}px;'
                    f'font-weight:{line["weight"]};line-height:{line_height:.6f}px;'
                    f'color:{line["color"]};letter-spacing:{line["spacing"]};opacity:{line["opacity"]}'
                )
                lines.append(f'<span class="featured-line" style="{escape(style, quote=True)}">{escape(line["text"])}</span>')
            text.append(f'<{tag}{attributes}>{"".join(lines)}</{tag}>')
        role = "intro" if index == 0 else ("all" if index == 1 else ("builder" if index == 2 else "category"))
        position = f'--x:{x}px;--y:{y-section["top"]}px;--w:{width}px;--h:{height}px'
        graphic = f'<img class="featured-graphics" src="assets/index2/featured/{index:02}.svg" width="{width}" height="{height}" alt="">'
        if index >= 3:
            title = escape(rows[piece["texts"][0]["key"]]["text"], quote=True)
            text.append(f'<button type="button" class="featured-open" data-action="demo" aria-label="{title}"></button>')
        output.append(f'<article class="featured-piece featured-{role}" style="{position}">{graphic}{"".join(text)}</article>')
    output[3:] = ['<ul class="featured-list">' + "".join(part.replace("<article ", "<li ").replace("</article>", "</li>") for part in output[3:]) + '</ul>']
    return '<section id="section-2" data-section="2" class="featured-categories"><div class="featured-canvas">' + "".join(output) + '</div></section>'
