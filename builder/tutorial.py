"""Turn rendered build steps into instruction pages: the parts added in a step get a red
outline (pixels that differ from the previous step, same camera and crop), and a callout
box lists that step's parts with their counts, like the official Wonder kit booklets."""
import json
import os
import sys
from collections import Counter

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RED = (227, 0, 11)
CALLOUT_BG = (214, 236, 251)


def new_parts_mask(mask_img, max_hole=2500):
    """mask_img: the step rendered with its new parts in flat black (render.py maskFrom)."""
    mask = np.array(mask_img.convert("L")) < 128
    # pin holes and gaps inside a new part show unchanged pixels: fill them, so only the
    # part's silhouette gets the outline
    labels, n = ndimage.label(~mask)
    sizes = ndimage.sum(np.ones_like(labels), labels, range(1, n + 1))
    border = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]])))
    holes = [i + 1 for i, s in enumerate(sizes) if s < max_hole and (i + 1) not in border]
    mask |= np.isin(labels, holes)
    return Image.fromarray((mask * 255).astype(np.uint8))


def outline(img, mask, width=2):
    ring = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(2 * width + 1)), mask)
    out = img.copy()
    out.paste(Image.new("RGB", img.size, RED), (0, 0), ring)
    return out


def icon(path, box=84):
    im = Image.open(path).convert("RGB")
    bb = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
    im = im.crop(bb) if bb else im
    im.thumbnail((box, box), Image.LANCZOS)
    return im


def callout(items, icons_dir, box=84):
    font = ImageFont.truetype(FONT, 18)
    tiles = []
    for (part, color), n in items:
        ic = icon(f"{icons_dir}/{part}-{color}.png", box)
        t = Image.new("RGB", (max(ic.width, 40), box + 26), CALLOUT_BG)
        t.paste(ic, ((t.width - ic.width) // 2, box - ic.height))
        ImageDraw.Draw(t).text((t.width // 2, box + 2), f"{n}x", font=font, fill="black", anchor="ma")
        tiles.append(t)
    pad, gap = 12, 18
    w = sum(t.width for t in tiles) + gap * (len(tiles) - 1) + 2 * pad
    h = box + 26 + 2 * pad
    c = Image.new("RGB", (w, h), CALLOUT_BG)
    x = pad
    for t in tiles:
        c.paste(t, (x, pad))
        x += t.width + gap
    ImageDraw.Draw(c).rectangle((0, 0, w - 1, h - 1), outline="black", width=2)
    return c


def page(number, model_img, co):
    num_font = ImageFont.truetype(FONT_BOLD, 44)
    top = 18 + co.height + 12
    w = max(model_img.width, 90 + co.width + 24)
    canvas = Image.new("RGB", (w, top + model_img.height), "white")
    d = ImageDraw.Draw(canvas)
    d.text((18, 14), str(number), font=num_font, fill="black")
    canvas.paste(co, (90, 18))
    canvas.paste(model_img, ((w - model_img.width) // 2, top))
    return canvas


def build(outdir):
    steps = json.load(open(f"{outdir}/steps.json"))
    os.makedirs(f"{outdir}/tutorial", exist_ok=True)
    for i, parts in enumerate(steps, 1):
        cur = Image.open(f"{outdir}/steps/step-{i:02d}.png").convert("RGB")
        marked = outline(cur, new_parts_mask(Image.open(f"{outdir}/masks/step-{i:02d}.png")))
        items = list(Counter((p["part"], p["color"]) for p in parts).items())
        page(i, marked, callout(items, f"{outdir}/icons")).save(f"{outdir}/tutorial/step-{i:02d}.png")
    return len(steps)


if __name__ == "__main__":
    print("pages:", build(sys.argv[1]))
