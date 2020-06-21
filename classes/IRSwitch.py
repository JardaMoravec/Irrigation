import RPi.GPIO as gpio
import time

from classes.IRLogger import IRLogger


class IRSwitch:

    def __init__(self, name: str, pin: int, logger: IRLogger, revers_mode: bool = False):
        self.name = name
        self.pin = pin
        self.revers_mode = revers_mode

        gpio.cleanup(pin)
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)

        self.logger = logger

        self.is_on = None
        self.stop()

    def start(self):
        if self.is_on is False:
            self.is_on = True
            self.gpio_output(gpio.HIGH)
            self.logger.log("Start " + self.name)

    def stop(self):
        if self.is_on is True:
            self.is_on = False
            self.gpio_output(gpio.LOW)
            self.logger.log("Stop " + self.name)

    def start_and_stop(self, seconds: int):
        if self.is_on is False:
            self.gpio_output(gpio.HIGH)
            self.logger.log("Start " + self.name)

            time.sleep(seconds)

            self.gpio_output(gpio.LOW)
            self.logger.log("Stop " + self.name)

    def clean(self):
        gpio.cleanup(self.pin)

    def gpio_output (self, status):
        if self.revers_mode is True:
            if status == gpio.HIGH:
                gpio.output(self.pin, gpio.LOW)
            else:
                gpio.output(self.pin, gpio.HIGH)
        else:
            gpio.output(self.pin, status)