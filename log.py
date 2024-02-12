import csv
import datetime


class Log:

    def __init__(self, config):
        self.config = config

    def write(self, message, *args):
        if self.config.LOG_ENABLED is False:
            return

        with open( self.config.LOG_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            now = datetime.datetime.now()
            formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
            row = [formatted_now, message]
            row.extend(args)
            writer.writerow(row)

    def started(self):
        self.write('started')

    def active(self):
        if self.config.NOTIFY_ACTIVE_LOG:
            self.write('internet active')

    def down(self):
        if self.config.NOTIFY_ACTIVE_LOG:
            self.write('internet down')

    def latency(self, latency):
        if self.config.NOTIFY_LATENCY_LOG:
            self.write('latency warning', latency)

    def speed_slow(self):
        if self.config.NOTIFY_LATENCY_LOG:
            self.write('speed slow')

    def speed_normal(self):
        if self.config.NOTIFY_LATENCY_LOG:
            self.write('speed normal')
