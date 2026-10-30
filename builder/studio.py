"""The downloads beside the booklet: the model for BrickLink Studio with the custom parts it needs
and how to install them (EN, CS), a BrickLink wanted list of its LEGO parts and a parts list."""
import csv
import os
import zipfile
from xml.sax.saxutils import escape

import colors
import customparts
import ldr


def counts(model):
    """{(part id, LDraw colour): quantity}, the custom parts with them."""
    return {(part[:-4], color): q for (part, color), q in sorted(model.parts_count().items())}


def studio_zip(meta, ldr_path, used_custom, dest):
    name = os.path.basename(ldr_path)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", customparts.model_readme(meta["title"], name, "en", bool(used_custom)))
        z.writestr("README-cs.txt", customparts.model_readme(meta["title_cs"], name, "cs", bool(used_custom)))
        z.write(ldr_path, name)
        for part in used_custom:
            z.writestr(f"parts/{part}.dat", customparts.dat(part).replace("\n", "\r\n"))


def wanted_list(rows, dest):
    out = ["<INVENTORY>"]
    for part, color, q in rows:
        bl = colors.bl_color(color)
        out.append(f"  <ITEM><ITEMTYPE>P</ITEMTYPE><ITEMID>{escape(part)}</ITEMID>"
                   + (f"<COLOR>{bl}</COLOR>" if bl else "") + f"<MINQTY>{q}</MINQTY></ITEM>")
    out.append("</INVENTORY>")
    open(dest, "w", encoding="utf-8").write("\n".join(out) + "\n")


def parts_csv(model_counts, dest):
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["part", "ldraw_colour", "bricklink_colour", "colour", "quantity", "description", "where"])
        for (part, color), q in model_counts.items():
            custom = customparts.PARTS.get(part)
            bl = colors.bl_color(color)
            w.writerow([part, color, "" if custom else bl, "" if custom else colors.color_name(bl), q,
                        custom["title"] if custom else ldr.title(f"{part}.dat"),
                        custom["shop"] if custom else f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={part}"])


def write(model, meta, dest):
    """Next to the bundle in dest: <slug>-studio.zip, <slug>-bricklink.xml, <slug>-parts.csv."""
    slug = meta["slug"]
    c = counts(model)
    used_custom = sorted({p for p, _ in c if p in customparts.PARTS})
    studio_zip(meta, f"{dest}/{slug}.ldr", used_custom, f"{dest}/{slug}-studio.zip")
    wanted_list([(p, color, q) for (p, color), q in c.items() if p not in customparts.PARTS], f"{dest}/{slug}-bricklink.xml")
    parts_csv(c, f"{dest}/{slug}-parts.csv")
