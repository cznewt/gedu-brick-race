"""Wukong tank with four servos, geared 2:1: our design, the four-servo Wukong tank
(wukong_tank_4_motors.py: the Wukong mecanum racer's body on tracks from the Building:bit kit)
with each servo geared up 2:1 and the belt shaped like the Building:bit tank's. The body,
servos and underside are the racer's (steps 1-9, the end 9-beams left out); the racer's bearing
frames (10-13: bridges, 7-beams a stud outboard of the lug line, ties, L-beams with the pins with
pin holes) hold the drive axles: a 16-tooth gear on each servo's
output turns the 8-tooth gear on a 7L axle through the ring, and the sprocket sits on the axle
past the ring, so the tracks run twice as fast as the servos turn, with half the pull. The ring
is 30 LDU along and 10 below the output: the gears' axles are 31.6 LDU apart, 1.6 LDU (0.65 mm)
more than LEGO's 30 for 16 and 8 teeth, so the teeth mesh 2.5 LDU deep instead of 4.1. A 15-beam
hangs under the middle of the car on 3L pins through the 15-beams there, and a pin with pin
hole in each of its end holes carries an idler sprocket one module below the drive sprockets:
the belt's bottom run bends down to it and the tank stands on the idlers, its ends 8 mm off the
floor, like the Building:bit tank (the user, 2026-10-31: "the belt shape with extra wheel"). One
module is what 31 links allow, the count that made the plain belt as round as the four-servo
tank's 27 (two modules lower needs 32 links and leaves 2 cm of slack). The Building:bit links
are 5 studs wide, so the tracks start outboard of the gears and of the bearing frames: the
sprocket hubs sit at 217 and the car is 21.2 cm wide over the tracks. The driver's directions are -1: a gear pair turns each
sprocket the other way. World: front = +X, left = +Z, Y points down."""
import numpy as np

import ldr
import wukong_mecanum as racer
from ldr import R
from tracks import Track
from wonder_common import BLACK, BLUE, DBG, LBG, PIN_DOWN

ACROSS = R(("y", 90))                                       # axle along Z
OUTPUTS = ((-racer.OUT_X, racer.OUT_Y), (racer.OUT_X, racer.OUT_Y))         # back, front
DRIVES = ((-racer.RING_X, racer.RING_Y), (racer.RING_X, racer.RING_Y))      # back, front: the sprockets on the ring axles
IDLER = (0, racer.RING_Y + 20)                              # the idler, a module below the drive sprockets
WHEELS = (DRIVES[0], DRIVES[1], IDLER)                      # back, forward along the top, then the low idler
MIDDLE_Y = 100                                              # the 15-beam under the middle, on 3L pins from the keel
IDLER_RING_Z = 140                                          # its end holes: the idlers' pins with pin holes
GEAR_Z = racer.GEAR_Z                                       # the gears' middle, the 16-tooth one against the servo (z = 126)
WHEEL_Z = 217                                               # sprocket hubs: the links (5 studs wide) start at 169, past the frames' ends
# along each drive axle (left side, the right mirrored): a bush clear of the lug (96..116), the
# 8-tooth gear (116..136), a half bush, 5 free, the ring (151..169), a half bush, a bush, the
# sprocket (199..235), a half bush; the 8L axle from z = 96 to 256
BUSH_Z, SPACER_Z, OUTER_SPACER_Z, OUTER_BUSH_Z, END_BUSH_Z, AXLE_Z = 106, 141, 174, 189, 240, 176
# along each idler axle: the ring (131..149), a bush, a half bush, a bush, the sprocket, a half
# bush; the 6L axle from z = 130 to 250
IDLER_BUSH_Z, IDLER_SPACER_Z, IDLER_AXLE_Z = 159, 174, 190
TRACK = Track(WHEELS, 31)
# the racer's cameras for its steps; the middle beam from below, the gears from the left, the
# axles and sprockets from the front left, low, the tracks from the front left
ARM_X = racer.ARM_X                                         # the racer's frames: a stud out the 8-tooth gear still reaches the 7-beam, two studs out the belt must start past it
VIEW = dict(racer.VIEW, step_views={**racer.VIEW["step_views"], 14: (160, -35), 15: (160, 8), 16: (150, 10),
                                    17: (150, 10), 18: (135, 20), 19: (130, 30), 20: (140, 35)})


def build():
    m = ldr.Model("wukong-tank-4servo-geared")
    racer.body(m)
    racer.servos(m)
    racer.underside(m, outer_beams=False)
    racer.end_beams(m, ARM_X)
    racer.ties(m)
    racer.bearings(m, ARM_X)
    # 14: a 15-beam under the middle of the car, on two blue 3L pins down through the 15-beams
    #     there; a pin with pin hole down in each of its end holes, the hole along the car's axles
    for z in (-20, 20):
        m.add("6558.dat", BLUE, (0, 80, z), PIN_DOWN)
    m.add("32278.dat", racer.LIME, (0, MIDDLE_Y, 0))
    for s in (1, -1):
        m.add("15100.dat", BLACK, (IDLER[0], IDLER[1], IDLER_RING_Z * s), racer.PIN_HOLE_ON_Z_DOWN)
    m.step()
    # 15: a 16-tooth gear pushed all the way onto each servo's output
    for x, y in OUTPUTS:
        for s in (1, -1):
            m.add("94925.dat", LBG, (x, y, GEAR_Z * s), racer.mesh(np.sign(x), 16, 8)[0])
    m.step()
    # 16: (x4) an 8L axle through the ring: inside it a half bush against the ring, the 8-tooth gear
    #     in the 16-tooth gear's teeth and a bush; outside it a half bush and a bush
    for x, y in DRIVES:
        turn = racer.mesh(np.sign(x), 16, 8)[1]            # the axle's cross as the 8-tooth gear's hole
        for s in (1, -1):
            m.add("3707.dat", LBG, (x, y, AXLE_Z * s), turn @ ACROSS)
            m.add("3713.dat", LBG, (x, y, BUSH_Z * s), turn)
            m.add("10928.dat", DBG, (x, y, GEAR_Z * s), turn)
            m.add("4265c.dat", LBG, (x, y, SPACER_Z * s), turn)
            m.add("4265c.dat", LBG, (x, y, OUTER_SPACER_Z * s), turn)
            m.add("3713.dat", LBG, (x, y, OUTER_BUSH_Z * s), turn)
    m.step()
    # 17: (x2) a 6L axle through each idler's ring, a bush, a half bush and a bush on it outside
    for s in (1, -1):
        turn = TRACK.sprocket_turn(IDLER)
        m.add("3706.dat", LBG, (IDLER[0], IDLER[1], IDLER_AXLE_Z * s), turn @ ACROSS)
        m.add("3713.dat", LBG, (IDLER[0], IDLER[1], IDLER_BUSH_Z * s), turn)
        m.add("4265c.dat", LBG, (IDLER[0], IDLER[1], IDLER_SPACER_Z * s), turn)
        m.add("3713.dat", LBG, (IDLER[0], IDLER[1], OUTER_BUSH_Z * s), turn)
    m.step()
    # 18: a sprocket on each axle against the half bush, a half bush outside it
    for x, y in WHEELS:
        for s in (1, -1):
            turn = TRACK.sprocket_turn((x, y))
            m.add("57519.dat", DBG, (x, y, WHEEL_Z * s), turn)
            m.add("4265c.dat", LBG, (x, y, END_BUSH_Z * s), turn)
    m.step()
    # 19: (x2) 31 links to a track, round each side's two sprockets and under its idler
    for s in (1, -1):
        TRACK.links(m, DBG, WHEEL_Z * s)
    m.step()
    racer.board(m)
    return m
