import socket
import ping3

from config import Config
from notify import Notify
from log import Log


class Network:

    def __init__(self, config: Config, notify: Notify, log: Log):
        self.config = config
        self.notify = notify
        self.log = log
        self.current_latency_count = 0

    @staticmethod
    def is_connected( url: str ) -> bool:
        try:
            socket.gethostbyname( url )
            return True
        except Exception as error:
            print( error )
            return False

    def is_latency_high( self, url: str, current_state: bool ) -> bool:
        latency = ping3.ping( url, timeout=self.config.RESPONSE_TIMEOUT )
        if not latency or latency is None or latency > self.config.LATENCY_MIN:
            self.current_latency_count += 1

            self.notify.latency()
            self.log.latency( latency )

            if not latency:
                print( "*** Latency: timeout" )
            elif latency is None:
                print( "*** Latency: host unreachable" )
            else:
                print( f"*** Latency {latency*1000} is too high" )

            if self.current_latency_count >= self.config.LATENCY_COUNT:
                return True

            return current_state
        else:
            print( f"Latency: {latency*1000}ms" )
            self.current_latency_count = 0
            return False
