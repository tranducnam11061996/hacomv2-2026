"""Render section 3 from measured text and original graphics."""
from collections import defaultdict
from html import escape
from pathlib import Path
import re
import base64
import mimetypes
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]


def save_graphics(markup, filename):
    svg = ET.fromstring(markup)
    ids = {node.get("id"): node for node in svg.iter() if node.get("id")}
    pending = [node for node in svg if not node.tag.endswith("}defs")]
    reached = set()
    while pending:
        node = pending.pop()
        if node in reached:
            continue
        reached.add(node)
        pending.extend(node)
        for key, value in node.attrib.items():
            references = re.findall(r"url\(#([^)]*)\)", value)
            if key.endswith("href") and value.startswith("#"):
                references.append(value[1:])
            pending.extend(ids[ref] for ref in references if ref in ids)
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
    path = ROOT / "assets/index2/flash" / filename
    path.parent.mkdir(exist_ok=True)
    path.write_text(ET.tostring(svg, encoding="unicode"), encoding="utf-8")
    return f'<img class="flash-art" src="assets/index2/flash/{filename}" alt="" aria-hidden="true">'


def text_markup(row, x, y, tag="p"):
    lines = []
    height = row["box"]["h"]
    if len(row["rows"]) > 1:
        leading = row["rows"][1]["y"] - row["rows"][0]["y"]
        height -= leading * (len(row["rows"]) - 1)
    for line in row["rows"]:
        top = row["box"]["y"] - y + line["y"] - row["rows"][0]["y"]
        style = (f'left:{line["x"]-x:.6f}px;top:{top:.6f}px;'
                 f'font-family:{line["font"]};font-size:{line["size"]}px;'
                 f'font-weight:{line["weight"]};line-height:{height:.6f}px;'
                 f'color:{line["color"]};letter-spacing:{line["spacing"]};opacity:{line["opacity"]}')
        lines.append(f'<span class="flash-line" style="{escape(style, quote=True)}">{escape(line["text"])}</span>')
    return f'<{tag}>{"".join(lines)}</{tag}>'


def action_markup(action, x, y, kind, label=None):
    box = action["box"]
    size = 32 if kind == "favorite" else 0
    width, height = max(size, box["w"]), max(size, box["h"])
    left = box["x"] - x - (width-box["w"])/2
    top = box["y"] - y - (height-box["h"])/2
    style = f'left:{left:.6f}px;top:{top:.6f}px;width:{width:.6f}px;height:{height:.6f}px'
    pressed = ' aria-pressed="false"' if kind in ("favorite", "filter") else ""
    name = escape(label or action["name"], quote=True)
    return f'<button class="flash-control" type="button" data-action="{kind}" aria-label="{name}"{pressed} style="{style}"></button>'


def render_flash_sale(section, mobile):
    rows = {row["key"]: row for row in section["texts"]}
    pieces = mobile["pieces"]
    header, products = pieces[:2]
    hx, hy, hw, hh = header["viewBox"]
    px, py, pw, ph = products["viewBox"]
    title = "<h2>" + "".join(text_markup(rows[key], hx, hy, "span") for key in ("t160", "t161")) + "</h2>"
    header_text = title + "".join(text_markup(rows[item["key"]], hx, hy) for item in header["texts"] if item["key"] not in ("t160", "t161"))
    header_text += "".join(action_markup(action, hx, hy, "demo") for action in header["actions"])
    grouped = defaultdict(list)
    for row in section["texts"]:
        if row["card"]:
            grouped[row["card"]].append(row)
    cards = []
    for index, (name, content) in enumerate(grouped.items()):
        left = index * (pw + 12) / 6
        width = (pw - 5 * 12) / 6
        title_row = next(row for row in content if row["id"].startswith("Product name"))
        photo = f'<img class="flash-product-photo" src="assets/index2/products/3-{index+1}.webp" alt="" width="275" height="175">'
        labels = photo + "".join(text_markup(row, px+left, py, "h3" if row is title_row else ("del" if row["id"].startswith("Original price") else "p")) for row in content)
        for action in section["actions"]:
            if action["card"] == name:
                kind = "favorite" if action["name"] == "heart" else "buy"
                label = "Yêu thích " + title_row["text"] if kind == "favorite" else action["name"]
                labels += action_markup(action, px+left, py, kind, label)
        cards.append(f'<li><article data-product="3-{index+1}" style="left:{left:.6f}px;width:{width:.6f}px">{labels}</article></li>')
    controls = []
    for index, action in enumerate(a for a in section["actions"] if a["kind"].startswith("famicons:")):
        controls.append(action_markup(action, 0, section["top"], "previous" if index == 0 else "next", "Sản phẩm trước" if index == 0 else "Sản phẩm tiếp theo"))
    categories = []
    for index, piece in enumerate(pieces[2:], 2):
        x, y, width, height = piece["viewBox"]
        content = "".join(text_markup(rows[item["key"]], x, y) for item in piece["texts"])
        if index > 2:
            label = piece["texts"][0]["text"]
            action = {"name": label, "box": {"x": x, "y": y, "w": width, "h": height}}
            content += action_markup(action, x, y, "filter")
        style = f'--x:{x}px;--y:{y-section["top"]}px;--w:{width}px;--h:{height}px'
        categories.append(f'<li class="flash-category" style="{style}">{save_graphics(piece["background"], str(index)+".svg")}{content}</li>')
    return (
        '<section id="section-3" data-section="3" class="flash-sale"><div class="flash-canvas catalog">'
        + '<div class="flash-desktop-art">' + save_graphics(section["background"], "desktop.svg") + '</div>'
        + f'<header class="flash-header" style="--x:{hx}px;--y:{hy-section["top"]}px;--w:{hw}px;--h:{hh}px"><div class="flash-header-stage">'
        + save_graphics(header["background"], "header.svg") + header_text + '</div></header>'
        + f'<div class="products flash-products" tabindex="0" role="region" aria-label="Sản phẩm Flash Sale" style="--x:{px}px;--y:{py-section["top"]}px;--w:{pw}px;--h:{ph}px">'
        + '<div class="flash-product-stage">' + save_graphics(products["background"], "products.svg") + '<ul>' + "".join(cards) + '</ul></div></div>'
        + "".join(controls) + '<ul class="flash-categories">' + "".join(categories) + '</ul></div></section>'
    )
