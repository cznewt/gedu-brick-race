#!/bin/sh
# Compile each firmware/<model>/ with the MakeCode CLI (npx makecode, the micro:bit editor its mkc.json
# names) into dist/<model>/<model>-firmware.hex: one universal hex for micro:bit V1 and V2.
set -e
cd "$(dirname "$0")"
for dir in */; do
    model=${dir%/}
    [ -f "$model/pxt.json" ] || continue
    (cd "$model" && npx -y makecode build)
    mkdir -p "../dist/$model"
    cp "$model/built/binary.hex" "../dist/$model/$model-firmware.hex"
    echo "$model: dist/$model/$model-firmware.hex"
done
