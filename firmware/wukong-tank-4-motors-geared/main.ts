function showDirection () {
    if (y_dir == "F") {
        if (x_dir == "L") {
            images.arrowImage(ArrowNames.NorthWest).showImage(0, 0)
        } else if (x_dir == "R") {
            images.arrowImage(ArrowNames.NorthEast).showImage(0, 0)
        } else {
            images.arrowImage(ArrowNames.North).showImage(0, 0)
        }
    } else if (y_dir == "B") {
        if (x_dir == "L") {
            images.arrowImage(ArrowNames.SouthWest).showImage(0, 0)
        } else if (x_dir == "R") {
            images.arrowImage(ArrowNames.SouthEast).showImage(0, 0)
        } else {
            images.arrowImage(ArrowNames.South).showImage(0, 0)
        }
    } else if (x_dir == "L") {
        images.arrowImage(ArrowNames.West).showImage(0, 0)
    } else if (x_dir == "R") {
        images.arrowImage(ArrowNames.East).showImage(0, 0)
    }
    showPower(Math.max(y_level, x_level))
}
// a shorter arrow for less power: one dot of its shaft for 1-3, two for 4-6, the whole arrow for 7-9
function showPower (power: number) {
    // where the arrow points (right 1, left -1, up -1, down 1): its shaft runs back from the middle
    point_x = 0
    point_y = 0
    if (x_dir == "R") {
        point_x = 1
    } else if (x_dir == "L") {
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
// a 360° servo turns at a speed instead of to an angle: 89 holds it still, above 89 it turns one way, below the other
function servo (port: number, speed: number) {
    if (speed == 0) {
        angle = 89
    } else if (speed > 0) {
        angle = Math.map(speed, 1, 100, 90, 180)
    } else {
        angle = Math.map(0 - speed, 1, 100, 88, 0)
    }
    if (port == 0) {
        wuKong.setServoAngle(wuKong.ServoTypeList._180, wuKong.ServoList.S0, angle)
    } else if (port == 1) {
        wuKong.setServoAngle(wuKong.ServoTypeList._180, wuKong.ServoList.S1, angle)
    } else if (port == 2) {
        wuKong.setServoAngle(wuKong.ServoTypeList._180, wuKong.ServoList.S2, angle)
    } else {
        wuKong.setServoAngle(wuKong.ServoTypeList._180, wuKong.ServoList.S3, angle)
    }
}
// S0 and S1 drive the left track, S2 and S3 the right one; the right servos face the other way, so they turn the other way round
function motors (left: number, right: number) {
    servo(0, LEFT_FRONT * left)
    servo(1, LEFT_REAR * left)
    servo(2, 0 - RIGHT_FRONT * right)
    servo(3, 0 - RIGHT_REAR * right)
}
function stop () {
    motors(0, 0)
    images.iconImage(IconNames.No).showImage(0, 0)
}
function drive () {
    // y_level and x_level: how far the joystick is pushed, 0 to 9
    speed = Math.map(y_level, 1, 9, SLOW, SPEED)
    curve = Math.map(x_level, 0, 9, speed, speed * CURVE / SPEED)
    spin = Math.map(x_level, 1, 9, SLOW, SPEED)
    if (y_dir == "F") {
        if (x_dir == "L") {
            motors(curve, speed)
        } else if (x_dir == "R") {
            motors(speed, curve)
        } else {
            motors(speed, speed)
        }
    } else if (y_dir == "B") {
        if (x_dir == "L") {
            motors(0 - curve, 0 - speed)
        } else if (x_dir == "R") {
            motors(0 - speed, 0 - curve)
        } else {
            motors(0 - speed, 0 - speed)
        }
    } else if (x_dir == "L") {
        motors(0 - spin, spin)
    } else if (x_dir == "R") {
        motors(spin, 0 - spin)
    } else {
        stop()
    }
    showDirection()
}
// the motor test (T, the phone joystick's Test motors button): each servo turns forward, then back, with its number on the display
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
// 1: S0 left front, 2: S2 right front, 3: S1 left rear, 4: S3 right rear (the mecanum racer's order)
function runMotor (motor: number, speed: number) {
    if (motor == 1) {
        servo(0, LEFT_FRONT * speed)
    } else if (motor == 2) {
        servo(2, 0 - RIGHT_FRONT * speed)
    } else if (motor == 3) {
        servo(1, LEFT_REAR * speed)
    } else {
        servo(3, 0 - RIGHT_REAR * speed)
    }
}
function testMotors () {
    testMotor(1)
    testMotor(2)
    testMotor(3)
    testMotor(4)
}
// a command looks like M,F7,R3 (forward at 7 of 9, right at 3 of 9); S stops; T tests the motors one by one; I reports what this is
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    receivedString = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    lastCommand = control.millis()
    command = receivedString.substr(0, 1)
    if (command == "M" && !testing) {
        y_dir = receivedString.substr(2, 1)
        y_level = parseFloat(receivedString.substr(3, 1))
        x_dir = receivedString.substr(5, 1)
        x_level = parseFloat(receivedString.substr(6, 1))
        drive()
    } else if (command == "S" && !testing) {
        stop()
    } else if (command == "T" && !testing) {
        // the forever loop below runs the test, so this handler answers the commands that come meanwhile
        testing = true
    } else if (command == "I") {
        // the phone joystick asks what this is: model 8 (a Wukong tank with four servos) and this program's release
        control.raiseEvent(9102, 8)
        control.raiseEvent(9103, 35)
    }
    // tell the phone joystick this command is done, so it sends the next one at once
    control.raiseEvent(9100, 1)
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
let point_y = 0
let point_x = 0
let angle = 0
let spin = 0
let curve = 0
let speed = 0
let x_level = 0
let y_level = 0
let lastCommand = 0
let testing = false
let command = ""
let x_dir = ""
let y_dir = ""
let receivedString = ""
// LEFT_FRONT, LEFT_REAR, RIGHT_FRONT, RIGHT_REAR: 1 for a servo mounted with its output outwards (as on the mecanum
// racer), -1 for one turned the other way round (its track runs backwards in its motor test)
let LEFT_FRONT = -1
let LEFT_REAR = -1
let RIGHT_FRONT = -1
let RIGHT_REAR = -1
// SPEED: full speed; SLOW: speed at the slightest push (tracks need more than wheels: raise it if they stall)
let SPEED = 100
let SLOW = 40
// TEST: speed in the motor test
let TEST = 60
// CURVE: speed of the inner track in the sharpest curve (0 = turn on the spot, 100 = straight on)
let CURVE = 40
bluetooth.startUartService()
stop()
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
