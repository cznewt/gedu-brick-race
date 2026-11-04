"""Compact mecanum car, a users' model by Aleš Komárek (2026-11-03, drawn from his photos):
four Geekservo 360 servos at the corners, outputs outwards, the 60 mm mecanum wheels straight on
them, no gears. The frame hangs on the servos' lugs, which lie on one line six studs apart: on
top, a lime 7-beam across each pair of outer lugs and a yellow 11-beam along each side on the
inner lugs; under the 11-beams, between the servos, a white 7-beam a side and a yellow 7-beam
across at the back third; under the servos, a lime 5-beam under each rear one with a white
7-beam across the back below them, and the yellow U under the front ones: two 9-beams and a
7-beam across the front below them, blue 3L pins at the corners. The Wukong board stands up
across the car's middle, its base down between the white beams, the micro:bit lying on top
pointing forward; a grey 5-beam screwed to its edge holds it (the builder's word, 2026-11-04). Driven by the racer's driver, DIRECTION 1. World: front = +X, left = +Z, Y points
down; the lug line at z = 60, the servos' centres at x = 140."""
import numpy as np

import ldr
from ldr import R
from wonder_common import BLACK, BLUE, LBG, PIN_DOWN, YELLOW, microbit
from wukong_mecanum import FLAT_X, LIME, frame, servo

WHITE = 15
SX, SY, SZ = 140, 50, 60                                   # servo centres; lugs at x = 100 and 180, their holes y 30..70
WHEEL_Z = 140                                              # the wheel's hub on the output past the servo's face (z = 96)
UPRIGHT = frame((0, -1, 0), (-1, 0, 0))                   # the board's base across the car, slot edge up, components forwards
BEAM_UP = R(("z", 90))                                    # a beam standing along Y, holes along X
WHEEL = {(1, 1): "geekedu-mecanum-wheel-60-left.dat", (-1, -1): "geekedu-mecanum-wheel-60-left.dat",
         (1, -1): "geekedu-mecanum-wheel-60-right.dat", (-1, 1): "geekedu-mecanum-wheel-60-right.dat"}
VIEW = dict(az=130, el=30, cover_az=130, cover_el=30,
            step_views={1: (130, 30), 2: (130, 35), 3: (130, 35), 4: (120, 40), 5: (150, 45), 6: (160, -40),
                        7: (60, -40), 8: (230, 25), 9: (130, 30)})


def servos(m):
    """Step 1: the four servos, outputs outwards."""
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add("geekedu-ef-geekservo-360.dat", LIME, (fx * SX, SY, side * SZ), servo(fx, side))
    m.step()


def top(m):
    """Steps 2-3: the beams on the lugs."""
    # 2: a lime 7-beam across each end on the outer lugs, a pin down into each lug's upper half
    for fx in (-1, 1):
        m.add("32524.dat", LIME, (fx * 180, 20, 0))
        for side in (-1, 1):
            m.add("2780.dat", BLACK, (fx * 180, 30, side * SZ), PIN_DOWN)
    m.step()
    # 3: a yellow 11-beam along each side on the inner lugs, pins down into them
    for side in (-1, 1):
        m.add("32525.dat", YELLOW, (0, 20, side * SZ), FLAT_X)
        for fx in (-1, 1):
            m.add("2780.dat", BLACK, (fx * 100, 30, side * SZ), PIN_DOWN)
    m.step()


def middle(m):
    """Steps 4-5: the beams between the servos."""
    # 4: a white 7-beam under each 11-beam between the servos, two pins down through both
    for side in (-1, 1):
        m.add("32524.dat", WHITE, (0, 40, side * SZ), FLAT_X)
        for x in (-60, 60):
            m.add("2780.dat", BLACK, (x, 30, side * SZ), PIN_DOWN)
    m.step()
    # 5: a yellow 7-beam across under the white beams' back ends, a pin down into each
    m.add("32524.dat", YELLOW, (-60, 60, 0))
    for side in (-1, 1):
        m.add("2780.dat", BLACK, (-60, 50, side * SZ), PIN_DOWN)
    m.step()


def underside(m):
    """Steps 6-7: the car turned over."""
    # 6: a lime 5-beam under each rear servo on both its lugs, a pin up into the inner one; the
    #    white 7-beam across the back under them; a blue 3L pin up through it, the 5-beam and
    #    the outer lug
    for side in (-1, 1):
        m.add("32316.dat", LIME, (-140, 80, side * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (-100, 70, side * SZ), PIN_DOWN)
    m.add("32524.dat", WHITE, (-180, 100, 0))
    for side in (-1, 1):
        m.add("6558.dat", BLUE, (-180, 80, side * SZ), PIN_DOWN)
    m.step()
    # 7: the yellow U under the front: a 9-beam under each front servo from the front lug back
    #    to the car's middle, a pin up into the inner lug; the 7-beam across the front below
    #    them; blue 3L pins up through the corners and the outer lugs
    for side in (-1, 1):
        m.add("40490.dat", YELLOW, (100, 80, side * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (100, 70, side * SZ), PIN_DOWN)
    m.add("32524.dat", YELLOW, (180, 100, 0))
    for side in (-1, 1):
        m.add("6558.dat", BLUE, (180, 80, side * SZ), PIN_DOWN)
    m.step()


def board(m):
    """Step 8: the Wukong board standing up across the car's middle, its base down between the
    white beams, the micro:bit lying on top pointing forward, display up; a grey 5-beam screwed
    to the board's left edge stands on the white beam (the builder's mount: screws, no pin)."""
    pos = (-20, 20, 0)
    m.add("geekedu-ef-wukong-board.dat", LBG, pos, UPRIGHT)
    microbit(m, pos, UPRIGHT)
    m.add("32316.dat", LBG, (-20, -20, 60), BEAM_UP)
    m.step()


def wheels(m):
    """Step 9: the mecanum wheels straight on the outputs, left-hand ones at front left and back
    right."""
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add(WHEEL[(fx, side)], BLACK, (fx * (SX + 10), SY, side * WHEEL_Z))
    m.step()


def build():
    m = ldr.Model("compact-mecanum-car")
    servos(m)
    top(m)
    middle(m)
    underside(m)
    board(m)
    wheels(m)
    return m
