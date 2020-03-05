import time
import datetime
from classes.IR_Switch import IR_Switch

pins = {'m': 16, 't': 27, 1: 18, 2: 23, 3: 24, 4: 12, 'f1': 17, 'f2': 21 }
log_file = "/home/pi/irrigation/data/irrigation.log"
filter_runtime = 60 # second

def laod_settings():
    f = open("/home/pi/irrigation/data/irrigation.conf", 'r')
    
    runlist = []

    for line in f:
        if line != '' and line is not None:
            try:
                line = line.replace("\n", "")
                data = line.split(' ')

                start_time = datetime.datetime.strptime(data[0], '%H:%M').time()
                item = {
                    'time': start_time,
                    1: int(data[1]),
                    2: int(data[2]),
                    3: int(data[3]),
                    4: int(data[4]), 
                }
                runlist.append(item)
      
            except ValueError as e:
                print(e)      
    f.close()
    return runlist


def is_it_time(runlist):
    t = datetime.datetime.now().time().replace(microsecond=0, second=0)

    for item in runlist:
        if t == item['time']:
            return item
    return False

def start():
    # zapnout trafo
    print("Trafo start")
    tr = IR_Switch("Trafo", pins['t'], log_file)
    tr.start()

    time.sleep(1)

    # zapnout hlavni ventil
    print("Hlavní ventil start")
    mv = IR_Switch("Hlavní ventil", pins['m'], log_file)
    mv.start() 

def clean_filters():
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

def stop():
    # vypnout hlavni ventil
    print("Hlavní ventil stop")
    mv = IR_Switch("Hlavní ventil", pins['m'], log_file)
    mv.stop()

    time.sleep(1)

    # vypnout trafo
    print("Trafo stop")
    tr = IR_Switch("Trafo", pins['t'], log_file)
    tr.stop()

