# wukong-tank-2-motors firmware

The Bluetooth driver for the Wukong tank with two motors. Drive it from the
[phone joystick](https://makecode-microbit.geekedu.eu/joystick/):
- up and down drive;
- up and sideways curves;
- sideways alone spins on the spot.

- **Ports:** Geekservo 360° servos on S0 (left track) and S1 (right track). The right one faces the other
  way, so the program turns it the other way round.
- **Settings** at the top of `main.ts`:
  - `LEFT`, `RIGHT`: 1 for a servo with its output outwards, -1 for one mounted the other way round;
  - `SPEED`, `SLOW`, `TEST`;
  - `CURVE` (the inner track's speed in the sharpest curve).
- **Motor test:** lift the tank and tap *Test motors* on the phone: 1 the left track, 2 the right one,
  each forward, then back.
- No pairing needed. It stops by itself when the phone goes quiet for 1.5 s.

In the GeekEdu editor: [Wukong Tank, 2 Servos (Bluetooth)](https://makecode-microbit.geekedu.eu/#example:/projects/geekedu-wukong-tank-2servo-bluetooth)
