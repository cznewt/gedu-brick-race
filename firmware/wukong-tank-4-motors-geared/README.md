# wukong-tank-4-motors-geared firmware

The Bluetooth driver for the Wukong tank with four motors, geared 2:1. It is the four-motor tank's
driver with `LEFT_FRONT`, `LEFT_REAR`, `RIGHT_FRONT` and `RIGHT_REAR` at -1: each servo turns its
track through a 16-tooth and an 8-tooth gear, and a pair of gears turns the track the other way
round. Drive it from the [phone joystick](https://makecode-microbit.geekedu.eu/joystick/), the same
way as the four-motor tank:
- up and down drive;
- up and sideways curves;
- sideways alone spins on the spot.

- **Ports:** Geekservo 360° servos on S0 left front, S1 left rear, S2 right front, S3 right rear.
- **Settings** at the top of `main.ts`:
  - `LEFT_FRONT`, `LEFT_REAR`, `RIGHT_FRONT`, `RIGHT_REAR`: -1 here;
  - `SPEED`, `SLOW`, `TEST`, `CURVE`.
- **Motor test:** lift the tank and tap *Test motors* on the phone: 1 left front, 2 right front,
  3 left rear, 4 right rear, each forward, then back. A track that runs back first: that servo's
  setting to 1.
- The joystick names it as the four-servo tank: it is the same driver. No pairing needed. It stops
  by itself when the phone goes quiet for 1.5 s.

In the GeekEdu editor it is [Wukong Tank, 4 Servos (Bluetooth)](https://makecode-microbit.geekedu.eu/#example:/projects/geekedu-wukong-tank-4servo-bluetooth)
with the four settings changed to -1.
