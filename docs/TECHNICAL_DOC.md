# Technical documentation

## Pipeline

`python3 builder/build.py <name>` runs these stages for `models/<name>.py`:

1. **Model** (`models/<name>.py`)
   - `build()` places parts step by step into an `ldr.Model`.
   - Its geometry helpers live in `builder/ldr.py`: the LDraw library, part bounding boxes and
     holes, rotations.
   - The custom parts (`builder/customparts.py`) are registered as local LDraw files.
   - `build.py` compares the parts with `booklet_parts` from the JSON, if the JSON has them.
2. **Renders** (`builder/steps.py`, `builder/render.py`)
   - Every step is drawn twice in headless Chromium with three.js and its `LDrawLoader` (WebGL in
     software): once as a picture and once as a mask, with the step's new parts black.
   - The camera is set once from the finished model's bounds, so steps don't jump. A model's
     `VIEW["step_views"]` turns it for chosen steps.
   - The cover is rendered on a transparent background and padded to 3:2.
   - Each part also gets an icon for the callouts.
3. **Instruction pages** (`builder/tutorial.py`): each step picture gets a red outline around the
   mask (the parts that step adds) and a callout with those parts and their counts.
4. **Booklet** (`builder/bundle.py`): `dist/<slug>/` with:
   - `model.json`;
   - `<slug>.ldr` (Studio and LDraw viewers);
   - `cover.png`;
   - `steps/` as 8-bit PNGs;
   - `<slug>-instructions.pdf`: A4 at 150 dpi, a cover page, the parts page, then two steps a page.
5. **Downloads** (`builder/studio.py`):
   - `<slug>-studio.zip`: the `.ldr`, `parts/*.dat` for the custom parts it uses, and
     `README.txt` / `README-cs.txt`.
   - `<slug>-bricklink.xml`: LEGO parts only, LDraw colours mapped to BrickLink ids by
     `builder/colors.py`.
   - `<slug>-parts.csv`.
6. **Archive:** `build.py` zips the folder into `dist/<slug>.zip`.

## Paths and caches

| What | Where |
|---|---|
| LDraw parts, fetched from gkjohnson/ldraw-parts-library on GitHub (jsDelivr as fallback) | `~/.cache/geekedu-ldraw`, or `LDRAW_CACHE` |
| Renders and work files | `~/.cache/geekedu-lego/<slug>/` |
| Output | `dist/`, or `DIST` |
| three.js | jsDelivr, pinned to 0.160.0 |

## Adding a model

1. Write `models/<name>.py` with `build()`, and optionally `VIEW`. Reuse `tracks.Track` for tracks,
   `wonder_common` for the Wonder kit's frames and pins, and `wukong_mecanum` for the racer's body.
2. Write `models/<name>.json` with:
   - `slug`;
   - `title`, `title_cs`;
   - `description`, `description_cs`;
   - `source`;
   - optionally `booklet_parts` (`{"<part>/<LDraw colour>": count}`).
3. Run `just build <name>` and check `dist/<slug>/steps/`: every new part outlined, nothing
   floating, nothing hidden behind earlier parts.
4. A new electronic part goes into `builder/customparts.py`, with `PARTS[<id>]` = title, colour,
   shop link and geometry. Keep the GeekEdu site's copy identical.

CI picks the model up by its JSON file; no workflow change is needed.

## Firmware

`firmware/<slug>/` is one MakeCode project per car, with the same slug as its model:
- `main.ts`;
- `pxt.json`:
  - `core`, `bluetooth` and ElecFreaks `wuKong` pinned at v1.6.0, the version the GeekEdu editor
    bundles;
  - no `radio`, which can't run beside Bluetooth;
  - `microbit-dal.bluetooth` `open: 1`, `whitelist: 0`: *No Pairing Required*, so the phone joystick
    connects without pairing.
- `mkc.json` pins the editor the CLI compiles against: `makecode.microbit.org/v8`, the line the
  GeekEdu editor runs.
- `README.md`.

**Source of truth: the GeekEdu MakeCode editor.** The drivers are written and released there, and
each one scrolls the editor release it comes from.
- `firmware/sync.py` copies the current Bluetooth drivers from `/docs/projects/<name>.md`: the
  program from the `blocks` section.
- It stops if a driver's extensions are no longer `bluetooth` + `wuKong`; then update `pxt.json`.

**Build:**
- `firmware/build.sh` runs `npx makecode build` in each folder: the MakeCode CLI with the native
  code from MakeCode's compile service.
- It copies `built/binary.hex`, a universal hex for V1 and V2, to `dist/<slug>/<slug>-firmware.hex`.
- The CLI's hex has no MakeCode source in it, unlike a download from the editor.
- Check a build: in the V2 part, look for the UART and event services' base UUIDs
  (`6e400000-…`, `e95d0000-…`) and the release string.

## CI and releases

`.github/workflows/build.yml` runs on every push to `main`, on pull requests, by hand and on
`v*` tags:
- **`models`** lists `models/*.json`.
- **`build`** builds each model in its own job (Python 3.12, Playwright's Chromium, DejaVu fonts),
  caches the LDraw parts and uploads `dist/` as a workflow artifact named after the model.
- **`firmware`** (Node.js 20) builds the firmware hex files.
- **`release`** runs only on a `v*` tag. It collects the artifacts and creates the GitHub Release
  with `<slug>.zip`, `-studio.zip`, `-instructions.pdf`, `-bricklink.xml`, `-parts.csv` and
  `-firmware.hex`.

```sh
git tag v0.2.0 && git push origin v0.2.0
```

## Relation to the GeekEdu site

The builder comes from the one the GeekEdu site uses for its LEGO models, which is not public.
There, the same bundle feeds the site's 3D viewer and downloads. `builder/customparts.py` holds
the four parts these models use; their `.dat` files are identical to the site's. Keep them that
way, so Studio files from either place work together.

## Limits

- The custom parts have no Studio connection points, so they don't snap in Studio.
- Renders need network access unless the LDraw cache is warm.
- Booklet pages are images: the PDF has no selectable text.
