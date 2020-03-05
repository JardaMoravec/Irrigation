import time
from classes.IRSwitch import IRSwitch


class IREngine:

    def __init__(self):
        self.pins = {'m': 16, 't': 27, 1: 18, 2: 23, 3: 24, 4: 12, 'f1': 17, 'f2': 21}
        self.switches = {}
        self.log_file = "./data/irrigation.log"
        self.filter_runtime = 60  # second

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
            self.switches[key] = IRSwitch(title, pin, self.log_file)

    def start(self):
        # zapnout trafo
        print("Trafo start")
        self.switches['t'].start()

        time.sleep(1)

        # zapnout hlavni ventil
        print("Hlavní ventil start")
        self.switches['m'].start()

    def clean_filters(self):
        print("Clean filter 1")
        self.switches['f1'].start()
        time.sleep(self.filter_runtime)
        self.switches['f2'].stop()

        time.sleep(5)

        print("Clean filter 2")
        self.switches['f2'].start()
        time.sleep(self.filter_runtime)
        self.switches['f2'].stop()

        time.sleep(2)

    def stop(self):
        # vypnout hlavni ventil
        print("Hlavní ventil stop")
        self.switches['m'].stop()

        time.sleep(1)

        # vypnout trafo
        print("Trafo stop")
        self.switches['f'].stop()
