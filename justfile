# Build the models into dist/ (builder/build.py)

default:
    @just --list

# Python packages and the headless Chromium the renders use
setup:
    pip install -r requirements.txt
    python3 -m playwright install chromium

# one model, by its script name: just build wukong_mecanum
build model:
    python3 builder/build.py {{model}}

# every model in models/
all:
    python3 builder/build.py --all

# only a model's cover: dist/<slug>/cover.png
cover model:
    python3 builder/build.py {{model}} --cover

clean:
    rm -rf dist

# the cars' micro:bit programs: dist/<model>/<model>-firmware.hex (Node.js in a container)
firmware:
    docker run --rm --user $(id -u):$(id -g) -e HOME=/tmp -v "$PWD":/w -w /w node:20 sh firmware/build.sh

# copy the drivers' current release from the GeekEdu MakeCode editor into firmware/*/main.ts
sync-firmware:
    python3 firmware/sync.py
