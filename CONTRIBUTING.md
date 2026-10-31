# Contributing a car

The Brick Race is open to your own designs. A car gets a page on
[brick-race.geekedu.eu](https://brick-race.geekedu.eu/en/models/) and a folder here, first with
your photos, then, once we have drawn it, with the same files as the Wukong cars: a booklet,
a BrickLink Studio model, a parts list and a wanted list.

## Register your car

Either way works; both end in this repository.

1. **On the site:** the form at [brick-race.geekedu.eu/en/your-car/](https://brick-race.geekedu.eu/en/your-car/)
   (Czech: [/vase-auto/](https://brick-race.geekedu.eu/vase-auto/)). Send the photos to the address
   it gives you, or put a link to them in the form.
2. **On GitHub:** open an issue with the *Register a car* template; drop the photos straight into
   it.

## What we need

- **Photos**, straight on, with nothing in the way: from the top, from the bottom, from the
  front, from one side, and one from the front left like a catalogue picture. More if a part
  hides another. A phone camera is fine; daylight helps.
- **The parts**: which kit or kits they come from (Wonder Building Kit, Building:bit, the
  Rugged Kit, your own LEGO Technic), and any part that is not in them.
- **The board and motors**: Wukong, Building:bit or another; which motors or servos, on which
  ports.
- **The driver** you flash from [makecode-microbit.geekedu.eu](https://makecode-microbit.geekedu.eu/)
  and any setting you changed (a wheel's SLIDE, DIRECTION).
- **Your name** as it should appear, or a nickname.

## What happens then

We draw the car as an LDraw model in `models/` (a Python script like the Wukong cars'), check it
against your photos and send you the renders to confirm, then build the booklet and release it.
Your folder `models/users/<slug>/` keeps the photos and a README; the model's `.json` names you.

## Licence

Models and booklets in this repository are published under
[CC BY-SA 4.0](models/LICENSE.md): by registering a car you agree that its model and pictures
are shared that way, with your name on them. The code stays MIT.
