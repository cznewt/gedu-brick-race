"""ElecFreaks Wonder Rugged Kit: the Wukong mecanum racer. Two side rails (a lime 15-beam on
two yellow 5-beams) carry two 9-beams and a 5 x 7 frame; a hood (curved panel, cross blocks,
7-beams, horns) is pinned to the frame's front, and a second frame on top carries the swept
wings and, below them, a back panel. Two bent beams arch from the hood over the sides. The
four green Geekservo 360 servos hang on the rails' end pins, outputs outwards, with lime
beams under them, and turn the four mecanum wheels. The Wukong board sits on the top frame.
The booklet builds the hood (6-10), the wing assembly (11-17), the back panel (18-20) and the
board (29-30) aside; its steps 21-23 and 31 only join them and add no parts, so our steps
21-27 are its 24-30. World: front = +X, left = +Z, Y points down; the lower frame is centred
on the X-Z origin."""
import numpy as np

import ldr
from ldr import R
from wonder_common import BEAM_ON_EDGE, BLACK, BLUE, LBG, PIN_DOWN, YELLOW

LIME, TRANS_RED = 27, 36                                   # horns and round plates: translucent red (callouts, cover photo)
FLAT_X = R(("y", 90))                                      # beam along X, holes vertical
ACROSS = R(("y", 90))                                      # pin along Z
PIN_UP = R(("z", -90))                                     # pin's +X end points up (-Y)
TO_PLUS_Z = R(("y", -90))                                  # axle pin: axle end (+X) towards +Z
TO_MINUS_Z = R(("y", 90))                                  # axle pin: axle end towards -Z
HOOD_PANEL = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]])   # 24119: base holes facing back, dome up and forward
BACK_PANEL = R(("z", -90))                                 # 24119: base holes facing forward, dome up and back
BLOCK_X = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])     # 48989 across, pins along X, side holes vertical
BLOCK_Y = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])    # 48989 across, pins vertical, side holes along X
HORN_FRONT = np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]])   # 41669 on an axle along X, tooth down
HORN_BACK = np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]])     # 41669 on a vertical axle, tooth back
PLATE_BACK = R(("z", 90))                                  # 85861: stud forward into a hole, underside facing back
PLATE_FRONT = R(("z", -90))                                # 85861: stud back into a hole, underside facing forward
PIN_HOLE_ON_Z_DOWN = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])   # 15100: pin hole along Z, pin down
BENT_TILT = 33                                             # the bent beams lean back until their ends rest on the rails
BENT = R(("z", -BENT_TILT)) @ np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])   # 32009: short arm up from its axle end, long arm back
WHEEL = {(1, 1): "geekedu-ef-mecanum-wheel-left.dat", (-1, -1): "geekedu-ef-mecanum-wheel-left.dat",
         (1, -1): "geekedu-ef-mecanum-wheel-right.dat", (-1, 1): "geekedu-ef-mecanum-wheel-right.dat"}
HOOD = np.array([100.0, -40.0, 0.0])                       # the hood panel's origin
BACK = np.array([-100.0, -20.0, 0.0])                      # the back panel's origin
SERVO_X, SERVO_Y, RAIL_Z = 120, 50, 80                     # servo centres (on the rails' end pins)
WHEEL_Z = 140                                              # wheel centres: inner plate just off the rails, servo inside the wheel (booklet 31, photo)
# the booklet's cameras: the rails and the chassis as it shows them; the hood from the front
# (low for 7 and 8, whose parts sit under the panel); the wing assembly and the back panel from
# behind and above (the booklet stacks those parts up along the car); the servos and the beams
# under the car from below (the booklet turns the car over); the wheels from above; the board
# from the front left
VIEW = dict(az=125, el=28, cover_az=130, cover_el=30,
            step_views={1: (330, 20), 2: (150, 20), 3: (65, 35), 4: (65, 35), 5: (65, 30),
                        6: (270, 60), 7: (120, 12), 8: (100, 15), 9: (135, 25), 10: (140, 25),
                        11: (270, 35), 12: (270, 65), 13: (270, 60), 14: (270, 55), 15: (270, 49),
                        16: (90, 46), 17: (305, 15), 18: (270, 30), 19: (270, 30), 20: (270, 35),
                        21: (125, 25), 22: (60, -35), 23: (160, -40), 24: (160, -35), 25: (90, 80),
                        26: (130, 30), 27: (140, 35)})


def frame(x, y):
    """Rotation with local X along x and local Y along y (unit, perpendicular)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    return np.column_stack([x, y, np.cross(x, y)])


def servo(fx, side):
    """Geekservo 360 on a rail: lugs along X, output (local -Y) outwards, output offset (local +X)
    towards the car's end fx."""
    return frame((fx, 0, 0), (0, 0, -side))


# the wing chain: angle connector hubs on the blue 3L pins behind the top frame, upper arm up
# and 22.5 degrees out; a pin with pin hole on an axle pin in it, its pin out; a second one on
# that pin, its pin swept back GAMMA from the arm; the fairing on that pin
GAMMA = np.radians(60)
C22, S22 = np.cos(np.radians(22.5)), np.sin(np.radians(22.5))
ARM = {s: np.array([0, -C22, s * S22]) for s in (-1, 1)}
OUT = {s: np.array([0, S22, s * C22]) for s in (-1, 1)}
SWEPT = {s: np.cos(GAMMA) * ARM[s] + np.sin(GAMMA) * np.array([-1.0, 0, 0]) for s in (-1, 1)}
ANGLE = {s: frame((-s, 0, 0), (0, 0, -s)) for s in (-1, 1)}  # 32016: one arm down, the other along ARM
WING = {1: "64391.dat", -1: "64683.dat"}


def hub(s):
    return np.array([-80.0, -60.0, s * 20])


def pin_hole_1(s):
    return hub(s) + 40 * ARM[s]


def pin_hole_2(s):
    return pin_hole_1(s) + 20 * OUT[s]


def wing_matrix(s):
    """Fairing on the second pin (local Z along it), its root's hole column (local -Y) outwards."""
    q = SWEPT[s]
    out = np.array([0, 0, s * 1.0]) - s * q[2] * q
    y = -out / np.linalg.norm(out)
    return np.column_stack([np.cross(y, q), y, q])


def body(m):
    """Steps 1-21: the rails, the frames, the hood, the wings, the back panel, the bent beams."""
    # 1: four yellow 5-beams: a pin down in the outer end hole, a pin up in the next one, a
    #    blue 3L pin through the inner end hole
    for x in (-120, 120):
        e = 1 if x > 0 else -1
        for z in (-RAIL_Z, RAIL_Z):
            m.add("32316.dat", YELLOW, (x, 20, z), FLAT_X)
            m.add("2780.dat", BLACK, (x + e * 40, 30, z), PIN_DOWN)
            m.add("2780.dat", BLACK, (x + e * 20, 10, z), PIN_DOWN)
            m.add("6558.dat", BLUE, (x - e * 40, 20, z), PIN_DOWN)
    m.step()
    # 2: a 15-beam on each pair, one hole short of their outer ends; two pins up
    for z in (-RAIL_Z, RAIL_Z):
        m.add("32278.dat", LIME, (0, 0, z), FLAT_X)
        for x in (-40, 40):
            m.add("2780.dat", BLACK, (x, -10, z), PIN_DOWN)
    m.step()
    # 3: two 9-beams across on those pins
    for x in (-40, 40):
        m.add("40490.dat", LIME, (x, -20, 0))
    m.step()
    # 4: four pins up in their second holes from the middle
    for x in (-40, 40):
        for z in (-20, 20):
            m.add("2780.dat", BLACK, (x, -30, z), PIN_DOWN)
    m.step()
    # 5: the frame
    m.add("64179.dat", LBG, (0, -40, 0))
    m.step()
    hx, hy = HOOD[0], HOOD[1]
    # 6: the hood (built aside in the booklet): the curved panel, a cross block in its base
    #    holes, a 5-beam on the block's back pins, two pins back (into the frame's front)
    m.add("24119.dat", YELLOW, tuple(HOOD), HOOD_PANEL)
    m.add("48989.dat", BLACK, (hx - 20, hy, 0), BLOCK_X)
    m.add("32316.dat", LIME, (hx - 40, hy, 0), BEAM_ON_EDGE)
    for z in (-40, 40):
        m.add("2780.dat", BLACK, (hx - 50, hy, z))
    m.step()
    # 7: blue 3L pins up through a flat 7-beam and two pins with pin holes into the panel's
    #    surface holes; the pin holes' pins point forward
    m.add("32524.dat", LIME, (hx + 40, hy + 60, 0))
    for z in (-40, 40):
        m.add("15100.dat", BLACK, (hx + 40, hy + 40, z))
        m.add("6558.dat", BLUE, (hx + 40, hy + 40, z), PIN_DOWN)
    m.step()
    # 8: a cross block under the 7-beam, two pins up into it, two down
    m.add("48989.dat", BLACK, (hx + 40, hy + 80, 0), BLOCK_Y)
    m.step()
    # 9: two pins forward in its side holes, a yellow 3-beam on them
    for z in (-20, 20):
        m.add("2780.dat", BLACK, (hx + 50, hy + 80, z))
    m.add("32523.dat", YELLOW, (hx + 60, hy + 80, 0), BEAM_ON_EDGE)
    m.step()
    # 10: a 7-beam on edge on the pin holes' pins, horns on axle pins in its end holes; two
    #     3/4 pins in the top of the first cross block
    m.add("32524.dat", LIME, (hx + 60, hy + 40, 0), BEAM_ON_EDGE)
    for z in (-60, 60):
        m.add("43093.dat", BLUE, (hx + 70, hy + 40, z))
        m.add("41669.dat", TRANS_RED, (hx + 80, hy + 40, z), HORN_FRONT)
    for z in (-20, 20):
        m.add("32002.dat", LBG, (hx - 20, hy - 10, z), PIN_UP)
    m.step()
    # 11: the wing assembly (built aside): the top frame, four pins down from its corners
    m.add("64179.dat", LBG, (0, -60, 0))
    for x in (-40, 40):
        for z in (-60, 60):
            m.add("2780.dat", BLACK, (x, -50, z), PIN_DOWN)
    m.step()
    # 12: a 5-beam on edge behind it on two pins, blue 3L pins back through its holes 2 and 4
    m.add("32316.dat", LIME, (-60, -60, 0), BEAM_ON_EDGE)
    for z in (-40, 40):
        m.add("2780.dat", BLACK, (-50, -60, z))
    for z in (-20, 20):
        m.add("6558.dat", BLUE, (-80, -60, z))
    m.step()
    # 13: 157.5-degree angle connectors on the 3L pins (one arm down, one up and out), a second
    #     5-beam on the pins' ends, pins with pin holes in its end holes
    for s in (-1, 1):
        m.add("32016.dat", BLACK, tuple(hub(s)), ANGLE[s])
    m.add("32316.dat", LIME, (-100, -60, 0), BEAM_ON_EDGE)
    for s in (-1, 1):
        m.add("15100.dat", BLACK, (-120, -60, s * 40))
    m.step()
    # 14: axle pins in the upper arms, pins with pin holes on them, their pins out
    for s in (-1, 1):
        m.add("43093.dat", BLUE, tuple(hub(s) + 30 * ARM[s]), frame(-ARM[s], OUT[s]))
        m.add("15100.dat", BLACK, tuple(pin_hole_1(s)), frame(OUT[s], ARM[s]))
    m.step()
    # 15: a second pin with pin hole on each, its pin swept back
    for s in (-1, 1):
        m.add("15100.dat", BLACK, tuple(pin_hole_2(s)), frame(SWEPT[s], OUT[s]))
    m.step()
    # 16: the wings (fairings #3 and #4)
    for s in (-1, 1):
        m.add(WING[s], LIME, tuple(pin_hole_2(s) + 20 * SWEPT[s]), wing_matrix(s))
    m.step()
    # 17: horns on axle pins in the back pin holes, pointing back
    for s in (-1, 1):
        m.add("43093.dat", BLUE, (-120, -70, s * 40), PIN_UP)
        m.add("41669.dat", TRANS_RED, (-120, -80, s * 40), HORN_BACK)
    m.step()
    bx, by = BACK[0], BACK[1]
    # 18: the back panel (built aside): the curved panel, a cross block in its base holes, a
    #     5-beam on edge on the block's front pins
    m.add("24119.dat", YELLOW, tuple(BACK), BACK_PANEL)
    m.add("48989.dat", BLACK, (bx + 20, by, 0), BLOCK_X)
    m.add("32316.dat", LIME, (bx + 40, by, 0), BEAM_ON_EDGE)
    m.step()
    # 19: axle pins up in the cross block (into the angle connectors' lower arms); pins up into
    #     the panel's surface holes through a flat 5-beam, a cross block under it with round
    #     plates in its side holes
    for z in (-20, 20):
        m.add("43093.dat", BLUE, (bx + 20, by - 10, z), PIN_UP)
    for z in (-40, 40):
        m.add("2780.dat", BLACK, (bx - 40, by + 30, z), PIN_DOWN)
    m.add("32316.dat", LIME, (bx - 40, by + 40, 0))
    m.add("48989.dat", BLACK, (bx - 40, by + 60, 0), BLOCK_Y)
    for z in (-20, 20):
        m.add("85861.dat", TRANS_RED, (bx - 50, by + 60, z), PLATE_BACK)
    m.step()
    # 20: pins in the panel's base end holes, pins with pin holes on them, their pins down
    #     (into the rails)
    for s in (-1, 1):
        m.add("2780.dat", BLACK, (bx, by, s * 70), ACROSS)
        m.add("15100.dat", BLACK, (bx, by, s * 80), PIN_HOLE_ON_Z_DOWN)
    m.step()
    # (booklet 21-23: the back panel goes under the wings, the wing assembly on the frame, the
    #  hood on the frame's front)
    # 21 (booklet 24): a bent beam on each side, its short arm's axle end on an axle pin in the
    #     hood panel's base end hole, the long arm back over the side
    for s in (-1, 1):
        m.add("43093.dat", BLUE, (hx, hy, s * 70), TO_PLUS_Z if s > 0 else TO_MINUS_Z)
        m.add("32009.dat", YELLOW, tuple(np.array([hx, hy, s * 80]) - BENT @ np.array([80.0, 0, 0])), BENT)
    m.step()


def servos(m, ends=(-1, 1)):
    """Step 22: the servos at the given ends of the car (-1 back, 1 front)."""
    # 22 (booklet 25, upside down): the servos on the rails' end pins, outputs out; a pin in
    #     each lug's other end
    for fx in ends:
        for side in (-1, 1):
            m.add("geekedu-ef-geekservo-360.dat", LIME, (fx * SERVO_X, SERVO_Y, side * RAIL_Z), servo(fx, side))
    for fx in ends:
        for side in (-1, 1):
            for x in (80, 160):
                m.add("2780.dat", BLACK, (fx * x, 70, side * RAIL_Z), PIN_DOWN)
    m.step()


def underside(m, ends=(-1, 1), outer_beams=True):
    """Steps 23-24: the beams under the car, across only at the ends that have servos.
    outer_beams=False leaves out the two at the car's ends (the geared tank puts a 7-beam per side there)."""
    # 23 (booklet 26): two 15-beams under the middle on the hood's and the back panel's cross
    #     block pins, a pin down in each one's holes 4 and 12
    for z in (-20, 20):
        m.add("32278.dat", LIME, (0, 60, z), FLAT_X)
        for x in (-80, 80):
            if np.sign(x) in ends:
                m.add("2780.dat", BLACK, (x, 70, z), PIN_DOWN)
    m.step()
    # 24 (booklet 27): four 9-beams across on the servo lug pins and those pins
    for x in (-160, -80, 80, 160) if outer_beams else (-80, 80):
        if np.sign(x) in ends:
            m.add("40490.dat", LIME, (x, 80, 0))
    m.step()


def wheels(m):
    # 25 (booklet 28): the mecanum wheels on the outputs; left-hand wheels front left and back
    #     right, as the booklet's top view shows the rollers
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add(WHEEL[(fx, side)], YELLOW, (fx * (SERVO_X + 10), SERVO_Y, side * WHEEL_Z))
    m.step()


def board(m):
    # 26 (booklet 29): the Wukong board on four pins in the top frame
    for x in (-40, 40):
        for z in (-20, 20):
            m.add("2780.dat", BLACK, (x, -70, z), PIN_DOWN)
    m.add("geekedu-ef-wukong-board.dat", LBG, (0, -80, 0))
    m.step()
    # 27 (booklet 30): a 5-beam on edge on two pins in the board's front, three round plates
    #     in its middle holes; the callout's other two pins in the back side holes (the
    #     booklet's picture hides that face)
    m.add("32316.dat", LIME, (60, -80, 0), BEAM_ON_EDGE)
    for z in (-40, 40):
        m.add("2780.dat", BLACK, (50, -80, z))
    for z in (-20, 0, 20):
        m.add("85861.dat", TRANS_RED, (70, -80, z), PLATE_FRONT)
    for z in (-40, 40):
        m.add("2780.dat", BLACK, (-50, -80, z))
    m.step()


def build():
    m = ldr.Model("wukong-mecanum-racer")
    body(m)
    servos(m)
    underside(m)
    wheels(m)
    board(m)
    return m
