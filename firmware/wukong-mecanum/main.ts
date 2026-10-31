function showDirection () {
    if (y_dir == "F") {
        if (arrow_x == "L") {
            images.arrowImage(ArrowNames.NorthWest).showImage(0, 0)
        } else if (arrow_x == "R") {
            images.arrowImage(ArrowNames.NorthEast).showImage(0, 0)
        } else {
            images.arrowImage(ArrowNames.North).showImage(0, 0)
        }
    } else if (y_dir == "B") {
        if (arrow_x == "L") {
            images.arrowImage(ArrowNames.SouthWest).showImage(0, 0)
        } else if (arrow_x == "R") {
            images.arrowImage(ArrowNames.SouthEast).showImage(0, 0)
        } else {
            images.arrowImage(ArrowNames.South).showImage(0, 0)
        }
    } else if (arrow_x == "L") {
        images.arrowImage(ArrowNames.West).showImage(0, 0)
    } else if (arrow_x == "R") {
        images.arrowImage(ArrowNames.East).showImage(0, 0)
    }
    showPower(Math.max(Math.max(y_level, x_level), s_level))
}
// a shorter arrow for less power: one dot of its shaft for 1-3, two for 4-6, the whole arrow for 7-9
function showPower (power: number) {
    // where the arrow points (right 1, left -1, up -1, down 1): its shaft runs back from the middle
    point_x = 0
    point_y = 0
    if (arrow_x == "R") {
        point_x = 1
    } else if (arrow_x == "L") {
        point_x = -1
    }
    if (y_dir == "F") {
        point_y = -1
    } else if (y_dir == "B") {
        point_y = 1
    }
    if (point_x != 0 || point_y != 0) {
        if (power < 7) {
            led.unplot(2 - 2 * point_x, 2 - 2 * point_y)
        }
        if (power < 4) {
            led.unplot(2 - point_x, 2 - point_y)
        }
    }
}
function stop () {
    wuKong.mecanumRun(wuKong.RunList.stop, 0)
    images.iconImage(IconNames.No).showImage(0, 0)
}
// a part of a command as a speed: SLOW to SPEED one way, minus that the other way, 0 for N
function signed (dir: string, level: number, plus: string, minus: string) {
    if (dir == plus) {
        return Math.map(level, 1, 9, SLOW, SPEED)
    } else if (dir == minus) {
        return 0 - Math.map(level, 1, 9, SLOW, SPEED)
    }
    return 0
}
function drive () {
    // stick 1: up/down drives, left/right turns; stick 2 (the phone joystick's second one): sideways
    forward = signed(y_dir, y_level, "F", "B")
    turn = signed(x_dir, x_level, "R", "L")
    strafe = signed(s_dir, s_level, "R", "L")
    if (forward == 0 && turn == 0 && strafe == 0) {
        stop()
    } else {
        mecanum(forward, strafe, turn)
        // the arrow shows the slide when the car slides sideways, else the turn
        arrow_x = x_dir
        if (s_dir == "L" || s_dir == "R") {
            arrow_x = s_dir
        }
        showDirection()
    }
}
// the four wheels from ahead (forward +), side (right +) and rotate (right +), exactly as gm0.org's
// mecanum drive: each wheel gets ahead plus or minus side and rotate, and all four share one
// denominator, so they keep their ratio (a car that slides the wrong way or twists has two motors
// in each other's ports: the motor test shows which; a wheel's SLIDE is -1 when it alone is mounted
// the other way round)
function mecanum (ahead: number, side: number, rotate: number) {
    // the rollers lose some of a slide: a little more of it (gm0: 1.1)
    sideways = side * STRAFE_GAIN
    denominator = Math.max(Math.abs(ahead) + Math.abs(sideways) + Math.abs(rotate), SPEED)
    left_front = (ahead + LF_SLIDE * sideways + rotate) * SPEED / denominator
    left_rear = (ahead - LR_SLIDE * sideways + rotate) * SPEED / denominator
    right_front = (ahead - RF_SLIDE * sideways - rotate) * SPEED / denominator
    right_rear = (ahead + RR_SLIDE * sideways - rotate) * SPEED / denominator
    wuKong.mecanumSpeed(wuKong.WheelList.LeftFront_def, Math.round(left_front * DIRECTION))
    wuKong.mecanumSpeed(wuKong.WheelList.LeftRear_def, Math.round(left_rear * DIRECTION))
    wuKong.mecanumSpeed(wuKong.WheelList.RightFront_def, Math.round(right_front * DIRECTION))
    wuKong.mecanumSpeed(wuKong.WheelList.RightRear_def, Math.round(right_rear * DIRECTION))
}
// the motor test (T, the phone joystick's Test motors button): each motor turns forward, then back, with its number on the display
function testMotor (motor: number) {
    basic.showNumber(motor)
    control.raiseEvent(9101, motor)
    runMotor(motor, TEST)
    basic.pause(1000)
    runMotor(motor, 0 - TEST)
    basic.pause(1000)
    runMotor(motor, 0)
    basic.pause(300)
}
// 1: left front (S0), 2: right front (S2), 3: left rear (S1), 4: right rear (S3)
function runMotor (motor: number, speed: number) {
    if (motor == 1) {
        wuKong.mecanumSpeed(wuKong.WheelList.LeftFront_def, speed * DIRECTION)
    } else if (motor == 2) {
        wuKong.mecanumSpeed(wuKong.WheelList.RightFront_def, speed * DIRECTION)
    } else if (motor == 3) {
        wuKong.mecanumSpeed(wuKong.WheelList.LeftRear_def, speed * DIRECTION)
    } else {
        wuKong.mecanumSpeed(wuKong.WheelList.RightRear_def, speed * DIRECTION)
    }
}
function testMotors () {
    testMotor(1)
    testMotor(2)
    testMotor(3)
    testMotor(4)
    // then gm0's three basic moves, numbered on: 5 forward, 6 slide right, 7 turn right
    testMove(5, TEST, 0, 0)
    testMove(6, 0, TEST, 0)
    testMove(7, 0, 0, TEST)
}
// one move of the motor test: its number on the display, all four wheels for 1.5 s, then stop
function testMove (move: number, ahead: number, side: number, rotate: number) {
    basic.showNumber(move)
    control.raiseEvent(9101, move)
    mecanum(ahead, side, rotate)
    basic.pause(1500)
    wuKong.mecanumRun(wuKong.RunList.stop, 0)
    basic.pause(300)
}
// a command looks like M,F7,R3 (forward at 7 of 9, right at 3 of 9), or M,F7,R3,L5 with sliding left at 5 of 9; S stops; T tests the motors one by one; I reports what this is
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    receivedString = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    lastCommand = control.millis()
    command = receivedString.substr(0, 1)
    if (command == "M" && !testing) {
        y_dir = receivedString.substr(2, 1)
        y_level = parseFloat(receivedString.substr(3, 1))
        x_dir = receivedString.substr(5, 1)
        x_level = parseFloat(receivedString.substr(6, 1))
        s_dir = receivedString.substr(8, 1)
        s_level = parseFloat(receivedString.substr(9, 1))
        drive()
    } else if (command == "S" && !testing) {
        stop()
    } else if (command == "T" && !testing) {
        // the forever loop below runs the test, so this handler answers the commands that come meanwhile
        testing = true
    } else if (command == "I") {
        // the phone joystick asks what this is: model 1 (the Wukong mecanum racer) and this program's release
        control.raiseEvent(9102, 1)
        control.raiseEvent(9103, 35)
    }
    // tell the phone joystick this command is done, so it sends the next one at once
    control.raiseEvent(9100, 2)
})
input.onButtonPressed(Button.B, function () {
    basic.showString(control.deviceName())
})
bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
})
bluetooth.onBluetoothDisconnected(function () {
    stop()
})
let denominator = 0
let sideways = 0
let right_rear = 0
let left_rear = 0
let right_front = 0
let left_front = 0
let strafe = 0
let turn = 0
let forward = 0
let arrow_x = ""
let point_y = 0
let point_x = 0
let s_level = 0
let s_dir = ""
let x_level = 0
let y_level = 0
let lastCommand = 0
let testing = false
let command = ""
let x_dir = ""
let y_dir = ""
let receivedString = ""
// SPEED: full speed; SLOW: speed at the slightest push (the wheels stall below about 30)
let SPEED = 100
let SLOW = 30
// TEST: speed in the motor test
let TEST = 60
// SLIDE, one per wheel: 1 as in the guide, -1 for a wheel mounted the other way round. The car
// twists or does not slide: see "Which motor is which?" on the joystick page for which ones
let LF_SLIDE = 1
let RF_SLIDE = 1
let LR_SLIDE = 1
let RR_SLIDE = 1
// DIRECTION: -1 when every wheel turns on a gear pair (the Brick Race racer), which turns it the other way round
let DIRECTION = -1
// STRAFE_GAIN: how much more a slide gets than driving ahead (gm0: 1.1, the rollers lose some)
let STRAFE_GAIN = 1.1
bluetooth.startUartService()
// this program's release, so you can tell which one a micro:bit runs
basic.showString("r35")
basic.showIcon(IconNames.Heart)
// the motor test when T asked for it; else the joystick sends commands all the time: when they
// stop (out of range, flat battery), stop
basic.forever(function () {
    if (testing) {
        testMotors()
        testing = false
        stop()
        control.raiseEvent(9101, 0)
    } else if (lastCommand > 0 && control.millis() - lastCommand > 1500) {
        lastCommand = 0
        stop()
    }
})
