import time
from classes.IRSwitch import IRSwitch
from classes.IRLogger import IRLogger


class IREngine:

    def __init__(self, logger: IRLogger):
        self.pins = {'m': 16, 't': 27, 1: 18, 2: 23, 3: 24, 4: 12, 'f1': 17, 'f2': 21}
        self.switches = {}
        self.logger = logger
        self.filter_runtime = 60  # second
        self.running_switch = None

        self.init_switches()

    def init_switches(self):
        for key, pin in self.pins.items():
            if key == 'm':
                title = 'Hlavní ventil'
                revers_mode = False
            elif key == 't':
                title = 'Trafo'
                revers_mode = True
            elif key == 'f1':
                title = 'Čištění Filtru 1'
                revers_mode = False
            elif key == 'f2':
                title = 'Čištění Filtru 2'
                revers_mode = False
            else:
                title = "Sekce " + str(key)
                revers_mode = False
            self.switches[key] = IRSwitch(title, pin, self.logger, revers_mode)

    def start(self):
        if self.main_switch_is_on() is False:
            # turn on transformer
            self.switches['t'].start()

            time.sleep(1)

            # turn on main switch
            self.switches['m'].start()

    def stop(self):
        if self.main_switch_is_on() is True:
            # turn off main switch
            self.switches['m'].stop()

            time.sleep(1)

            # turn off transformer
            self.switches['t'].stop()

    def clean_filters(self):
        if self.filters_is_on() is True:
            return

        # main is on?
        if self.main_switch_is_on() is False:
            self.start()
        else:
            # turn all switches
            for i in range(1, 5):
                self.switches[i].stop()

        # turn on first switch and stop
        self.switches['f1'].start()
        time.sleep(self.filter_runtime)
        self.switches['f1'].stop()

        time.sleep(5)

        # turn on second switch and stop
        self.switches['f2'].start()
        time.sleep(self.filter_runtime)
        self.switches['f2'].stop()

        time.sleep(2)

    def turn_on_switch(self, key):
        # main is on?
        if self.main_switch_is_on() is False:
            self.start()

        # filter is on?
        if self.filters_is_on():
            self.logger.log("Beži filtry, nelze zapnout zavlažovaní")
            return

        try:
            # turn off all other switches and filters
            self.switches['f1'].stop()
            self.switches['f2'].stop()
            for i in range(1, 5):
                if key != i:
                    self.switches[i].stop()
            # turn on actual switch
            if self.switches[key].is_on is False:
                self.switches[key].start()
        except KeyError:
            self.logger.log("Spínač [{}] není definovaný".format(key))

    def turn_off(self, clean_filters: bool):
        # if main is off, do nothing
        if self.main_switch_is_on() is False:
            return

        # turn all switches
        for i in range(1, 5):
            self.switches[i].stop()

        time.sleep(2)

        # clean filters
        if clean_filters is True:
            self.clean_filters()

        # turn off main switch
        self.stop()

    def start_and_stop_switch(self, key, seconds: int):
        # main is on?
        if self.main_switch_is_on() is False:
            self.start()

        try:
            # turn off all other switches and filters
            self.switches['f1'].stop()
            self.switches['f2'].stop()
            for i in range(1, 5):
                if key != i:
                    self.switches[i].stop()
            # turn on actual switch
            if self.switches[key].is_on is False:
                self.switches[key].start_and_stop(seconds)
        except KeyError:
            self.logger.log("Spínač [{}] není definovaný".format(key))

    def is_on(self):
        return self.filters_is_on() or self.main_switch_is_on() or self.switches_is_on()

    def main_switch_is_on(self):
        return self.switches['m'].is_on is True

    def switches_is_on(self):
        return self.switches[1].is_on is True or self.switches[2].is_on is True or self.switches[3].is_on is True or self.switches[4].is_on is True

    def filters_is_on(self):
        return self.switches['f1'].is_on is True or self.switches['f2'].is_on is True
