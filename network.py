import socket
import ping3


class Network:

    def __init__(self, config, notify, log):
        self.config = config
        self.notify = notify
        self.log = log
        self.current_latency_count = 0

    @staticmethod
    def is_connected(url):
        try:
            socket.gethostbyname(url)
            return True
        except socket.error as error:
            print(error)
            return False

    def is_latency_high(self, url):
        latency = ping3.ping(url, timeout=self.config.RESPONSE_TIMEOUT)
        if not latency or latency is None or latency > self.config.LATENCY_MIN:
            self.current_latency_count += 1

            self.notify.latency()
            self.log.latency(latency)

            if not latency:
                print("*** Latency: timeout")
            elif latency is None:
                print("*** Latency: host unreachable")
            else:
                print(f"*** Latency {latency*1000} is too high")

            if self.current_latency_count >= self.config.LATENCY_COUNT:
                return True

            return False
        else:
            print(f"Latency: {latency*1000}ms")
            self.current_latency_count = 0
            return False
