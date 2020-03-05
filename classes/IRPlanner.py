import datetime
from classes.IRSwitch import IRSwitch
from classes.IREngine import IREngine


class IRPlanner:
    def __init__(self, engine: IREngine):
        self.engine = engine
        self.run_list = []
        self.load_settings()

    def load_settings(self):
        f = open("./data/irrigation.conf", 'r')

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
                    self.run_list.append(item)

                except ValueError as e:
                    self.engine.logger.log("Špatný konfigurák.")
        f.close()

    def is_it_time(self):
        t = datetime.datetime.now().time().replace(microsecond=0, second=0)

        for item in self.run_list:
            if t == item['time']:
                return item
        return False
