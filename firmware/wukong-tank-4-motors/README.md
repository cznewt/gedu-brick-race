# wukong-tank-4-motors firmware

The Bluetooth driver for the Wukong tank with four motors. Drive it from the
[phone joystick](https://makecode-microbit.geekedu.eu/joystick/):
- up and down drive;
- up and sideways curves;
- sideways alone spins on the spot.

- **Ports:** Geekservo 360° servos on S0 left front, S1 left rear, S2 right front, S3 right rear, as on
  the mecanum racer.
- **Settings** at the top of `main.ts`:
  - `LEFT_FRONT`, `LEFT_REAR`, `RIGHT_FRONT`, `RIGHT_REAR`: 1 for a servo with its output outwards,
    -1 for one mounted the other way round;
  - `SPEED`, `SLOW`, `TEST`, `CURVE`.
- **Motor test:** lift the tank and tap *Test motors* on the phone: 1 left front, 2 right front,
  3 left rear, 4 right rear, each forward, then back.
- No pairing needed. It stops by itself when the phone goes quiet for 1.5 s.

In the GeekEdu editor: [Wukong Tank, 4 Servos (Bluetooth)](https://makecode-microbit.geekedu.eu/#example:/projects/geekedu-wukong-tank-4servo-bluetooth)
