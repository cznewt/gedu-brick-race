"""Tracks of 57518 links round 57519 sprockets (the Building:bit tank's), for any set of wheels:
the links' bars sit PITCH apart in a closed loop round the wheels' convex hull, at the hull
radius that makes the loop close. Wheels are (x, y) in the side view, axles along Z, Y down,
listed so the inside of the loop is on the left going from one to the next (for front = +X:
back wheel first, then forward along the top)."""
import numpy as np

from ldr import R

PITCH = 30                                                  # 57518: bar at z = 0, clip at z = -30
TOOTH_DEG = 36                                              # 57519: 10 teeth 36 degrees apart, one at 0 degrees


class Track:
    def __init__(self, wheels, n_links):
        self.wheels = wheels
        self.n_links = n_links
        self.bars = self._bars()

    def hull_point(self, s, r):
        """Point at arc length s along the wheels' convex hull offset by r (straight runs between
        the wheels, arcs round them), starting in the middle of the first run; and the hull's length."""
        c = [np.array(p, dtype=float) for p in self.wheels]
        n = len(c)
        pieces = []
        for i in range(n):
            d = c[(i + 1) % n] - c[i]
            d /= np.linalg.norm(d)
            out = np.array([d[1], -d[0]])                   # outward normal: the inside is on the left
            d2 = c[(i + 2) % n] - c[(i + 1) % n]
            d2 /= np.linalg.norm(d2)
            out2 = np.array([d2[1], -d2[0]])
            pieces.append(("line", c[i] + r * out, c[(i + 1) % n] + r * out))
            turn = np.arctan2(out[0] * out2[1] - out[1] * out2[0], out @ out2)
            if n == 2:
                turn = np.pi                                # two wheels: the arcs are half circles
            pieces.append(("arc", c[(i + 1) % n], np.arctan2(out[1], out[0]), turn))
        lengths = [np.linalg.norm(p[2] - p[1]) if p[0] == "line" else r * abs(p[3]) for p in pieces]
        total = sum(lengths)
        s = (s + lengths[0] / 2) % total
        for p, length in zip(pieces, lengths):
            if s <= length:
                if p[0] == "line":
                    return p[1] + (p[2] - p[1]) * s / length, total
                a = p[2] + p[3] * s / length
                return p[1] + r * np.array([np.cos(a), np.sin(a)]), total
            s -= length
        return self.hull_point(0, r)

    def chain(self, r):
        """The links' bars round the hull at radius r, each PITCH from the last; and the gap the
        last link has to close."""
        pts, s = [self.hull_point(0, r)[0]], 0.0
        for _ in range(self.n_links - 1):
            lo, hi = s, s + 2 * PITCH
            for _ in range(50):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if np.linalg.norm(self.hull_point(mid, r)[0] - pts[-1]) < PITCH else (lo, mid)
            s = (lo + hi) / 2
            pts.append(self.hull_point(s, r)[0])
        return pts, np.linalg.norm(pts[0] - pts[-1])

    def _bars(self):
        """n_links bars, exactly PITCH apart in a closed loop: the hull radius that makes the loop close."""
        lo, hi = 30.0, 70.0
        for _ in range(50):
            r = (lo + hi) / 2
            lo, hi = (lo, r) if self.chain(r)[1] > PITCH else (r, hi)
        self.radius = (lo + hi) / 2
        return self.chain(self.radius)[0]

    def link_frame(self, k):
        """Link k: bar at bars[k], clip on the next bar, studs side (+y) towards the wheels."""
        p, q = self.bars[k], self.bars[(k + 1) % self.n_links]
        t = (q - p) / np.linalg.norm(q - p)
        inward = np.array([-t[1], t[0], 0.0])
        return p, np.column_stack([(0, 0, 1), inward, (-t[0], -t[1], 0)])

    def sprocket_turn(self, wheel):
        """Turn a sprocket about its axle so a tooth points at the middle of the link nearest the
        middle of the wheel's wrap (the teeth go into the links' middles)."""
        c = np.array(wheel, dtype=float)
        mids = [(self.bars[k] + self.bars[(k + 1) % self.n_links]) / 2 - c for k in range(self.n_links)]
        near = [v for v in mids if np.linalg.norm(v) < 55]
        centroid = np.mean(np.array(self.wheels, dtype=float), axis=0)
        away = c - centroid
        v = max(near, key=lambda v: v @ away / np.linalg.norm(v))
        return R(("z", float(np.degrees(np.arctan2(v[1], v[0]))) % TOOTH_DEG))

    def links(self, m, color, z):
        """All the links, in the plane z."""
        for k in range(self.n_links):
            p, M = self.link_frame(k)
            m.add("57518.dat", color, (p[0], p[1], z), M)
