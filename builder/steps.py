"""Render a model's build steps, cover and part icons."""
import os, shutil, sys, json, numpy as np
import ldr, render, custom

def trim(paths, pad=24):
    """Crop renders to the same box (the union of their content) so steps don't jump."""
    from PIL import Image, ImageChops
    boxes = {}
    for p in paths:
        im = Image.open(p)
        if im.mode == "RGBA":                                 # the cover: rendered on transparent
            boxes[p] = (im, im.getchannel("A").getbbox())
            continue
        im = im.convert("RGB")
        bb = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
        boxes[p] = (im, bb)
    steps = [p for p in paths if "/steps/" in p]
    if steps:
        # masks share the step pictures' box, so they line up pixel for pixel
        x0 = min(boxes[p][1][0] for p in steps); y0 = min(boxes[p][1][1] for p in steps)
        x1 = max(boxes[p][1][2] for p in steps); y1 = max(boxes[p][1][3] for p in steps)
        for p in steps + [p for p in paths if "/masks/" in p]:
            im = boxes[p][0]
            im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad))).save(p)
    for p in paths:
        if "/steps/" not in p and "/masks/" not in p:
            im, bb = boxes[p]
            im = im.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad)))
            if p.endswith("/cover.png"):
                im = pad_to(im, 3 / 2)                # cards crop covers to 3:2
            im.save(p)


def pad_to(im, ratio):
    from PIL import Image
    w, h = (im.width, round(im.width / ratio)) if im.width / im.height > ratio else (round(im.height * ratio), im.height)
    out = Image.new(im.mode, (w, h), (0, 0, 0, 0) if im.mode == "RGBA" else "white")
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def model_files(m):
    used = {p for s in m.steps for p, *_ in s}
    return {n: fn() for n, fn in custom.PARTS.items() if n in used}

def fit_zoom(mpd, cam, outdir, zoom=0.62):
    """Back the camera off until the finished model clears the canvas edges."""
    from PIL import Image, ImageChops
    probe = f"{outdir}/fit.png"
    for _ in range(8):
        render.render([(mpd, probe, dict(cam, zoom=zoom))])
        im = Image.open(probe).convert("RGB")
        x0, y0, x1, y1 = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
        if x0 > 2 and y0 > 2 and x1 < im.width - 2 and y1 < im.height - 2:
            break
        zoom *= 1.1
    os.remove(probe)
    return zoom


def render_model(m, outdir, az=125, el=30, cover_az=125, cover_el=28, step_views=None):
    """step_views: {step number: (azimuth, elevation)} for steps the booklet shows from another side."""
    # a shorter model leaves the longer one's pictures behind: the booklet listed them (2026-10-31)
    for sub in ("steps", "icons", "masks", "tutorial"):
        shutil.rmtree(f"{outdir}/{sub}", ignore_errors=True)
    os.makedirs(f"{outdir}/steps", exist_ok=True); os.makedirs(f"{outdir}/icons", exist_ok=True)
    extra = model_files(m)
    full = m.mpd(extra_files=extra)
    # one framing for every step: the finished model's bounds
    pts = []
    for s in m.steps:
        for part, color, pos, M, _ in s:
            try:
                lo, hi = ldr.bbox(part)
            except Exception:
                continue
            for c in [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]:
                pts.append(M @ np.array(c) + pos)
    pts = np.array(pts); c = (pts.min(0) + pts.max(0)) / 2; r = np.linalg.norm(pts.max(0) - pts.min(0)) / 2
    target = [float(c[0]), float(-c[1]), float(-c[2])]          # three.js frame (group rotated by pi about X)
    jobs = []
    steps = [s for s in m.steps if s]
    n = len(steps)
    os.makedirs(f"{outdir}/masks", exist_ok=True)
    cams = {}

    def camera(view):
        if view not in cams:
            cams[view] = {"azimuth": view[0], "elevation": view[1], "target": target, "radius": r, "width": 1000, "height": 700}
            cams[view]["zoom"] = fit_zoom(full, cams[view], outdir)
        return cams[view]

    cover_cam = {"azimuth": cover_az, "elevation": cover_el, "width": 1200, "height": 800}
    cover_cam["zoom"] = fit_zoom(full, cover_cam, outdir)
    for i in range(1, n + 1):
        cam = camera(tuple((step_views or {}).get(i, (az, el))))
        jobs.append((m.mpd(upto=i, extra_files=extra), f"{outdir}/steps/step-{i:02d}.png", cam))
        before = sum(len(s) for s in steps[:i - 1])
        jobs.append((m.mpd(upto=i, extra_files=extra), f"{outdir}/masks/step-{i:02d}.png",
                     dict(cam, maskFrom=before, expectChildren=before + len(steps[i - 1]))))
    jobs.append((full, f"{outdir}/cover.png", dict(cover_cam, transparent=True)))   # a page shows the car on its own background
    for (part, color), q in sorted(m.parts_count().items()):
        one = ldr.Model("icon"); one.add(part, color)
        jobs.append((one.mpd(extra_files={k: v for k, v in extra.items() if k == part}),
                     f"{outdir}/icons/{part[:-4]}-{color}.png", {"azimuth": 135, "elevation": 30, "width": 240, "height": 240, "zoom": 1.05}))
    render.render(jobs)
    trim([j[1] for j in jobs if "/icons/" not in j[1]])
    with open(f"{outdir}/model.ldr", "w") as fh:
        fh.write(m.mpd())                                     # custom parts come from the site's library
    with open(f"{outdir}/steps.json", "w") as fh:
        json.dump([[{"part": p[:-4], "color": c} for p, c, *_ in s] for s in m.steps if s], fh, indent=1)
    return n


def render_cover(m, outdir, cover_az=125, cover_el=28, **_):
    """Only the cover, as render_model makes it (build.py --cover)."""
    full = m.mpd(extra_files=model_files(m))
    cover_cam = {"azimuth": cover_az, "elevation": cover_el, "width": 1200, "height": 800}
    cover_cam["zoom"] = fit_zoom(full, cover_cam, outdir)
    render.render([(full, f"{outdir}/cover.png", dict(cover_cam, transparent=True))])
    trim([f"{outdir}/cover.png"])
