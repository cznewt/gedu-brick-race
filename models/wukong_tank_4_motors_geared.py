"""Wukong tank with four servos, geared 2:1: our design, the four-servo Wukong tank
(wukong_tank_4_motors.py: the Wukong mecanum racer of the ElecFreaks Wonder Rugged Kit on tracks
from the Building:bit kit) with each servo geared up 2:1. The racer's body, servos and underside
stay as its booklet builds them (steps 1-24), but for the outer lugs' lower pins and the two
9-beams under the car's ends: the lug's lower hole crosses its vertical one, so the axle needs that
pin's place (the servos still hang on the rails' end pins and the inner lugs' pins). A 16-tooth gear on each servo's output turns an
8-tooth gear on a 6L axle that runs free in the lower round hole of the servo's outer lug (a half
bush inside the lug and a bush outside hold it), and the sprocket sits on that axle: the tracks
run twice as fast as the servos turn, with half the pull. The hole is 30 LDU along and 10 below
the output, so the gears' axles are sqrt(30^2 + 10^2) = 31.6 LDU apart, 1.6 LDU (0.65 mm) more
than LEGO's 30 for 16 and 8 teeth: the teeth mesh 2.5 LDU deep instead of 4.1. The sprockets sit
18 LDU further out than the four-servo tank's (hub at 156, past the 8-tooth gear and a half
bush), where their rims clear the 16-tooth gears; 31 links make each track as round as that
tank's 27. World: front = +X, left = +Z, Y points down."""
import numpy as np

import ldr
import wukong_mecanum as racer
from ldr import R
from tracks import Track
from wonder_common import DBG, LBG

ACROSS = R(("y", 90))                                       # axle along Z
OUT_X, OUT_Y = racer.SERVO_X + 10, racer.SERVO_Y            # the outputs sit 10 off the servos' centres
LUG_X, LUG_Y = racer.SERVO_X + 40, racer.SERVO_Y + 10       # the outer lug's lower round hole along Z
OUTPUTS = ((-OUT_X, OUT_Y), (OUT_X, OUT_Y))                 # back, front
WHEELS = ((-LUG_X, LUG_Y), (LUG_X, LUG_Y))                  # back, front: the sprockets on the lug axles
GEAR_Z = racer.RAIL_Z + 46                                  # the gears' middle, the 16-tooth one against the servo (z = 116)
WHEEL_Z = GEAR_Z + 30                                       # sprocket hub past the 8-tooth gear and a half bush
# along each lug axle (left side, the right mirrored): a half bush against the lug's inner face
# (z = 68), the lug, a bush against its outer face (z = 92), 4 LDU free, the 8-tooth gear, a half
# bush, the sprocket, a half bush; the 6L axle from z = 57 to 177
INNER_BUSH_Z, BUSH_Z, SPACER_Z, OUTER_BUSH_Z, AXLE_Z = 63, 102, 141, 171, 117
TRACK = Track(WHEELS, 31)
# the racer's cameras for its steps; the gears from the left, low, the sprockets and tracks from
# the front left, the board as the four-servo tank's
VIEW = dict(racer.VIEW, step_views={**racer.VIEW["step_views"], 25: (160, 8), 26: (150, 10), 27: (140, 15),
                                    28: (125, 25), 29: (130, 30), 30: (140, 35)})


def mesh(fx):
    """The gears' turns about Z at the end fx (-1 back, 1 front): a tooth of the 8-tooth gear in a
    gap of the 16-tooth gear on the line between their axles (94925: gaps at 0 degrees and every
    22.5; 10928: teeth at 0 degrees and every 45)."""
    a = np.degrees(np.arctan2(LUG_Y - OUT_Y, fx * (LUG_X - OUT_X)))
    return R(("z", a % 22.5)), R(("z", (a + 180) % 45))


def build():
    m = ldr.Model("wukong-tank-4servo-geared")
    racer.body(m)
    racer.servos(m, outer_pins=False)
    racer.underside(m, outer_beams=False)
    # 25: a 16-tooth gear pushed all the way onto each servo's output
    for x, y in OUTPUTS:
        for s in (1, -1):
            m.add("94925.dat", LBG, (x, y, GEAR_Z * s), mesh(np.sign(x))[0])
    m.step()
    # 26: (x4) a 6L axle through the lower round hole of the servo's outer lug, a half bush on it
    #     inside the lug, a bush outside; the 8-tooth gear in the 16-tooth gear's teeth, a half bush
    for x, y in WHEELS:
        turn = mesh(np.sign(x))[1]                          # the axle's cross as the 8-tooth gear's hole
        for s in (1, -1):
            m.add("3706.dat", LBG, (x, y, AXLE_Z * s), turn @ ACROSS)
            m.add("4265c.dat", LBG, (x, y, INNER_BUSH_Z * s), turn)
            m.add("3713.dat", LBG, (x, y, BUSH_Z * s), turn)
            m.add("10928.dat", DBG, (x, y, GEAR_Z * s), turn)
            m.add("4265c.dat", LBG, (x, y, SPACER_Z * s), turn)
    m.step()
    # 27: a sprocket on each lug axle, a half bush outside it
    for x, y in WHEELS:
        for s in (1, -1):
            m.add("57519.dat", DBG, (x, y, WHEEL_Z * s), TRACK.sprocket_turn((x, y)))
            m.add("4265c.dat", LBG, (x, y, OUTER_BUSH_Z * s), mesh(np.sign(x))[1])
    m.step()
    # 28: (x2) 31 links to a track, round each side's two sprockets
    for s in (1, -1):
        TRACK.links(m, DBG, WHEEL_Z * s)
    m.step()
    racer.board(m)
    return m
