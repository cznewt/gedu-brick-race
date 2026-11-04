"""Compact mecanum car, a users' model by Aleš Komárek, drawn from his photos (2026-11-04, the
second reading: the first had the car upside down). Four Geekservo 360 servos at the corners on
one lug line, outputs outwards, the 60 mm mecanum wheels straight on them, no gears. Four
layers of beams: at the bottom a yellow 9-beam a side on the inner lugs; at the servos' height
a white 5-beam a side between the servos and a lime 7-beam across each end beside the outer
lugs; on top, along each side, the kit's blue 1 x 4 beam with an axle hole (on the front outer
lug), a lime 5-beam (on the front inner lug), the kit's yellow 1 x 4 and a yellow 5-beam (on
the back lugs); and across, on top of those, a white 7-beam at the front, a yellow 7-beam over
the front inner lugs and the yellow 7-beam of the back U. Black pins are 2L, tan ones 3L
(through two beams into a lug or down into the white beams), blue ones 3L. The Wukong board
stands across the car's middle on the side beams, its micro:bit lying flat towards the front,
a grey 7-beam screwed up its right edge. Driven by the racer's driver, DIRECTION 1. World:
front = +X (the micro:bit's end), left = +Z, Y points down; the top layer of beams is at y = 0,
the lug line at z = +-60."""
import numpy as np

import ldr
from ldr import R
from wonder_common import BLACK, BLUE, LBG, PIN_DOWN, TAN, WHITE, YELLOW, microbit
from wukong_mecanum import FLAT_X, LIME, frame, servo

SX, SY, SZ = 110, 30, 60                                    # servo centres; lugs at x = +-70 and +-150, 16 mm tall (y 10..50)
TOP, UPPER, LOWER, BOTTOM = 0, 20, 40, 60                   # the beam layers' centres: on top, the servos' upper and lower halves, under them
OVER = -20                                                  # the across beams on top of the side beams
WHEEL_Z = 145                                               # the wheel's hub on the output past the servo's face (z = 96)
AXLE_END_IN = R(("y", -90))                                 # the blue beam along X with its axle hole towards the car's middle
WHEEL = {(1, 1): "geekedu-mecanum-wheel-60-left.dat", (-1, -1): "geekedu-mecanum-wheel-60-left.dat",
         (1, -1): "geekedu-mecanum-wheel-60-right.dat", (-1, 1): "geekedu-mecanum-wheel-60-right.dat"}
UPRIGHT = frame((0, -1, 0), (-1, 0, 0))                    # the Wukong on its base's 7-stud edge, slot up, the micro:bit forwards
STANDING = frame((0, 0, -1), (1, 0, 0))                    # a beam standing along Y, holes along X
VIEW = dict(az=130, el=30, cover_az=130, cover_el=30,
            step_views={1: (130, 35), 2: (130, 30), 3: (130, 30), 4: (130, 35), 5: (130, 40), 6: (60, 35),
                        7: (130, 40), 8: (140, 25), 9: (130, 30)})


def bottom(m):
    """Step 1: (x2) a yellow 9-beam a side, a pin up in its first and eighth hole: the servos' inner
    lugs stand on them, one stud of beam past the back ones."""
    for s in (-1, 1):
        m.add("40490.dat", YELLOW, (-10, BOTTOM, s * SZ), FLAT_X)
        for x in (70, -70):
            m.add("2780.dat", BLACK, (x, BOTTOM - 10, s * SZ), PIN_DOWN)
    m.step()


def servos(m):
    """Step 2: the four servos on those pins, outputs outwards, the outputs' offsets towards the ends."""
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add("geekedu-ef-geekservo-360.dat", LIME, (fx * SX, SY, side * SZ), servo(fx, side))
    m.step()


def end_beams(m):
    """Step 3: (x2) a lime 7-beam across each end beside the outer lugs, at the servos' upper half: a
    blue 3L pin down through each end hole to the car's floor, black pins up from the middle
    holes (three at the front, five at the back) that the across beams of step 7 rest on."""
    for fx, middles in ((1, (-20, 0, 20)), (-1, (-40, -20, 0, 20, 40))):
        m.add("32524.dat", LIME, (fx * 170, UPPER, 0))
        for s in (-1, 1):
            m.add("6558.dat", BLUE, (fx * 170, UPPER + 20, s * SZ), PIN_DOWN)
        for z in middles:
            m.add("2780.dat", BLACK, (fx * 170, UPPER - 10, z), PIN_DOWN)
    m.step()


def middle_beams(m):
    """Step 4: (x2) a white 5-beam a side between the servos at their upper half, under the fifth
    to ninth hole of the bottom beam; the pins of step 5 hold it."""
    for s in (-1, 1):
        m.add("32316.dat", WHITE, (-10, UPPER, s * SZ), FLAT_X)
    m.step()


def side_beams(m):
    """Step 5: (x2) the top layer along each side, back to front: a yellow 5-beam on the back
    servo's lugs (a pin down into the inner one, the outer one waits for step 7), the kit's
    yellow 1 x 4 (pins down into the white beam: black in its second and fourth hole, tan in the
    third), a lime 5-beam (a tan pin down through its last hole into the white beam, another
    hanging from the fourth, a black pin up in the second; its third hole waits for step 7)."""
    for s in (-1, 1):
        m.add("32316.dat", YELLOW, (-110, TOP, s * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (-70, TOP + 10, s * SZ), PIN_DOWN)
        m.add("geekedu-beam-1x4.dat", YELLOW, (-20, TOP, s * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (-10, TOP + 10, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (-30, TOP + 20, s * SZ), PIN_DOWN)
        m.add("2780.dat", BLACK, (-50, TOP + 10, s * SZ), PIN_DOWN)
        m.add("32316.dat", LIME, (70, TOP, s * SZ), FLAT_X)
        m.add("32556.dat", TAN, (30, TOP + 20, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (50, TOP + 20, s * SZ), PIN_DOWN)
        m.add("2780.dat", BLACK, (90, TOP - 10, s * SZ), PIN_DOWN)
    m.step()


def front_beams(m):
    """Step 6: (x2) the kit's blue 1 x 4 beam with the axle hole in front of the lime beam, the axle
    hole towards the middle: a pin down through its third hole into the front outer lug."""
    for s in (-1, 1):
        m.add("geekedu-beam-1x4-axle.dat", BLUE, (160, TOP, s * SZ), AXLE_END_IN)
        m.add("2780.dat", BLACK, (150, TOP + 10, s * SZ), PIN_DOWN)
    m.step()


def across_beams(m):
    """Step 7: three 7-beams across on top: white at the front on the blue beams' second holes
    (black pins), yellow over the front inner lugs (tan 3L pins through the lime beams into the
    lugs), yellow over the back outer lugs (blue 3L pins through the yellow 5-beams into the
    lugs): the back U."""
    m.add("32524.dat", WHITE, (170, OVER, 0))
    m.add("32524.dat", YELLOW, (70, OVER, 0))
    m.add("32524.dat", YELLOW, (-150, OVER, 0))
    for s in (-1, 1):
        m.add("2780.dat", BLACK, (170, OVER + 10, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (70, TOP, s * SZ), PIN_DOWN)
        m.add("6558.dat", BLUE, (-150, TOP, s * SZ), PIN_DOWN)
    m.step()


def board(m):
    """Step 8: the Wukong board standing across the car on the side beams, just behind the middle,
    slot up, its micro:bit lying flat towards the front; a grey 7-beam screwed up its right edge
    (no pin)."""
    pos = (20, -60, 0)
    m.add("geekedu-ef-wukong-board.dat", LBG, pos, UPRIGHT)
    microbit(m, pos, UPRIGHT)
    m.add("32524.dat", LBG, (44, -80, -60), STANDING)
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
    bottom(m)
    servos(m)
    end_beams(m)
    middle_beams(m)
    side_beams(m)
    front_beams(m)
    across_beams(m)
    board(m)
    wheels(m)
    return m
