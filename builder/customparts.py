"""The ElecFreaks electronics these models use, as LDraw parts at their real size (Kittenbot/ElecFreaks
drawings, ElecFreaks Wukong spec), so the renders, the booklet and the Studio zip all use the same part
files; 1 mm = 2.5 LDU, Y points down.

The Wukong board carries its Technic holes where the real one has them, so models pin onto it; its
origin is the centre of its 7 x 5 base (the footprint of Technic frame 64179, x +-50, z +-70).
"""
import math

MM = 2.5
EDGE = 24


def _box(x0, y0, z0, x1, y1, z1, color=16):
    x0, y0, z0, x1, y1, z1 = (round(v * MM, 2) for v in (x0, y0, z0, x1, y1, z1))
    c = [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1),
         (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    pt = lambda i: " ".join(f"{v:g}" for v in c[i])
    lines = [f"4 {color} " + " ".join(pt(i) for i in f) for f in faces]
    lines += [f"2 {EDGE} {pt(a)} {pt(b)}" for a, b in edges]
    return lines


def _cross_axle(cx, top, height, cz, color=15):
    # a LEGO cross axle seen from above: two 4.8 x 1.8 mm bars
    return (_box(cx - 2.4, top - height, cz - 0.9, cx + 2.4, top, cz + 0.9, color)
            + _box(cx - 0.9, top - height, cz - 2.4, cx + 0.9, top, cz + 2.4, color))


def _geekservo(output_color=72):
    # Kittenbot drawing: body 24 x 28.8 x 16 mm (x, y, z), 8 mm lugs at both ends in the middle
    # 9.6 mm band, 32 mm apart, each with ONE pin hole, across (z): the drawing's two small holes
    # down through each lug are screw holes, not pin holes (the real part, 2026-10-30: a design
    # that ran an axle through them could not be built); the cross axle output on top, 4 mm off
    # centre (origin = body centre)
    out = (_box(-12, -14.4, -8, 12, 14.4, 8)
           + _box(-20, -4.8, -8, -12, 4.8, 8)
           + _box(12, -4.8, -8, 20, 4.8, 8)
           + _cross_axle(4, -14.4, 5.6, 0, output_color))
    for x in (-40, 40):
        out += _disc((x, 0, -20.2), "z", 6) + _disc((x, 0, 20.2), "z", 6)
    return out + _disc((10, -36.2, 0), "y", 8, output_color)


def _box_ldu(x0, y0, z0, x1, y1, z1, color=16, edges=True):
    c = [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    pt = lambda i: " ".join(f"{v:g}" for v in c[i])
    out = [f"4 {color} " + " ".join(pt(i) for i in f) for f in faces]
    if edges:
        out += [f"2 {EDGE} {pt(a)} {pt(b)}" for a, b in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]]
    return out


def _disc(center, normal, r, color=0):
    x, y, z = center
    m = {"x": (0, 1, 0, r, 0, 0, 0, 0, r), "y": (r, 0, 0, 0, 1, 0, 0, 0, r), "z": (r, 0, 0, 0, 0, r, 0, 1, 0)}[normal]
    head = f"1 {color} {x:g} {y:g} {z:g} " + " ".join(f"{v:g}" for v in m)
    return [head + " 4-4disc.dat", head + " 4-4edge.dat"]


def _wukong_board():
    out = _box_ldu(-50, -10, -70, 50, 10, 70)                 # base, main colour
    for x in (-40, 40):
        for z in range(-60, 61, 20):
            out += _disc((x, -10.2, z), "y", 6) + _disc((x, 10.2, z), "y", 6)
    for z in (-60, 60):
        for x in (-20, 0, 20):
            out += _disc((x, -10.2, z), "y", 6) + _disc((x, 10.2, z), "y", 6)
    out += _box_ldu(-50, -14, -70, 50, -10, 70, 0)            # board
    out += _box_ldu(-46, -26, -40, 6, -14, 40, 72)            # battery holder
    out += _box_ldu(18, -60, -64, 32, -14, 64, 14)            # micro:bit edge connector slot
    for z in range(-60, 61, 8):                               # servo and sensor headers
        out += _box_ldu(36, -24, z - 2, 46, -14, z + 2, 0, edges=False)
    return out


def _num(v):
    return ("%.3f" % v).rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"


def _cylinder(p0, w, r, length, color, ends=True):
    """A cylinder of radius r from p0 along the unit vector w (4-4cyli with edges and end discs)."""
    a = (0.0, 1.0, 0.0) if abs(w[1]) < 0.9 else (1.0, 0.0, 0.0)
    u = (a[1] * w[2] - a[2] * w[1], a[2] * w[0] - a[0] * w[2], a[0] * w[1] - a[1] * w[0])
    n = sum(c * c for c in u) ** 0.5
    u = tuple(c / n for c in u)
    v = (w[1] * u[2] - w[2] * u[1], w[2] * u[0] - w[0] * u[2], w[0] * u[1] - w[1] * u[0])
    m = [r * u[0], length * w[0], r * v[0], r * u[1], length * w[1], r * v[1], r * u[2], length * w[2], r * v[2]]
    p1 = tuple(p0[i] + length * w[i] for i in range(3))
    head = lambda p, mm=m: f"1 {color} " + " ".join(_num(c) for c in (*p, *mm))
    out = [head(p0) + " 4-4cyli.dat", head(p0) + " 4-4edge.dat", head(p1) + " 4-4edge.dat"]
    if ends:
        # the disc primitive is one-sided: draw it both ways so the ends show from either side
        flipped = [-c if i % 3 == 1 else c for i, c in enumerate(m)]
        out += [head(p, mm) + " 4-4disc.dat" for p in (p0, p1) for mm in (m, flipped)]
    return out


def _mecanum(hand):
    # ElecFreaks mecanum wheel, 80 mm across and 42 mm wide; axle (cross hole) along Z like LEGO
    # wheels; ten black rollers at 45 degrees, hand = +1 or -1 for the two mirror wheels
    width = 105.0
    out = _cylinder((0, 0, -width / 2 + 4), (0, 0, 1), 22, width - 8, 16)
    for z0 in (-width / 2 + 4, width / 2 - 10):
        out += _cylinder((0, 0, z0), (0, 0, 1), 92, 6, 16)         # side plates, clear of the rollers' ends
    for zf in (-width / 2 + 3.7, width / 2 - 4):
        out += _box_ldu(-6, -1.8, zf, 6, 1.8, zf + 0.3, 0, edges=False) + _box_ldu(-1.8, -6, zf, 1.8, 6, zf + 0.3, 0, edges=False)
    s = math.sqrt(0.5)
    for k in range(10):
        a = 2 * math.pi * k / 10
        radial, tangent = (math.cos(a), math.sin(a), 0.0), (-math.sin(a), math.cos(a), 0.0)
        w = (tangent[0] * s, tangent[1] * s, hand * s)
        p0 = tuple(88 * radial[i] - 40 * w[i] for i in range(3))
        out += _cylinder(p0, w, 13, 80, 0)
    return out


PARTS = {
    "geekedu-ef-geekservo-360": dict(
        title="ElecFreaks Geekservo 360° servo (green)", color=27, vendor="ElecFreaks",
        shop="https://shop.elecfreaks.com/search?q=geekservo%20360",
        geometry=lambda: _geekservo(25)),
    "geekedu-ef-mecanum-wheel-left": dict(
        title="ElecFreaks mecanum wheel 80 mm (left)", color=14, vendor="ElecFreaks",
        shop="https://shop.elecfreaks.com/products/elecfreaks-micro-bit-wonder-rugged-car-kit-without-micro-bit-board",
        geometry=lambda: _mecanum(1)),
    "geekedu-ef-mecanum-wheel-right": dict(
        title="ElecFreaks mecanum wheel 80 mm (right)", color=14, vendor="ElecFreaks",
        shop="https://shop.elecfreaks.com/products/elecfreaks-micro-bit-wonder-rugged-car-kit-without-micro-bit-board",
        geometry=lambda: _mecanum(-1)),
    "geekedu-ef-wukong-board": dict(
        title="ElecFreaks Wukong board on its 7 x 5 LEGO base", color=71, vendor="ElecFreaks",
        shop="https://www.elecfreaks.com/wukong-board-with-lego-holder-for-micro-bit.html",
        geometry=_wukong_board),
}


def dat(name):
    p = PARTS[name]
    head = [
        f"0 {p['title']}",
        f"0 Name: {name}.dat",
        "0 Author: GeekEdu",
        "0 !LDRAW_ORG Unofficial_Part",
        "0 !LICENSE Licensed under CC BY 4.0 : see CAreadme.txt",
        "0 BFC NOCERTIFY",
        "",
    ]
    return "\n".join(head + p["geometry"]()) + "\n"


INSTALL = {
    "en": """Install the custom parts
------------------------
1. Close Studio.
2. Copy the .dat files from the "parts" folder of this zip into Studio's
   CustomParts\\parts folder. If CustomParts is missing, create it with the
   folders parts, connectivity and collider inside.
     Windows: %LOCALAPPDATA%\\Stud.io\\CustomParts\\parts
     macOS:   ~/.local/share/Stud.io/CustomParts/parts
              (a hidden folder: in Finder use Go > Go to Folder, Shift-Cmd-G)
3. Start Studio and switch the parts palette from "Master" to "Custom Parts".

The parts have no Studio connection points, so they do not snap: place them
by hand. The Wukong board has its pin holes where the real one has them. To
make a part snap, open it in Studio's Part Designer, add the connectors and
export it to Studio.
""",
    "cs": """Instalace vlastních dílů
------------------------
1. Zavřete Studio.
2. Zkopírujte soubory .dat ze složky "parts" v tomto zipu do složky
   CustomParts\\parts ve Studiu. Pokud složka CustomParts chybí, vytvořte ji
   a v ní složky parts, connectivity a collider.
     Windows: %LOCALAPPDATA%\\Stud.io\\CustomParts\\parts
     macOS:   ~/.local/share/Stud.io/CustomParts/parts
              (skrytá složka: ve Finderu Otevřít > Otevřít složku, Shift-Cmd-G)
3. Spusťte Studio a v paletě dílů přepněte z "Master" na "Custom Parts".

Díly nemají ve Studiu spojovací body, takže se samy nepřichytí: umístěte je
ručně. Deska Wukong má otvory pro kolíky tam, kde je má skutečná deska. Aby
se díl přichytil, otevřete ho v Part Designeru ve Studiu, přidejte spoje a
vyexportujte ho do Studia.
""",
}


def model_readme(title, filename, lang="en", custom_parts=True):
    if lang == "cs":
        text = f"{title} pro BrickLink Studio\n\n{filename} je model s postupem stavby.\n"
        if custom_parts:
            text += ("Elektronika ElecFreaks (serva, kola, deska Wukong) jsou vlastní díly GeekEdu:\n"
                     "nejdřív je nainstalujte.\n\n" + INSTALL["cs"])
        text += f"\nPotom otevřete {filename} ve Studiu (File > Open nebo File > Import).\n"
    else:
        text = f"{title} for BrickLink Studio\n\n{filename} is the model with its building steps.\n"
        if custom_parts:
            text += ("Its ElecFreaks electronics (servos, wheels, the Wukong board) are GeekEdu custom parts:\n"
                     "install them first.\n\n" + INSTALL["en"])
        text += f"\nThen open {filename} in Studio (File > Open, or File > Import).\n"
    return text.replace("\n", "\r\n")
