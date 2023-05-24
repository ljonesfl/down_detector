import time
from config import Config
from network import Network
from notify import Notify

URL = "www.google.com"


class DownDetector:
    CONFIG_FILE = "down_detector.yaml.example"

    def __init__(self):
        self.config = Config(self.CONFIG_FILE, self)
        self.notify = Notify(self.config)
        self.network = Network(self.config, self.notify)

        self.current_connection_state = None
        self.current_latency_state = None

        self.timeout = self.config.DOWN_TIMEOUT

    def detect(self, url):
        state = self.network.is_connected(url)

        if state != self.current_connection_state:
            if state:
                self.notify.active()
                self.timeout = self.config.ACTIVE_TIMEOUT
            else:
                self.notify.down()
                self.timeout = self.config.DOWN_TIMEOUT

            self.current_connection_state = state

        state = self.network.is_latency_high(url)

        if state != self.current_latency_state:
            if state:
                self.notify.speed_slow()
            else:
                self.notify.speed_normal()

            self.current_latency_state = state

        time.sleep(self.timeout)
        self.config.refresh()


if __name__ == '__main__':
    dd = DownDetector()

    while True:
        dd.detect(URL)
