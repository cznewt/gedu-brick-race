# User guide

## Get the files

Open the latest [release](https://github.com/cznewt/gedu-lego-racing/releases) and download the files
of the car you want. The [README](../README.md#download) lists what each file is.

## Build from the booklet

Print `<model>-instructions.pdf` on A4:
- **Page 1:** the cover.
- **Page 2:** every part with its count.
- **Then:** two steps a page. In each step, the parts that step adds have a red outline, and a
  callout shows those parts with their counts.

The electronics don't come from LEGO:
- the Wukong board with its 7 × 5 LEGO base;
- the Geekservo 360° servos;
- for `wukong-mecanum`, its mecanum wheels.

`<model>-parts.csv` gives a shop link for each of them.

## Order the LEGO parts

On BrickLink, open *Want* > *Upload* and upload `<model>-bricklink.xml`. It lists the LEGO parts
with their colours and counts, without the electronics. `<model>-parts.csv` has the same list plus
the electronics, for a spreadsheet.

## Open the car in BrickLink Studio

1. Unzip `<model>-studio.zip`.
2. Install the custom parts once (also in `README.txt` inside the zip):
   1. Close Studio.
   2. Copy the `.dat` files from the zip's `parts` folder into Studio's `CustomParts\parts` folder:
      - **Windows:** `%LOCALAPPDATA%\Stud.io\CustomParts\parts`
      - **macOS:** `~/.local/share/Stud.io/CustomParts/parts`
   3. If `CustomParts` is missing, create it with the folders `parts`, `connectivity` and
      `collider` inside.
3. Start Studio and open `<model>.ldr` (*File* > *Open*). The building steps come with it.
4. The custom parts are in the parts palette under *Custom Parts*.

They have no Studio connection points, so they do not snap: move them by hand. To make one snap,
add its connectors in Studio's Part Designer.

## Drive it

1. Flash the car's program from the [README](../README.md#drive-it) onto its micro:bit.
2. Open the [phone joystick](https://makecode-microbit.geekedu.eu/joystick/) (Chrome on Android,
   Bluefy on iPhone) and connect to the car.
3. Before the first race, lift the car and tap *Test motors*. Each motor turns forward and then
   back, and the car shows the motor's number.
   - On the tanks, a track that turns back first: flip that motor's setting at the top of the
     program (`LEFT` / `RIGHT` on the two-motor tank, `LEFT_FRONT`, `LEFT_REAR`, `RIGHT_FRONT`,
     `RIGHT_REAR` on the four-motor one).
   - The mecanum car has no such settings: each servo must sit in its port (see the wiring
     drawing). Its test steps 5 to 7 drive forward, slide right and turn right. A wheel that is
     right in 5 but wrong in 6 is plugged into another motor's port.
