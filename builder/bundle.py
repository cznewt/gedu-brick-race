"""Assemble a model's folder in dist/: model.json, <slug>.ldr, cover.png, steps/*.png (the
instruction pages) and <slug>-instructions.pdf (A4, printable)."""
import json
import os
import shutil
from collections import Counter

from PIL import Image, ImageChops, ImageDraw, ImageFont
from PIL import JpegImagePlugin  # noqa: F401  registers the encoder the PDF writer uses

import colors
import customparts

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
A4 = (1240, 1754)          # 150 dpi
MARGIN = 70


def trimmed(path):
    im = Image.open(path)
    if im.mode == "RGBA":                                     # the transparent cover, on the white page
        im = Image.alpha_composite(Image.new("RGBA", im.size, "white"), im)
    im = im.convert("RGB")
    bb = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
    return im.crop(bb) if bb else im


def fit(im, w, h):
    s = min(w / im.width, h / im.height)
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)


def footer(page, n, url):
    d = ImageDraw.Draw(page)
    f = ImageFont.truetype(FONT, 20)
    d.text((MARGIN, A4[1] - 50), "GeekEdu  " + url, font=f, fill=(110, 110, 110))
    if n:
        d.text((A4[0] - MARGIN, A4[1] - 50), str(n), font=f, fill=(110, 110, 110), anchor="ra")


def cover_page(meta, outdir, url):
    page = Image.new("RGB", A4, "white")
    d = ImageDraw.Draw(page)
    d.text((MARGIN, 90), meta["title"], font=ImageFont.truetype(FONT_BOLD, 64), fill="black")
    d.text((MARGIN, 175), meta["title_cs"], font=ImageFont.truetype(FONT, 44), fill=(80, 80, 80))
    f = ImageFont.truetype(FONT, 26)
    for k, line in enumerate(wrap(d, meta["source"], f, A4[0] - 2 * MARGIN)[:3]):    # the page holds three lines
        d.text((MARGIN, 250 + 34 * k), line, font=f, fill=(80, 80, 80))
    img = fit(trimmed(f"{outdir}/cover.png"), A4[0] - 2 * MARGIN, 1100)
    page.paste(img, ((A4[0] - img.width) // 2, 380))
    footer(page, 0, url)
    return page


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and d.textlength(trial, font=font) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def parts_page(model, outdir, url):
    page = Image.new("RGB", A4, "white")
    d = ImageDraw.Draw(page)
    d.text((MARGIN, 70), "Parts / Díly", font=ImageFont.truetype(FONT_BOLD, 48), fill="black")
    f, fb = ImageFont.truetype(FONT, 18), ImageFont.truetype(FONT_BOLD, 24)
    counts = Counter((p[:-4], c) for s in model.steps for p, c, *_ in s)
    items = sorted(counts.items(), key=lambda kv: (kv[0][0] in customparts.PARTS, kv[0][0]))
    cols = 5
    cell_w, icon = (A4[0] - 2 * MARGIN) // cols, 140
    rows = -(-len(items) // cols)
    cell_h = min(250, (A4[1] - 170 - 120) // rows)
    for i, ((part, color), n) in enumerate(items):
        x, y = MARGIN + (i % cols) * cell_w, 170 + (i // cols) * cell_h
        im = fit(trimmed(f"{outdir}/icons/{part}-{color}.png"), icon, icon)
        page.paste(im, (x + (cell_w - im.width) // 2, y + icon - im.height))
        d.text((x + cell_w // 2, y + icon + 6), f"{n}x", font=fb, fill="black", anchor="ma")
        if part in customparts.PARTS:
            label = customparts.PARTS[part]["title"].replace("ElecFreaks ", "")
        else:
            label = f"{part} {colors.color_name(colors.bl_color(color))}"
        for k, line in enumerate(wrap(d, label, f, cell_w - 16)[:3]):
            d.text((x + cell_w // 2, y + icon + 38 + k * 22), line, font=f, fill=(60, 60, 60), anchor="ma")
    footer(page, 0, url)
    return page


def step_pages(outdir, url, first_number=1):
    pages, steps = [], sorted(os.listdir(f"{outdir}/tutorial"))
    box_h = (A4[1] - 2 * MARGIN - 60) // 2
    for k in range(0, len(steps), 2):
        page = Image.new("RGB", A4, "white")
        for j, name in enumerate(steps[k:k + 2]):
            im = fit(Image.open(f"{outdir}/tutorial/{name}").convert("RGB"), A4[0] - 2 * MARGIN, box_h - 20)
            page.paste(im, ((A4[0] - im.width) // 2, MARGIN + j * box_h))
        footer(page, first_number + len(pages), url)
        pages.append(page)
    return pages


def save_8bit(im, path):
    """A third of the size and no visible difference for these flat renders."""
    im.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)


REPO = "github.com/cznewt/gedu-lego-racing"


def build(model, meta, outdir, dest):
    url = REPO
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(f"{dest}/steps")
    json.dump({k: meta[k] for k in ("slug", "title", "title_cs", "description", "description_cs")},
              open(f"{dest}/model.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    lines = model.mpd().split("\n")[1:]                    # plain .ldr: no "0 FILE" line
    lines[:3] = [f"0 {meta['title']}", f"0 Name: {meta['slug']}.ldr", "0 Author: GeekEdu"]
    open(f"{dest}/{meta['slug']}.ldr", "w", encoding="utf-8", newline="\r\n").write("\n".join(lines))
    shutil.copy(f"{outdir}/cover.png", f"{dest}/cover.png")
    for name in sorted(os.listdir(f"{outdir}/tutorial")):
        save_8bit(Image.open(f"{outdir}/tutorial/{name}"), f"{dest}/steps/{name}")
    pages = [cover_page(meta, outdir, url), parts_page(model, outdir, url)] + step_pages(outdir, url, 3)
    pages[0].save(f"{dest}/{meta['slug']}-instructions.pdf", save_all=True, append_images=pages[1:], resolution=150, quality=80)
    return len(pages)
