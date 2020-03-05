import datetime


class IRLogger:

    def __init__(self, log_file=None, std_output=False):
        self.buffer = []
        self.std_output = std_output

        if log_file is not None:
            self.file = open(log_file, 'a')

    def log(self, message: str):
        self.buffer.append(message)

        if self.file is not None:
            self.file.write(str(datetime.datetime.now()) + ' - ' + message + "\n")

        if self.std_output is True:
            print(message)

    def close(self):
        if self.file is not None:
            self.file.close()
