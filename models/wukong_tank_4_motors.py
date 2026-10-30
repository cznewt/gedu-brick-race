"""Wukong tank with four servos: our design, the Wukong mecanum racer (ElecFreaks Wonder Rugged
Kit, wukong_mecanum.py) with tracks instead of its mecanum wheels. The racer's body,
servos and underside stay as its booklet builds them (steps 1-24), so its four Geekservo 360
servos keep their ports (S0 left front, S1 left rear, S2 right front, S3 right rear); a sprocket
goes on each output and a 27-link track round each side's two, from the Building:bit kit.
World: front = +X, left = +Z, Y points down."""
import ldr
import wukong_mecanum as racer
from tracks import Track
from wonder_common import DBG

OUT_X = racer.SERVO_X + 10                                  # the outputs sit 10 off the servos' centres
WHEELS = ((-OUT_X, racer.SERVO_Y), (OUT_X, racer.SERVO_Y))  # back, front
WHEEL_Z = 138                                               # sprocket hub on the output, the track just clear of the rails
TRACK = Track(WHEELS, 27)
# the racer's cameras for its steps; the sprockets and tracks from the front left, the board as
# the racer's
VIEW = dict(racer.VIEW, step_views={**racer.VIEW["step_views"], 25: (125, 20), 26: (125, 25), 27: (130, 30), 28: (140, 35)})


def build():
    m = ldr.Model("wukong-tank-4servo")
    racer.body(m)
    racer.servos(m)
    racer.underside(m)
    # 25: a sprocket pushed all the way onto each servo's output
    for x, y in WHEELS:
        for s in (1, -1):
            m.add("57519.dat", DBG, (x, y, WHEEL_Z * s), TRACK.sprocket_turn((x, y)))
    m.step()
    # 26: (x2) 27 links to a track, round each side's two sprockets
    for s in (1, -1):
        TRACK.links(m, DBG, WHEEL_Z * s)
    m.step()
    racer.board(m)
    return m
