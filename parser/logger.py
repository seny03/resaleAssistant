import logging.config
import os


class Logger:
    def __init__(self):
        logging.config.fileConfig("logger.ini")
        self.log = logging.getLogger('parser')

    def clear(self):
        for i in os.listdir("../log/"):
            if ".log" not in i:
                continue
            with open(i, 'w') as file:
                file.truncate(0)
