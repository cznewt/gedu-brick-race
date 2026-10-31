"""Wukong mecanum racer: our design after the ElecFreaks Wonder Rugged Kit racer, without its
hood, wings, horns, lights and bent beams (the user, 2026-10-31: "clean uncommon pieces for
aesthetic"). Two side rails (a lime 15-beam on two yellow 5-beams) carry two 9-beams and two
5 x 7 frames; the four green Geekservo 360 servos hang on the rails' end pins, outputs
outwards, with lime beams under them. The wheels are not on the servos: each servo's output
turns a 12-tooth double bevel gear that drives a second one on an 8L axle, held by a pin with
pin hole on a 7-beam under the car's end (the two 7-beams of an end tied by a 5-beam), and the
mecanum wheel sits on that axle past the ring. The gears' axles are 31.6 LDU apart, 1.6 LDU
(0.65 mm) more than LEGO's 30 for two 12-tooth gears, so the teeth mesh 2.4 LDU deep instead of
4. A gear pair turns each wheel the other way round: the driver's DIRECTION setting is -1 (the
mecanum wheels' pattern, left-hand wheels at front left and back right, stays). The Wukong board
sits on the top frame, micro:bit at the front. The tanks (wukong_tank_*.py) build the same body
and servos and their own drives. World: front = +X, left = +Z, Y points down; the lower frame is
centred on the X-Z origin."""
import numpy as np

import ldr
from ldr import R
from wonder_common import BLACK, BLUE, LBG, PIN_DOWN, YELLOW

LIME = 27
FLAT_X = R(("y", 90))                                      # beam along X, holes vertical
ACROSS = R(("y", 90))                                      # pin or axle along Z
PIN_HOLE_ON_Z_DOWN = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])   # 15100: pin hole along Z, pin down
WHEEL = {(1, 1): "geekedu-ef-mecanum-wheel-left.dat", (-1, -1): "geekedu-ef-mecanum-wheel-left.dat",
         (1, -1): "geekedu-ef-mecanum-wheel-right.dat", (-1, 1): "geekedu-ef-mecanum-wheel-right.dat"}
SERVO_X, SERVO_Y, RAIL_Z = 120, 50, 80                     # servo centres (on the rails' end pins)
OUT_X, OUT_Y = SERVO_X + 10, SERVO_Y                       # the outputs sit 10 off the servos' centres
RING_X, RING_Y = SERVO_X + 40, SERVO_Y + 10                # the pin with pin hole on the 7-beam's outer hole
BEAM_Z = RAIL_Z + 20                                       # the 7-beams' middles: holes from 40 to 160, the lug pin in 80
TIE_Z = RAIL_Z - 40                                        # the 7-beams' innermost holes (z = 40): the 5-beam's end pins
RING_Z = RAIL_Z + 80                                       # the 7-beams' outer holes (z = 160)
GEAR_Z = RAIL_Z + 46                                       # the gears' middle, the one on the output against the servo (z = 126)
WHEEL_Z = 231.5                                            # wheel centre: inner plate against the half bush past the ring
# along each ring axle (left side, the right mirrored): a bush clear of the lug (96..116), the
# gear (116..136), a half bush, 5 free, the ring (151..169), a half bush, the wheel (179..284);
# the 8L axle from z = 96 to 256
BUSH_Z, SPACER_Z, OUTER_SPACER_Z, AXLE_Z = 106, 141, 174, 176
# the cameras: the rails and the chassis as the kit's booklet shows them; the servos and the
# beams under the car from below (the booklet turns the car over); the drive from the front
# left, low; the board from the front left
VIEW = dict(az=125, el=28, cover_az=130, cover_el=30,
            step_views={1: (330, 20), 2: (150, 20), 3: (65, 35), 4: (65, 35), 5: (65, 30), 6: (270, 35),
                        7: (60, -35), 8: (160, -40), 9: (160, -35), 10: (150, 12), 11: (150, 12),
                        12: (160, 8), 13: (150, 10), 14: (130, 30), 15: (140, 35)})


def frame(x, y):
    """Rotation with local X along x and local Y along y (unit, perpendicular)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    return np.column_stack([x, y, np.cross(x, y)])


def servo(fx, side):
    """Geekservo 360 on a rail: lugs along X, output (local -Y) outwards, output offset (local +X)
    towards the car's end fx."""
    return frame((fx, 0, 0), (0, 0, -side))


def mesh(fx, teeth_out, teeth_axle):
    """The gears' turns about Z at the end fx (-1 back, 1 front): a tooth of the output's gear on
    the line between the axles, a gap of the axle's gear there (LDraw's gears have a tooth at
    0 degrees)."""
    a = np.degrees(np.arctan2(RING_Y - OUT_Y, fx * (RING_X - OUT_X)))
    p_out, p_axle = 360 / teeth_out, 360 / teeth_axle
    return R(("z", a % p_out)), R(("z", (a + 180 + p_axle / 2) % p_axle))


def body(m):
    """Steps 1-6: the rails, the 9-beams and the two frames."""
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
    # 6: the top frame on four pins down from its corners
    m.add("64179.dat", LBG, (0, -60, 0))
    for x in (-40, 40):
        for z in (-60, 60):
            m.add("2780.dat", BLACK, (x, -50, z), PIN_DOWN)
    m.step()


def servos(m, ends=(-1, 1)):
    """Step 7: the servos at the given ends of the car (-1 back, 1 front)."""
    # 7: the servos on the rails' end pins, outputs out; a pin down in each lug's other end
    for fx in ends:
        for side in (-1, 1):
            m.add("geekedu-ef-geekservo-360.dat", LIME, (fx * SERVO_X, SERVO_Y, side * RAIL_Z), servo(fx, side))
    for fx in ends:
        for side in (-1, 1):
            for x in (80, 160):
                m.add("2780.dat", BLACK, (fx * x, 70, side * RAIL_Z), PIN_DOWN)
    m.step()


def underside(m, ends=(-1, 1), outer_beams=True):
    """Steps 8-9: the beams under the car, across only at the ends that have servos.
    outer_beams=False leaves out the two at the car's ends (the geared cars put a 7-beam per side
    there, end_beams())."""
    # 8: two 15-beams under the middle, a pin down in each one's holes 4 and 12
    for z in (-20, 20):
        m.add("32278.dat", LIME, (0, 60, z), FLAT_X)
        for x in (-80, 80):
            if np.sign(x) in ends:
                m.add("2780.dat", BLACK, (x, 70, z), PIN_DOWN)
    m.step()
    # 9: 9-beams across on those pins and the servo lugs' pins
    for x in (-160, -80, 80, 160) if outer_beams else (-80, 80):
        if np.sign(x) in ends:
            m.add("40490.dat", LIME, (x, 80, 0))
    m.step()


def end_beams(m, ends=(-1, 1)):
    """Step 10: the geared cars' bearings: (x4) a 7-beam under each end of the car on the outer
    lug's pin, its outer end past the servo; a pin up in its innermost hole, a pin with pin hole
    down in its outer hole, the hole along the car's axles."""
    for fx in ends:
        for s in (1, -1):
            m.add("32524.dat", LIME, (fx * RING_X, 80, BEAM_Z * s))
            m.add("2780.dat", BLACK, (fx * RING_X, 70, TIE_Z * s), PIN_DOWN)
            m.add("15100.dat", BLACK, (fx * RING_X, RING_Y, RING_Z * s), PIN_HOLE_ON_Z_DOWN)
    m.step()


def ties(m, ends=(-1, 1)):
    """Step 11: (x2) a 5-beam across the two 7-beams' inner ends, on those pins: on one pin a
    beam could turn."""
    for fx in ends:
        m.add("32316.dat", LIME, (fx * RING_X, 60, 0))
    m.step()


def drive(m):
    """Steps 12-14: the 1:1 gear pairs, the axles and the mecanum wheels."""
    # 12: a 12-tooth double bevel gear pushed all the way onto each servo's output
    for fx in (-1, 1):
        for s in (1, -1):
            m.add("32270.dat", LBG, (fx * OUT_X, OUT_Y, GEAR_Z * s), mesh(fx, 12, 12)[0])
    m.step()
    # 13: (x4) an 8L axle through the ring: inside it a half bush against the ring, the second
    #     12-tooth gear in the first one's teeth and a bush; outside it a half bush
    for fx in (-1, 1):
        turn = mesh(fx, 12, 12)[1]                          # the axle's cross as the gear's hole
        for s in (1, -1):
            m.add("3707.dat", LBG, (fx * RING_X, RING_Y, AXLE_Z * s), turn @ ACROSS)
            m.add("3713.dat", LBG, (fx * RING_X, RING_Y, BUSH_Z * s), turn)
            m.add("32270.dat", LBG, (fx * RING_X, RING_Y, GEAR_Z * s), turn)
            m.add("4265c.dat", LBG, (fx * RING_X, RING_Y, SPACER_Z * s), turn)
            m.add("4265c.dat", LBG, (fx * RING_X, RING_Y, OUTER_SPACER_Z * s), turn)
    m.step()
    # 14: the mecanum wheels on the axles against the half bushes; left-hand wheels at front
    #     left and back right (the kit's top view shows the rollers)
    for fx in (-1, 1):
        for side in (-1, 1):
            m.add(WHEEL[(fx, side)], YELLOW, (fx * RING_X, RING_Y, side * WHEEL_Z))
    m.step()


def board(m):
    """The Wukong board on four pins in the top frame, its micro:bit slot at the front."""
    for x in (-40, 40):
        for z in (-20, 20):
            m.add("2780.dat", BLACK, (x, -70, z), PIN_DOWN)
    m.add("geekedu-ef-wukong-board.dat", LBG, (0, -80, 0))
    m.step()


def build():
    m = ldr.Model("wukong-mecanum-racer")
    body(m)
    servos(m)
    underside(m, outer_beams=False)
    end_beams(m)
    ties(m)
    drive(m)
    board(m)
    return m
