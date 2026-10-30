# Firmware

The micro:bit programs for the cars: Bluetooth drivers for the
[phone joystick](https://makecode-microbit.geekedu.eu/joystick/) (Chrome on Android, Bluefy on iPhone).
Each `<model>/` folder is a MakeCode project:
- `main.ts`: the program;
- `pxt.json`: the extensions (`bluetooth`, ElecFreaks `wuKong` v1.6.0) and *No Pairing Required*;
- `mkc.json`: the micro:bit editor it is built with;
- `README.md`: ports, settings and the motor test.

## Flash it

1. Download `<model>-firmware.hex` from a [release](https://github.com/cznewt/gedu-lego-racing/releases).
   It is one file for micro:bit V1 and V2.
2. Connect the micro:bit by USB and copy the file onto its `MICROBIT` drive.
3. It scrolls its release and shows a heart.

The hex has no MakeCode source in it. To read or change a program, open it in the GeekEdu editor
(link in its README) or edit `main.ts` here.

## Where the programs come from

The drivers are written and released in the [GeekEdu MakeCode editor](https://makecode-microbit.geekedu.eu/),
on the *LEGO Racing Challenge* row. The micro:bit scrolls the editor's release at start (`r32`).
`python3 firmware/sync.py` copies the current ones here.

## Build

`firmware/build.sh` compiles each folder with the MakeCode CLI into
`dist/<model>/<model>-firmware.hex`. It needs Node.js and network access (`npx makecode`). The
`just firmware` recipe runs it in a `node:20` container.
