# User guide

## Get the files

Open the latest [release](https://github.com/cznewt/gedu-brick-race/releases) and download the files
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

1. Flash the car's program: connect its micro:bit by USB and copy `<model>-firmware.hex` from the
   release onto the `MICROBIT` drive. It scrolls its release (for example `r32`) and shows a heart.
   To change the program, open it in the GeekEdu editor instead (links in the
   [README](../README.md#drive-it)).
2. Open the [phone joystick](https://makecode-microbit.geekedu.eu/joystick/) (Chrome on Android,
   Bluefy on iPhone) and connect to the car.
   - On an Android handheld with sticks, or with a gamepad, the controller drives too once you
     press any of its buttons: the left stick (or the D-pad) drives, the right stick slides.
   - Connect stays a tap on the screen.
3. Before the first race, lift the car and tap *Test motors*. Each motor turns forward and then
   back, and the car shows the motor's number.
   - On the tanks, a track that turns back first: flip that motor's setting at the top of the
     program (`LEFT` / `RIGHT` on the two-motor tank, `LEFT_FRONT`, `LEFT_REAR`, `RIGHT_FRONT`,
     `RIGHT_REAR` on the four-motor one).
   - On the mecanum car, steps 1 to 4 turn the left front, right front, left rear and right rear
     wheel. A different wheel turning means two servos are in each other's ports: swap those plugs
     (see the wiring drawing).
   - Steps 5 to 7 then drive forward, slide right and turn right. If every wheel is in its port and
     the car still twists or slides the wrong way in step 6, a wheel is mounted the other way
     round: set its `SLIDE` at the top of the program to -1 (`LF_SLIDE`, `RF_SLIDE`, `LR_SLIDE`,
     `RR_SLIDE`).
