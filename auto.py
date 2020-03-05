#!/usr/bin/python3

from IR_Switch import IR_Switch 
from func import laod_settings, is_it_time, start, stop, pins, log_file, clean_filters, filter_runtime
import time
import datetime

runlist = laod_settings()

while True:
    runline = is_it_time(runlist)
    print(runline)

    if runline is not False:
        # zapnout trafo
        print("Trafo start")
        tr = IR_Switch("Trafo", pins['m'], log_file)
        tr.start()

        time.sleep(1)

        # zapnout hlavni ventil
        print("Hlavní ventil start")
        mv = IR_Switch("Hlavní ventil", pins['m'], log_file)
        mv.start()

        time.sleep(1)

        # zapnout sekce
        for section in list(range(1, 5)):
            print("Sekce " + str(section) + ' start')
            s = IR_Switch("Sekce " + str(section), pins[section], log_file)
            s.start()

            time.sleep(int(runline[section]))

            print("Sekce " + str(section) + ' stop')
            s = IR_Switch("Sekce " + str(section), pins[section], log_file)
            s.stop()
            s.clean() 

            time.sleep(2)

        # procistit filtry
        print("Clean filter 1")
        f1 = IR_Switch("Filtr 1", pins['f1'], log_file)
        f1.start()
        time.sleep(filter_runtime)
        f1.stop()

        time.sleep(5)
        
        print("Clean filter 2")
        f2 = IR_Switch("Filtr 2", pins['f2'], log_file)
        f2.start()
        time.sleep(filter_runtime)
        f2.stop()

        time.sleep(2)

        # vypnout hlavni ventil
        print("Hlavní ventil stop")
        mv.stop()

        time.sleep(1)

        # vypnout trafo
        print("Trafo stop")
        tr.stop()
    else:
        time.sleep(59)

