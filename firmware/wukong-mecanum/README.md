# wukong-mecanum firmware

The Bluetooth driver for the Wukong mecanum racer. Drive it from the
[phone joystick](https://makecode-microbit.geekedu.eu/joystick/): the first stick drives and turns, the
second slides sideways.

- **Ports:** Geekservo 360° servos on S0 left front, S1 left rear, S2 right front, S3 right rear.
- **Settings** at the top of `main.ts`:
  - `SPEED` (full speed);
  - `SLOW` (speed at the slightest push);
  - `TEST` (speed in the motor test);
  - one `SLIDE` per wheel (`LF_SLIDE`, `RF_SLIDE`, `LR_SLIDE`, `RR_SLIDE`): -1 for a wheel mounted the other way round;
  - `STRAFE_GAIN`.
- **Motor test:** lift the car and tap *Test motors* on the phone.
  - 1 left front, 2 right front, 3 left rear, 4 right rear: each forward, then back.
  - Then 5 forward, 6 slide right, 7 turn right.
  - The car shows each number.
- No pairing needed. It stops by itself when the phone goes quiet for 1.5 s.

In the GeekEdu editor: [Elecfreak Wukong Mecanum Car (Bluetooth)](https://makecode-microbit.geekedu.eu/#example:/projects/elecfreak-wukong-mecanum-car-bluetooth)
