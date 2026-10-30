# Instructions for agents

## What this repo holds

Three LEGO car models (`models/<name>.py` + `<name>.json`) and the builder (`builder/`) that renders
each one into `dist/<slug>/`:
- the cover and step pictures;
- the A4 booklet;
- `<slug>.ldr`;
- the Studio zip;
- the BrickLink wanted list and the parts CSV.

`firmware/` holds each car's micro:bit program, built into `dist/<slug>/<slug>-firmware.hex`.

## Build

- Run `just setup` once, then `just build <script name>` or `just all`.
- Renders need the network: three.js comes from jsDelivr, the LDraw parts from GitHub (cached in
  `~/.cache/geekedu-ldraw`).
- Check a change by rebuilding the model and looking at the pictures in `dist/<slug>/steps/` and
  `cover.png`.

## What goes in git

- Never commit `dist/`: CI builds it and releases carry it.
- `docs/images/` only holds the small README pictures (the covers, 360 px wide). Refresh them when a
  cover changes.

## Models

- `build()` returns an `ldr.Model`: its steps, each a list of placed parts.
- `VIEW` sets cameras: `az`, `el`, `cover_az`, `cover_el`, `step_views`.
- The JSON gives:
  - `slug`, which names the dist folder and files;
  - titles and descriptions in EN and CS;
  - `source`;
  - optionally `booklet_parts`, which `build.py` checks the parts against.
- The tanks import `wukong_mecanum` for the racer's body. A change there changes all three models:
  rebuild them all.

## Shared with the GeekEdu site

- `builder/` is a copy of the builder the GeekEdu site uses, which is not public.
- `builder/customparts.py` must stay byte-identical to the site's parts: the same `.dat` files go
  out from both places.
- Fixes that matter to both go to both.

## Firmware

- `firmware/<slug>/` is one MakeCode project per car: `main.ts`, `pxt.json`, `mkc.json`,
  `README.md`.
- The drivers are made in the GeekEdu MakeCode editor. Don't change `main.ts` here alone: change
  the editor's driver, release the editor, then `just sync-firmware` and review the diff.
- `pxt.json` follows the editor: `wuKong` at the version it bundles (v1.6.0), no `radio`, and the
  *No Pairing Required* yotta config.
- Build with `just firmware` (Docker) or `sh firmware/build.sh` (Node.js).

## Licences and docs

- Licences: builder MIT, models CC BY-SA 4.0, custom part files CC BY 4.0 (their header line). Keep
  the credits in `README.md` and `models/LICENSE.md`.
- Release: tag `vX.Y.Z` on `main` and push the tag; the `release` job attaches the files.
- Docs: keep `README.md`, `docs/USER_DOC.md`, `docs/TECHNICAL_DOC.md` and `docs/USER_STORIES.md` in
  step with any change.
