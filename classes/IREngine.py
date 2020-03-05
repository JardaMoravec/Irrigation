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
            elif key == 't':
                title = 'Trafo'
            elif key == 'f1':
                title = 'Filtr 1'
            elif key == 'f2':
                title = 'Filtr 2'
            else:
                title = "Sekce " + str(key)
            self.switches[key] = IRSwitch(title, pin, self.logger)

    def start(self):
        # turn on transformer
        self.logger.log("Trafo start")
        self.switches['t'].start()

        time.sleep(1)

        # turn on main switch
        self.logger.log("Hlavní ventil start")
        self.switches['m'].start()

    def clean_filters(self):
        # main is on?
        if self.main_switch_is_on() is False:
            self.start()

        # turn on first switch and stop
        self.logger.log("Clean filter 1")
        self.switches['f1'].start()
        time.sleep(self.filter_runtime)
        self.switches['f2'].stop()

        time.sleep(5)

        # turn on second switch and stop
        self.logger.log("Clean filter 2")
        self.switches['f2'].start()
        time.sleep(self.filter_runtime)
        self.switches['f2'].stop()

        time.sleep(2)

    def stop(self):
        # turn off main switch
        self.logger.log("Hlavní ventil stop")
        self.switches['m'].stop()

        time.sleep(1)

        # turn off transformer
        self.logger.log("Trafo stop")
        self.switches['f'].stop()

    def turn_on_switch(self, key):
        # main is on?
        if self.main_switch_is_on() is False:
            self.start()

        # filter is on?
        if self.filters_is_on():
            self.logger.log("Beži filtry, nelze zapnout zavlažovaní")
            return

        try:
            # turn off all other switches
            for i in range(1, 5):
                if key != i:
                    self.switches[i].stop()
            # turn on actual switch
            if self.switches[key].is_on is False:
                self.switches[key].start()
        except KeyError:
            self.logger.log("Spínač [{}] není definovaný".format(key))

    def turn_off(self):
        # if main is off, do nothing
        if self.main_switch_is_on() is False:
            return

        # turn all switches
        for i in range(1, 5):
            self.switches[i].stop()

        time.sleep(2)

        # clean filters
        self.clean_filters()

        # turn off main switch
        self.stop()

    def is_on(self):
        return self.filters_is_on() or self.main_switch_is_on() or self.switches_is_on()

    def main_switch_is_on(self):
        return self.switches['m'].is_on is True

    def switches_is_on(self):
        return self.switches[1].is_on is True or self.switches[2].is_on is True or self.switches[3].is_on is True or self.switches[4].is_on is True

    def filters_is_on(self):
        return self.switches['f1'].is_on is True or self.switches['f2'].is_on is True
