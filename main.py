#!/usr/bin/python3

import time
import RPi.GPIO as gpio
from pad4pi import rpi_gpio
from classes.IREngine import IREngine
from classes.IRLogger import IRLogger
from classes.IRPlanner import IRPlanner

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [25, 5, 6, 13]   # BCM numbering
COL_PINS = [19, 26, 20]   # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

logger = IRLogger("./data/irrigation.log", True)

engine = IREngine(logger)
planner = IRPlanner(engine)


def key_pressed(key):
    global engine
    
    if key == 1 or key == 2 or key == 3 or key == 4:
        # turn on
        engine.turn_on_switch(key)

    elif key == '#':
        # turn off
        engine.turn_off()

    elif key == '*':
        # clean filters
        engine.clean_filters()
        engine.turn_off()

    else:
        logger.log("Žádná funkce")
            

keypad.registerKeyPressHandler(key_pressed)

try:
    while True:
        time.sleep(0.2)
except (KeyboardInterrupt, SystemExit, Exception):
    keypad.cleanup()
    gpio.cleanup() 
