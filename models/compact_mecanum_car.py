"""Compact mecanum car, a users' model by Aleš Komárek, drawn from his photos (third reading,
2026-11-05, with the builder's two corrections: the blue pins point up, the board's base sits
down on the frame). Four Geekservo 360 servos at the corners, outputs outwards, the 60 mm
mecanum wheels straight on them, no gears; the servos' inner lugs six studs apart. Four layers
of beams: at the bottom a yellow 9-beam a side pinned up into the inner lugs; at the servos'
upper half a white 5-beam a side, exactly between the inner lugs, and a lime 7-beam across each
end: two studs in front of the front lugs, one stud behind the back ones; on top, along each
side from the front, the kit's blue L piece (its cross hole inboard, its second hole pointing
in), a lime 5-beam, the kit's yellow 1 x 4 and a yellow 5-beam; and across, on top of those, a
white 7-beam at the front on the L pieces, a yellow 7-beam over the front inner lugs and the
yellow 7-beam of the back U. The lime end beams' blue pins point up: at the front into the L
pieces' first holes, at the back through the yellow 5-beams into the U's cross beam, which lies
directly over the back end beam (its middle pins reach it too); the front end beam's middle pins
hang below it. The Wukong board stands across the car's middle on the side beams, pinned down
through its base's edge holes, the micro:bit lying flat towards the front; a grey 3 x 5
L-liftarm screwed to the board's right corner. Driven by the racer's driver, DIRECTION 1.
World: front = +X (the micro:bit's end), left = +Z, Y points down; the top layer of beams is at
y = 0, the lug line at z = +-60, the car centred on x = 0."""
import numpy as np

import ldr
from ldr import R
from wonder_common import BLACK, BLUE, LBG, PIN_DOWN, TAN, WHITE, YELLOW, microbit
from wukong_mecanum import FLAT_X, LIME, frame, servo

SX, SY, SZ = 100, 30, 60                                    # servo centres; lugs at x = +-60 and +-140, 16 mm tall (y 10..50)
TOP, UPPER, BOTTOM, OVER = 0, 20, 60, -20                   # the beam layers' centres; the lower servo half (y 40) holds no beam
FRONT_END, BACK_END = 180, -160                             # the lime end beams: two studs before the front lugs, one behind the back ones
WHEEL_Z = 145                                               # the wheel's hub on the output past the servo's face (z = 96)
WHEEL = {(1, 1): "geekedu-mecanum-wheel-60-left.dat", (-1, -1): "geekedu-mecanum-wheel-60-left.dat",
         (1, -1): "geekedu-mecanum-wheel-60-right.dat", (-1, 1): "geekedu-mecanum-wheel-60-right.dat"}
L_RIGHT = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])     # the kit's L piece along X, cross hole backwards, second hole inboard
L_LEFT = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])    # the same piece turned over for the left side
UPRIGHT = frame((0, -1, 0), (-1, 0, 0))                    # the Wukong on its base's 7-stud edge, slot up, components forwards
GREY_L = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])        # 32526: the corner up, the 5-hole arm down, the 3-hole arm inboard, holes along X
VIEW = dict(az=130, el=30, cover_az=130, cover_el=30,
            step_views={1: (130, 35), 2: (130, 30), 3: (130, 35), 4: (130, 35), 5: (60, 35), 6: (130, 40),
                        7: (140, 25), 8: (130, 30)})


def bottom(m):
    """Step 1: (x2) a yellow 9-beam a side, a pin up in its second and eighth hole: the servos' inner
    lugs stand on them, the beam one stud past each."""
    for s in (-1, 1):
        m.add("40490.dat", YELLOW, (0, BOTTOM, s * SZ), FLAT_X)
        for x in (60, -60):
            m.add("2780.dat", BLACK, (x, BOTTOM - 10, s * SZ), PIN_DOWN)
    m.step()


def servos(m):
    """Step 2: the four servos on those pins, outputs outwards, the outputs' offsets towards the ends."""
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add("geekedu-ef-geekservo-360.dat", LIME, (fx * SX, SY, side * SZ), servo(fx, side))
    m.step()


def middle_and_ends(m):
    """Step 3: (x2) a white 5-beam a side between the inner lugs at the servos' upper half (the
    pins of step 4 hold it); a lime 7-beam across each end at the same height: blue pins up in
    its end holes; at the front five black pins hanging from its middle holes, at the back three
    black 3L pins up from its middle holes (the U's cross beam of step 6 sits on them)."""
    for s in (-1, 1):
        m.add("32316.dat", WHITE, (0, UPPER, s * SZ), FLAT_X)
    m.add("32524.dat", LIME, (FRONT_END, UPPER, 0))
    m.add("32524.dat", LIME, (BACK_END, UPPER, 0))
    for s in (-1, 1):
        m.add("2780.dat", BLUE, (FRONT_END, UPPER - 10, s * SZ), PIN_DOWN)
        m.add("6558.dat", BLUE, (BACK_END, UPPER - 20, s * SZ), PIN_DOWN)
    for z in (-40, -20, 0, 20, 40):
        m.add("2780.dat", BLACK, (FRONT_END, UPPER + 10, z), PIN_DOWN)
    for z in (-20, 0, 20):
        m.add("6558.dat", BLACK, (BACK_END, UPPER - 20, z), PIN_DOWN)
    m.step()


def side_beams(m):
    """Step 4: (x2) the top layer along each side, back to front: a yellow 5-beam over the back
    servo (its last hole on the end beam's blue pin; a black pin down in its first hole), the
    kit's yellow 1 x 4 (black pin down into the inner lug from its last hole, tan 3L pins down
    into the white beam from its middle ones; its first hole waits for the board), a lime 5-beam
    (a black pin and a tan 3L pin down into the white beam from its last two holes; its middle
    hole waits for the across beam)."""
    for s in (-1, 1):
        m.add("32316.dat", YELLOW, (-120, TOP, s * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (-80, TOP + 10, s * SZ), PIN_DOWN)
        m.add("geekedu-beam-1x4.dat", YELLOW, (-30, TOP, s * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (-60, TOP + 10, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (-40, TOP + 20, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (-20, TOP + 20, s * SZ), PIN_DOWN)
        m.add("32316.dat", LIME, (60, TOP, s * SZ), FLAT_X)
        m.add("2780.dat", BLACK, (20, TOP + 10, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (40, TOP + 20, s * SZ), PIN_DOWN)
    m.step()


def front_pieces(m):
    """Step 5: (x2) the kit's blue L piece at each front corner: its first hole on the end beam's
    blue pin, its second hole pointing in, its cross hole backwards; a black pin down through its
    third hole into the front outer lug."""
    for s, rot in ((-1, L_RIGHT), (1, L_LEFT)):
        m.add("geekedu-beam-L-2x4-axle.dat", BLUE, (150, TOP, s * SZ), rot)
        m.add("2780.dat", BLACK, (140, TOP + 10, s * SZ), PIN_DOWN)
    m.step()


def across_beams(m):
    """Step 6: three 7-beams across on top: white at the front on the L pieces' second holes
    (black pins), yellow over the front inner lugs (tan 3L pins through the lime beams into the
    lugs), and the yellow cross beam of the back U on the back end beam's pins (blue 3L pins
    through the yellow 5-beams' last holes)."""
    m.add("32524.dat", WHITE, (160, OVER, 0))
    m.add("32524.dat", YELLOW, (60, OVER, 0))
    m.add("32524.dat", YELLOW, (BACK_END, OVER, 0))
    for s in (-1, 1):
        m.add("2780.dat", BLACK, (160, OVER + 10, s * SZ), PIN_DOWN)
        m.add("32556.dat", TAN, (60, TOP, s * SZ), PIN_DOWN)
    m.step()


def board(m):
    """Step 7: the Wukong board standing across the car's middle on the side beams, slot up, its
    micro:bit lying flat towards the front: blue 3L pins up through the white beams and the yellow
    1 x 4 beams' first holes into the base's edge holes. A grey 3 x 5 L-liftarm screwed to the
    board's right corner, its long arm down the edge, its short arm along the top."""
    pos = (0, -60, 0)
    for s in (-1, 1):
        m.add("6558.dat", BLUE, (0, TOP, s * SZ), PIN_DOWN)
    m.add("geekedu-ef-wukong-board.dat", LBG, pos, UPRIGHT)
    microbit(m, pos, UPRIGHT)
    m.add("32526.dat", LBG, (0, -120, -80), GREY_L)
    m.step()


def wheels(m):
    """Step 8: the mecanum wheels straight on the outputs, left-hand ones at front left and back
    right."""
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add(WHEEL[(fx, side)], BLACK, (fx * (SX + 10), SY, side * WHEEL_Z))
    m.step()


def build():
    m = ldr.Model("compact-mecanum-car")
    bottom(m)
    servos(m)
    middle_and_ends(m)
    side_beams(m)
    front_pieces(m)
    across_beams(m)
    board(m)
    wheels(m)
    return m
