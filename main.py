#!/usr/bin/python3

import time
import datetime
import RPi.GPIO as gpio
from pad4pi import rpi_gpio
from classes.IR_Switch import IR_Switch
from classes.func import start, stop, pins, log_file, clean_filters

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

KEYPAD = [
        [1,2,3],
        [4,5,6],
        [7,8,9],
        ["*",0,"#"]
]

ROW_PINS = [25,5,6,13] # BCM numbering
COL_PINS = [19,26,20] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

run = False
run_section = None
run_filters = False

def keyPressed(key):
    global run, run_section, run_filters
    
    if run_filters is False:
        if key == 1 or key == 2 or key == 3 or key == 4:
            # zapnou privod        
            if run is False:                                
                start()
                run = True
            # vypnout bezici
            if run_section is not None:
                print("Sekce " + str(run_section.name) + ' stop')
                run_section.stop()
                run_section.clean() 
                run_section = None    
            
            # spustit novy
            print("Sekce " + str(key) + ' start')
            run_section = IR_Switch("Sekce " + str(key), pins[key], log_file)
            run_section.start()

        elif key == '#': # vypnout
            if run is True and run_section is not None:
                print("Sekce " + str(run_section.name) + ' stop')
                run_section.stop()
                run_section.clean()
                run_section = None      
                
                time.sleep(2)
                # vycistit filtry
                run_filters = True
                clean_filters()
                run_filters = False
                #vypnout
                stop()
                run = False

        elif key == '*': # procistit filtry
            # zapnou privod            
            if run is False:                                
                start()
                run = True

            # vypnout bezici
            if run_section is not None:
                print("Sekce " + str(run_section.name) + ' stop')
                run_section.stop()
                run_section.clean()  
                run_section = None
        
            # vycistit filtry
            run_filters = True
            clean_filters()
            run_filters = False
            #vypnout
            stop()
            run = False
        else:
            print("Žádná funkce")
            
            

keypad.registerKeyPressHandler(keyPressed)

try:
    while(True):
        time.sleep(0.2)
except (KeyboardInterrupt,SystemExit, Exception):
    keypad.cleanup()
    gpio.cleanup() 

