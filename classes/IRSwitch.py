import RPi.GPIO as gpio
import time

from classes.IRLogger import IRLogger


class IRSwitch:

    def __init__(self, name: str, pin: int, logger: IRLogger):
        self.name = name
        self.pin = pin

        gpio.cleanup(pin)
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)

        self.logger = logger

        self.is_on = False

    def start(self):
        if self.is_on is False:
            self.is_on = True
            gpio.output(self.pin, gpio.HIGH)
            self.logger.log("Start " + self.name)

    def stop(self):
        if self.is_on is True:
            self.is_on = False
            gpio.output(self.pin, gpio.LOW)
            self.logger.log("Stop " + self.name)

    def start_and_stop(self, seconds: int):
        if self.is_on is False:
            gpio.output(self.pin, gpio.HIGH)
            self.logger.log("Start " + self.name)

            time.sleep(seconds)

            gpio.output(self.pin, gpio.LOW)
            self.logger.log("Stop " + self.name)

    def clean(self):
        gpio.cleanup(self.pin)   
