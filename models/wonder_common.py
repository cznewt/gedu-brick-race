"""Shared by the Wonder Building Kit models: colours, orientations, and the chassis the
cars start with (booklet steps 1-3: the 5 x 7 frame, two motors under its short ends, the
rear wheels). World: that frame flat at the origin, long axis Z, front = +X; Y points down."""
import numpy as np

from ldr import R

LBG, DBG, BLACK, RED, YELLOW, BLY, WHITE, BLUE, TAN = 71, 72, 0, 4, 14, 226, 15, 1, 19
ROT_Y180 = R(("y", 180))
PIN_DOWN = R(("z", 90))        # pin's +X end points down (+Y)
BEAM_ON_EDGE = R(("z", 90))    # beam along Z with its holes along X


def chassis(m, bush=BLY, wheels=True):
    # 1: the 5 x 7 frame
    m.add("64179.dat", LBG)
    m.step()
    # 2: two motors under the short ends, pinned into the frame's corner holes;
    #    turned so their axle hubs sit toward the back (-X)
    for z in (-60, 60):
        m.add("geekedu-ef-geekservo-2kg-motor.dat", RED, (0, 40, z), ROT_Y180)
        for x in (-40, 40):
            m.add("32002.dat", LBG, (x, 10, z), PIN_DOWN)
    m.step()
    if not wheels:
        return
    # 3: rear wheels on the motor outputs (hub at x = -20): axle 3, half bush, rim, tyre
    for side in (-1, 1):
        zf = side * 90                       # outer axle face
        M = ROT_Y180 if side > 0 else np.eye(3)       # spokes outward
        m.add("4519.dat", LBG, (-20, 40, zf + side * 10), R(("y", 90)))
        m.add("4265c.dat", bush, (-20, 40, zf + side * 5))
        m.add("56145.dat", LBG, (-20, 40, zf + side * 35), M)
        m.add("55978.dat", BLACK, (-20, 40, zf + side * 35), M)
    m.step()


def wukong(m, x=0):
    """The Wukong board on the frame centred at x, pinned in the long sides' second holes."""
    for dx in (-40, 40):
        for z in (-20, 20):
            m.add("2780.dat", BLACK, (x + dx, -10, z), PIN_DOWN)
    m.add("geekedu-ef-wukong-board.dat", LBG, (x, -20, 0), ROT_Y180)


MICROBIT_ON_WUKONG = np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]])   # display towards the board's +X (its slot side)


def microbit(m, wukong_pos, wukong_rot=np.eye(3)):
    """The micro:bit standing in the slot of a Wukong board placed at wukong_pos, wukong_rot."""
    wukong_rot = np.asarray(wukong_rot, dtype=float)
    pos = wukong_rot @ np.array([25.0, -145.0, 0.0]) + np.asarray(wukong_pos, dtype=float)
    m.add("geekedu-microbit-v2.dat", BLACK, tuple(pos), wukong_rot @ MICROBIT_ON_WUKONG)
