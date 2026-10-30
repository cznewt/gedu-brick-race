"""Wukong tank with two servos: our design on the Wukong mecanum racer's body (ElecFreaks Wonder
Rugged Kit, wukong_mecanum.py, booklet steps 1-21). Only the two back servos stay (plugged
into S0 left and S1 right); where the front ones hung, a 5-beam on each rail's end pins carries a
cross block with a free idler, and the beams under the car go across at the back only. A sprocket
on each servo, one on each idler, a 25-link track from the Building:bit kit round each side.
World: front = +X, left = +Z, Y points down."""
import numpy as np

import ldr
import wukong_mecanum as racer
from ldr import R
from tracks import Track
from wonder_common import DBG, LBG

BLOCK_DOWN = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])    # 48989 along X: pins vertical, end holes along Z
ACROSS = R(("y", 90))                                       # axle along Z
OUT_X = racer.SERVO_X + 10                                  # the outputs sit 10 off the servos' centres
HOLDER_X, BLOCK_Y = 120, 60                                 # the 5-beams on the rails' front end pins; the blocks under them
IDLER = (HOLDER_X - 20, BLOCK_Y)                            # the blocks' back end holes
WHEELS = ((-OUT_X, racer.SERVO_Y), IDLER)                   # back, front
WHEEL_Z = 138                                               # as the four-servo tank's: sprocket hub on the output
TRACK = Track(WHEELS, 25)
# the racer's cameras for its steps; the front holders and idlers from the front below, the
# beams under the car as the racer's, the sprockets and tracks from the front left
VIEW = dict(racer.VIEW, step_views={**racer.VIEW["step_views"], 22: (60, -35), 23: (60, -35), 24: (160, -40),
                                    25: (160, -35), 26: (60, -25), 27: (125, 20), 28: (125, 25), 29: (130, 30),
                                    30: (140, 35)})


def build():
    m = ldr.Model("wukong-tank-2servo")
    racer.body(m)
    # 22: the back servos on the rails' end pins, outputs out; a pin in each lug's other end
    racer.servos(m, ends=(-1,))
    # 23: at the front, a 5-beam on each rail's two end pins, and a cross block under it on its
    #     holes 2 and 4
    for s in (1, -1):
        m.add("32316.dat", racer.LIME, (HOLDER_X, 40, racer.RAIL_Z * s), racer.FLAT_X)
        m.add("48989.dat", racer.BLACK, (HOLDER_X, BLOCK_Y, racer.RAIL_Z * s), BLOCK_DOWN)
    m.step()
    # 24-25: the 15-beams under the middle; 9-beams across on the back servos' lug pins
    racer.underside(m, ends=(-1,))
    # 26: (x2) the idlers' 5L axles through the blocks' back end holes, a half bush inside, a
    #     bush and a half bush outside
    for s in (1, -1):
        m.add("32073.dat", LBG, (IDLER[0], IDLER[1], 110 * s), ACROSS)
        m.add("4265c.dat", LBG, (IDLER[0], IDLER[1], 65 * s))
        m.add("3713.dat", LBG, (IDLER[0], IDLER[1], 100 * s))
        m.add("4265c.dat", LBG, (IDLER[0], IDLER[1], 115 * s))
    m.step()
    # 27: a sprocket pushed all the way onto each servo's output, one on each idler axle
    for x, y in WHEELS:
        for s in (1, -1):
            m.add("57519.dat", DBG, (x, y, WHEEL_Z * s), TRACK.sprocket_turn((x, y)))
    m.step()
    # 28: (x2) 25 links to a track, round each side's sprocket and idler
    for s in (1, -1):
        TRACK.links(m, DBG, WHEEL_Z * s)
    m.step()
    racer.board(m)
    return m
