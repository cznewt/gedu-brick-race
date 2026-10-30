"""Wukong tank with four servos, geared 2:1: our design, the four-servo Wukong tank
(wukong_tank_4_motors.py: the Wukong mecanum racer of the ElecFreaks Wonder Rugged Kit on tracks
from the Building:bit kit) with each servo geared up 2:1. The racer's body, servos and underside
stay as its booklet builds them (steps 1-24), but for the two 9-beams under the car's ends, which
become a 7-beam per side on the same lug pins, reaching four holes further out, the two of an end
tied into one piece by a 5-beam across their inner ends (on one pin a beam cannot turn). A pin with
pin hole stands in each 7-beam's outer hole, its ring the bearing of a 7L axle along the servo's axis:
a 16-tooth gear on the servo's output turns the 8-tooth gear on that axle, and the sprocket sits
on the axle past the ring, so the tracks run twice as fast as the servos turn, with half the pull.
The ring is 30 LDU along and 10 below the output, so the gears' axles are sqrt(30^2 + 10^2) =
31.6 LDU apart, 1.6 LDU (0.65 mm) more than LEGO's 30 for 16 and 8 teeth: the teeth mesh 2.5 LDU
deep instead of 4.1. The Geekservo's lugs have one pin hole each, across the servo (the mounting
pins' one), so nothing can hold an axle in them; and the Building:bit links are 5 studs wide, so
the tracks start outboard of the gears: the sprocket hubs sit at 198, the car is 19.6 cm wide over
the tracks (the racer 15.4). 31 links make each track as round as the four-servo tank's 27.
World: front = +X, left = +Z, Y points down."""
import numpy as np

import ldr
import wukong_mecanum as racer
from ldr import R
from tracks import Track
from wonder_common import BLACK, DBG, LBG, PIN_DOWN

ACROSS = R(("y", 90))                                       # axle along Z
OUT_X, OUT_Y = racer.SERVO_X + 10, racer.SERVO_Y            # the outputs sit 10 off the servos' centres
RING_X, RING_Y = racer.SERVO_X + 40, racer.SERVO_Y + 10     # the pin with pin hole on the 7-beam's outer hole
OUTPUTS = ((-OUT_X, OUT_Y), (OUT_X, OUT_Y))                 # back, front
WHEELS = ((-RING_X, RING_Y), (RING_X, RING_Y))              # back, front: the sprockets on the ring axles
BEAM_Z = racer.RAIL_Z + 20                                  # the 7-beams' middles: holes from 40 to 160, the lug pin in 80
TIE_Z = racer.RAIL_Z - 40                                   # the 7-beams' innermost holes (z = 40): the 5-beam's end pins
RING_Z = racer.RAIL_Z + 80                                  # the 7-beams' outer holes (z = 160)
GEAR_Z = racer.RAIL_Z + 46                                  # the gears' middle, the 16-tooth one against the servo (z = 126)
WHEEL_Z = 198                                               # sprocket hub past the ring and a half bush; the links start at 150
# along each ring axle (left side, the right mirrored): a bush clear of the lug (96..116), the
# 8-tooth gear (116..136), a half bush, 5 free, the ring (151..169), a half bush, the sprocket,
# a half bush; the 7L axle from z = 96 to 236
BUSH_Z, SPACER_Z, OUTER_SPACER_Z, OUTER_BUSH_Z, AXLE_Z = 106, 141, 174, 221.5, 166
TRACK = Track(WHEELS, 31)
# the racer's cameras for its steps; the beams and rings from the front left, low, the gears from
# the left, the sprockets and tracks from the front left, the board as the four-servo tank's
VIEW = dict(racer.VIEW, step_views={**racer.VIEW["step_views"], 25: (150, 12), 26: (150, 12), 27: (160, 8), 28: (150, 10),
                                    29: (135, 20), 30: (130, 30), 31: (140, 35), 32: (140, 35)})


def mesh(fx):
    """The gears' turns about Z at the end fx (-1 back, 1 front): a tooth of the 8-tooth gear in a
    gap of the 16-tooth gear on the line between their axles (94925: gaps at 0 degrees and every
    22.5; 10928: teeth at 0 degrees and every 45)."""
    a = np.degrees(np.arctan2(RING_Y - OUT_Y, fx * (RING_X - OUT_X)))
    return R(("z", a % 22.5)), R(("z", (a + 180) % 45))


def build():
    m = ldr.Model("wukong-tank-4servo-geared")
    racer.body(m)
    racer.servos(m)
    racer.underside(m, outer_beams=False)
    # 25: (x4) a 7-beam under each end of the car on the outer lug's pin, its outer end past the
    #     servo; a pin up in its innermost hole, a pin with pin hole down in its outer hole, the hole
    #     along the car's axles
    for fx in (-1, 1):
        for s in (1, -1):
            m.add("32524.dat", racer.LIME, (fx * RING_X, 80, BEAM_Z * s))
            m.add("2780.dat", BLACK, (fx * RING_X, 70, TIE_Z * s), PIN_DOWN)
            m.add("15100.dat", BLACK, (fx * RING_X, RING_Y, RING_Z * s), racer.PIN_HOLE_ON_Z_DOWN)
    m.step()
    # 26: (x2) a 5-beam across the two 7-beams' inner ends, on those pins
    for fx in (-1, 1):
        m.add("32316.dat", racer.LIME, (fx * RING_X, 60, 0))
    m.step()
    # 27: a 16-tooth gear pushed all the way onto each servo's output
    for x, y in OUTPUTS:
        for s in (1, -1):
            m.add("94925.dat", LBG, (x, y, GEAR_Z * s), mesh(np.sign(x))[0])
    m.step()
    # 28: (x4) a 7L axle through the ring: inside it a half bush against the ring, the 8-tooth gear
    #     in the 16-tooth gear's teeth and a bush; outside it a half bush
    for x, y in WHEELS:
        turn = mesh(np.sign(x))[1]                          # the axle's cross as the 8-tooth gear's hole
        for s in (1, -1):
            m.add("44294.dat", LBG, (x, y, AXLE_Z * s), turn @ ACROSS)
            m.add("3713.dat", LBG, (x, y, BUSH_Z * s), turn)
            m.add("10928.dat", DBG, (x, y, GEAR_Z * s), turn)
            m.add("4265c.dat", LBG, (x, y, SPACER_Z * s), turn)
            m.add("4265c.dat", LBG, (x, y, OUTER_SPACER_Z * s), turn)
    m.step()
    # 29: a sprocket on each axle against the half bush, a half bush outside it
    for x, y in WHEELS:
        for s in (1, -1):
            m.add("57519.dat", DBG, (x, y, WHEEL_Z * s), TRACK.sprocket_turn((x, y)))
            m.add("4265c.dat", LBG, (x, y, OUTER_BUSH_Z * s), mesh(np.sign(x))[1])
    m.step()
    # 30: (x2) 31 links to a track, round each side's two sprockets
    for s in (1, -1):
        TRACK.links(m, DBG, WHEEL_Z * s)
    m.step()
    racer.board(m)
    return m
