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
