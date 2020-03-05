import RPi.GPIO as gpio
import time
import datetime

class IR_Switch:


    def __init__ (self, name: str, pin: int, logfile: str):
        self.name = name
        self.pin = pin

        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)

        self.log = open(logfile, 'a')        


    def start(self):
        gpio.output(self.pin, gpio.HIGH)
        self.log.write(str(datetime.datetime.now()) + " start " + self.name + "\n")


    def stop(self):
        gpio.output(self.pin, gpio.LOW)
        self.log.write(str(datetime.datetime.now()) + " stop " + self.name + "\n")


    def start_stop(self, seconds:int):
        gpio.output(self.pin, gpio.HIGH)
        self.log.write(str(datetime.datetime.now()) + " start " + self.name + "\n")
        time.sleep(seconds)
        gpio.output(self.pin, gpio.LOW)
        self.log.write(str(datetime.datetime.now()) + " stop " + self.name + "\n")


    def clean(self):
        gpio.cleanup(self.pin)   

