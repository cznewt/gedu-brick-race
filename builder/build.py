"""Build a model, or all of them, from models/<name>.py into dist/<slug>/: the cover, the step
pictures, the A4 booklet, the model for BrickLink Studio, a BrickLink wanted list and the parts list,
then dist/<slug>.zip with all of it.

    python3 builder/build.py wukong_mecanum           one model
    python3 builder/build.py --all                    every models/<name>.py that has a <name>.json
    python3 builder/build.py wukong_mecanum --cover   only dist/<slug>/cover.png
"""
import glob
import importlib.util
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODELS = os.path.join(ROOT, "models")
DIST = os.environ.get("DIST") or os.path.join(ROOT, "dist")
sys.path.insert(0, HERE)
sys.path.insert(0, MODELS)                                   # shared model code (wonder_common, tracks)

import bundle  # noqa: E402
import custom  # noqa: E402
import ldr  # noqa: E402
import steps  # noqa: E402
import studio  # noqa: E402
import tutorial  # noqa: E402


def parts_diff(model, meta):
    """Differences from the booklet's parts list ("booklet_parts": {"<part>/<LDraw colour>": count})."""
    ours = {f"{p[:-4]}/{c}": n for (p, c), n in model.parts_count().items()}
    booklet = meta.get("booklet_parts")
    if booklet is None:
        return None
    return {k: (booklet.get(k, 0), ours.get(k, 0)) for k in sorted(set(ours) | set(booklet)) if booklet.get(k, 0) != ours.get(k, 0)}


def check_parts(model, meta):
    diff = parts_diff(model, meta)
    if diff is None:
        print(f"{meta['slug']}: no booklet_parts to check against")
    elif diff:
        print(f"{meta['slug']}: parts differ from the booklet (part: booklet, ours): {diff}")
    else:
        print(f"{meta['slug']}: parts match the booklet")


def main(name, cover_only=False):
    spec = importlib.util.spec_from_file_location(name, os.path.join(MODELS, f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    meta = json.load(open(os.path.join(MODELS, f"{name}.json"), encoding="utf-8"))
    custom.install(ldr)
    work = os.path.join(os.path.expanduser("~/.cache/geekedu-lego"), meta["slug"])
    os.makedirs(work, exist_ok=True)
    model = mod.build()
    dest = os.path.join(DIST, meta["slug"])
    if cover_only:
        steps.render_cover(model, work, **getattr(mod, "VIEW", {}))
        os.makedirs(dest, exist_ok=True)
        shutil.copy(f"{work}/cover.png", f"{dest}/cover.png")
        print(f"{meta['slug']}: cover -> {dest}/cover.png")
        return
    check_parts(model, meta)
    n = steps.render_model(model, work, **getattr(mod, "VIEW", {}))
    tutorial.build(work)
    pages = bundle.build(model, meta, work, dest)
    studio.write(model, meta, dest)
    shutil.make_archive(dest, "zip", DIST, meta["slug"])
    print(f"{meta['slug']}: {n} steps, {sum(model.parts_count().values())} parts, {pages} PDF pages -> {dest}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--all" in args:
        names = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(MODELS, "*.json")))
    else:
        names = [a for a in args if not a.startswith("--")]
    if not names:
        sys.exit(__doc__)
    for name in names:
        main(name, "--cover" in args)
