import time
from config import Config
from network import Network
from notify import Notify
from log import Log

URL = "www.google.com"


class DownDetector:
    CONFIG_FILE = "down_detector.yaml"

    def __init__( self ):
        self.config: Config = Config( self.CONFIG_FILE )
        self.notify: Notify = Notify( self.config )
        self.log: Log = Log( self.config )
        self.network: Network = Network( self.config, self.notify, self.log )

        self.current_connection_state = None
        self.current_latency_state = None

        self.timeout = self.config.DOWN_TIMEOUT

        self.log.started()

    def detect( self, url: str ) -> None:
        state = self.network.is_connected( url )

        if state != self.current_connection_state:
            if state:
                self.notify.active()
                self.log.active()
                self.timeout = self.config.ACTIVE_TIMEOUT
            else:
                self.notify.down()
                self.log.down()
                self.timeout = self.config.DOWN_TIMEOUT

            self.current_connection_state = state

        state = self.network.is_latency_high( url, self.current_latency_state )

        if self.current_connection_state and state != self.current_latency_state:
            if state:
                # Only notify of slow connections if the connection is active
                if self.current_connection_state:
                    self.notify.speed_slow()
                    self.log.speed_slow()
            else:
                self.notify.speed_normal()
                self.log.speed_normal()

            self.current_latency_state = state

        time.sleep( self.timeout )
        self.config.refresh()


def main():
    dd = DownDetector()

    while True:
        dd.detect(URL)

if __name__ == '__main__':
    main()
