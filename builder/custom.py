"""The custom parts (customparts.py) as local LDraw files, so the renders, the booklet and the Studio
zip use the same part files."""
import customparts

PARTS = {f"{name}.dat": (lambda n=name: customparts.dat(n)) for name in customparts.PARTS}


def install(ldr_module):
    for name, fn in PARTS.items():
        ldr_module.LOCAL_PARTS[name] = fn()
