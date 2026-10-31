"""Copy each car's Bluetooth driver from the GeekEdu MakeCode editor into firmware/<model>/main.ts.

The drivers are made and released in the editor (its Brick Race row), stamped with the
editor's release (the micro:bit scrolls it at start). Run this after an editor release, check the
diff, then build:

    python3 firmware/sync.py
"""
import os
import re
import sys
import urllib.request

EDITOR = "https://makecode-microbit.geekedu.eu"
DRIVERS = {                                   # firmware folder: the editor's project, settings changed here
    # the 1:1 gear pairs turn each wheel the other way round: the mecanum driver with DIRECTION -1 (editor r35)
    "wukong-mecanum": ("elecfreak-wukong-mecanum-car-bluetooth", {"DIRECTION": -1}),
    "wukong-tank-2-motors": ("geekedu-wukong-tank-2servo-bluetooth", {}),
    "wukong-tank-4-motors": ("geekedu-wukong-tank-4servo-bluetooth", {}),
    # the 2:1 gears turn each track the other way round: the four-servo driver with every servo at -1
    "wukong-tank-4-motors-geared": ("geekedu-wukong-tank-4servo-bluetooth",
                                    {"LEFT_FRONT": -1, "LEFT_REAR": -1, "RIGHT_FRONT": -1, "RIGHT_REAR": -1}),
}
EXTENSIONS = {"bluetooth", "wuKong"}          # what pxt.json depends on besides core
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    for folder, (project, settings) in DRIVERS.items():
        md = urllib.request.urlopen(f"{EDITOR}/docs/projects/{project}.md", timeout=60).read().decode("utf-8")
        code = re.search(r"```blocks\n(.*?)\n```", md, re.S).group(1)
        for name, value in settings.items():
            code, n = re.subn(rf"^let {name} = -?[\d.]+$", f"let {name} = {value}", code, flags=re.M)
            if n != 1:
                sys.exit(f"{project}: no 'let {name} = ...' line to set for {folder}")
        packages = set(re.search(r"```package\n(.*?)\n```", md, re.S).group(1).split())
        if packages != EXTENSIONS:
            sys.exit(f"{project}: extensions {sorted(packages)}, pxt.json has {sorted(EXTENSIONS)}")
        release = re.search(r'basic\.showString\("(r\d+)"\)', code)
        path = os.path.join(HERE, folder, "main.ts")
        open(path, "w", encoding="utf-8").write(code + "\n")
        changed = ", ".join(f"{k} = {v}" for k, v in settings.items())
        print(f"{folder}: {project}, release {release.group(1) if release else '?'}, {len(code.splitlines())} lines"
              + (f", {changed}" if changed else ""))


if __name__ == "__main__":
    main()
