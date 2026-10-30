"""Copy each car's Bluetooth driver from the GeekEdu MakeCode editor into firmware/<model>/main.ts.

The drivers are made and released in the editor (its LEGO Racing Challenge row), stamped with the
editor's release (the micro:bit scrolls it at start). Run this after an editor release, check the
diff, then build:

    python3 firmware/sync.py
"""
import os
import re
import sys
import urllib.request

EDITOR = "https://makecode-microbit.geekedu.eu"
DRIVERS = {                                   # firmware folder: the editor's project
    "wukong-mecanum": "elecfreak-wukong-mecanum-car-bluetooth",
    "wukong-tank-2-motors": "geekedu-wukong-tank-2servo-bluetooth",
    "wukong-tank-4-motors": "geekedu-wukong-tank-4servo-bluetooth",
}
EXTENSIONS = {"bluetooth", "wuKong"}          # what pxt.json depends on besides core
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    for folder, project in DRIVERS.items():
        md = urllib.request.urlopen(f"{EDITOR}/docs/projects/{project}.md", timeout=60).read().decode("utf-8")
        code = re.search(r"```blocks\n(.*?)\n```", md, re.S).group(1)
        packages = set(re.search(r"```package\n(.*?)\n```", md, re.S).group(1).split())
        if packages != EXTENSIONS:
            sys.exit(f"{project}: extensions {sorted(packages)}, pxt.json has {sorted(EXTENSIONS)}")
        release = re.search(r'basic\.showString\("(r\d+)"\)', code)
        path = os.path.join(HERE, folder, "main.ts")
        open(path, "w", encoding="utf-8").write(code + "\n")
        print(f"{folder}: {project}, release {release.group(1) if release else '?'}, {len(code.splitlines())} lines")


if __name__ == "__main__":
    main()
