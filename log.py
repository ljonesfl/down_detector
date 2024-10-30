import csv
import datetime

from config import Config


class Log:

    def __init__( self, config: Config ):
        self.config = config

    def write( self, message: str, *args) -> None:
        if self.config.LOG_ENABLED is False:
            return

        with open( self.config.LOG_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            now = datetime.datetime.now()
            formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
            row = [formatted_now, message]
            row.extend(args)
            writer.writerow(row)

    def started( self ) -> None:
        self.write('started', 0 )

    def active( self ) -> None:
        if self.config.NOTIFY_ACTIVE_LOG:
            self.write('internet active', 0 )

    def down( self ) -> None:
        if self.config.NOTIFY_ACTIVE_LOG:
            self.write('internet down', 0 )

    def latency( self, latency ) -> None:
        if self.config.NOTIFY_LATENCY_LOG:
            self.write('latency warning', latency)

    def speed_slow( self ) -> None:
        if self.config.NOTIFY_LATENCY_LOG:
            self.write('speed slow', 0 )

    def speed_normal( self ) -> None:
        if self.config.NOTIFY_LATENCY_LOG:
            self.write('speed normal', 0)
