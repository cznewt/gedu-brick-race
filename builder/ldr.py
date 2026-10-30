"""Small LDraw toolkit: fetch/cache parts, flatten geometry, find Technic holes,
assemble models with exact placements and write MPD files with build steps."""
import os
import re
import urllib.error
import urllib.request

import numpy as np

LIBS = ["https://raw.githubusercontent.com/gkjohnson/ldraw-parts-library/master/complete/ldraw/",
        "https://cdn.jsdelivr.net/gh/gkjohnson/ldraw-parts-library@master/complete/ldraw/"]
CACHE = os.environ.get("LDRAW_CACHE") or os.path.expanduser("~/.cache/geekedu-ldraw")
LOCAL_PARTS = {}          # name -> text, for our own custom parts
MISSING = set()


def _norm(name):
    return name.strip().replace("\\", "/").lower()


def write_atomic(path, data):
    """Several builds share the cache: never let one read a half-written file."""
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)


def fetch(name):
    name = _norm(name)
    if name in LOCAL_PARTS:
        return LOCAL_PARTS[name]
    for sub in ("parts/", "p/", "models/"):
        path = os.path.join(CACHE, sub, name)
        if os.path.exists(path):
            return open(path, encoding="latin-1").read()
    for sub in ("parts/", "p/"):
        data, missing = None, 0
        for lib in LIBS:
            for attempt in range(3):
                try:
                    data = urllib.request.urlopen(lib + sub + name, timeout=60).read().decode("latin-1")
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        missing += 1
                        break
                except (TimeoutError, urllib.error.URLError, ConnectionError):
                    continue
            if data is not None or missing:
                break
        if data is None:
            continue
        path = os.path.join(CACHE, sub, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        write_atomic(path, data.encode("latin-1"))
        return data
    raise FileNotFoundError(name)


def lines(name):
    for line in fetch(name).splitlines():
        f = line.split()
        if f:
            yield f


def mat(f):
    """Line type 1 fields -> (3x3 rotation/scale, translation)."""
    x, y, z, a, b, c, d, e, g, h, i, j = map(float, f[2:14])
    return np.array([[a, b, c], [d, e, g], [h, i, j]]), np.array([x, y, z])


HOLE_RE = re.compile(r"(beamhole|peghole|connhole|axlehole|axl\dhole|axlhole|npeghol|confric|axleh)", re.I)


def holes(name, M=None, t=None, depth=0, _seen=None):
    """Technic hole primitives in a part (recursing into its subparts, not into
    primitives): list of (kind, centre, axis) in the part's coordinates."""
    if M is None:
        M, t = np.eye(3), np.zeros(3)
    out = []
    for f in lines(name):
        if f[0] != "1" or len(f) < 15:
            continue
        sub = _norm(" ".join(f[14:]))
        m, tr = mat(f)
        M2, t2 = M @ m, M @ tr + t
        base = os.path.basename(sub)
        if HOLE_RE.search(base) and not sub.startswith("s/"):
            axis = M2 @ np.array([0.0, 1.0, 0.0])
            n = np.linalg.norm(axis)
            out.append((base[:-4], np.round(t2, 3), np.round(axis / n if n else axis, 3), round(float(n), 3)))
        elif sub.startswith("s/") or (depth == 0 and not base.startswith(("4-4", "2-4", "1-4", "3-4", "1-8", "3-8", "rect", "box", "stud", "ring", "edge", "cyl", "disc", "ndis", "48/", "8/"))):
            try:
                out += holes(sub, M2, t2, depth + 1)
            except FileNotFoundError:
                pass
    return out


def flatten(name, M=None, t=None, depth=0):
    """All vertices of a part (for bounding boxes)."""
    if M is None:
        M, t = np.eye(3), np.zeros(3)
    pts = []
    if depth > 12:
        return pts
    for f in lines(name):
        if f[0] == "1" and len(f) >= 15:
            m, tr = mat(f)
            try:
                pts += flatten(" ".join(f[14:]), M @ m, M @ tr + t, depth + 1)
            except FileNotFoundError as e:
                MISSING.add(str(e))
        elif f[0] in ("3", "4") and len(f) >= 2 + 3 * int(f[0]):
            k = int(f[0])
            for v in range(k):
                p = np.array(list(map(float, f[2 + 3 * v:5 + 3 * v])))
                pts.append(M @ p + t)
    return pts


def bbox(name):
    p = np.array(flatten(name))
    return p.min(0).round(2), p.max(0).round(2)


def title(name):
    for line in fetch(name).splitlines():
        if line.startswith("0 "):
            return line[2:].strip()
    return name


# ---------------------------------------------------------------- rotations
def rot(axis, deg):
    a = np.radians(deg)
    c, s = np.cos(a), np.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def R(*steps):
    """R(('x', 90), ('y', 180)) applies the rotations left to right."""
    M = np.eye(3)
    for axis, deg in steps:
        M = rot(axis, deg) @ M
    return M


# ---------------------------------------------------------------- model
class Model:
    def __init__(self, name):
        self.name = name
        self.steps = [[]]
        self.subfiles = {}

    def add(self, part, color, pos=(0, 0, 0), M=None, note=""):
        M = np.eye(3) if M is None else np.asarray(M, dtype=float)
        self.steps[-1].append((part, color, np.asarray(pos, dtype=float), M, note))
        return M, np.asarray(pos, dtype=float)

    def step(self):
        if self.steps[-1]:
            self.steps.append([])

    @staticmethod
    def line(part, color, pos, M):
        f = lambda v: ("%.4f" % v).rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"
        m = M.flatten()
        return "1 %s %s %s %s %s %s" % (color, f(pos[0]), f(pos[1]), f(pos[2]), " ".join(f(v) for v in m), part)

    def mpd(self, upto=None, extra_files=None):
        out = [f"0 FILE {self.name}.ldr", f"0 {self.name}", f"0 Name: {self.name}.ldr", "0 Author: GeekEdu", ""]
        steps = [s for s in self.steps if s]
        for i, s in enumerate(steps[: upto if upto else None]):
            for part, color, pos, M, note in s:
                out.append(self.line(part, color, pos, M))
            out.append("0 STEP")
        text = "\n".join(out) + "\n"
        for n, body in (extra_files or {}).items():
            text += f"\n0 FILE {n}\n{body.rstrip()}\n"
        return text

    def parts_count(self):
        from collections import Counter
        return Counter((p, c) for s in self.steps for p, c, _, _, _ in s)
