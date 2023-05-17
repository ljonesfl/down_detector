from gtts import gTTS
import os
import time
import socket
import platform
import yaml
from datetime import datetime, time as dttime


URL = "www.google.com"


class DownDetector:
    SCHEDULE_START = dttime(6, 30)
    SCHEDULE_END = dttime(22, 0)

    ACTIVE_TIMEOUT = 10
    DOWN_TIMEOUT = 5
    RESPONSE_TIMEOUT = 5

    ACTIVE_TEXT = "the internet connection has been restored"
    DOWN_TEXT = "the internet is currently unreachable"

    ACTIVE_FILE = "audio/active.mp3"
    DOWN_FILE = "audio/down.mp3"

    def __init__(self):
        self.current_state = None
        self.timeout = self.DOWN_TIMEOUT

        self.outages_total = 0
        self.outage_current_time = 0
        self.outages_total_time = 0

        self.active_total_time = 0
        self.active_current_time = 0

        self.load_config()
        if not os.path.exists(self.ACTIVE_FILE):
            self.create_mp3(self.ACTIVE_TEXT, self.ACTIVE_FILE)

        if not os.path.exists(self.DOWN_FILE):
            self.create_mp3(self.DOWN_TEXT, self.DOWN_FILE)

    def load_config(self):
        try:
            with open("down_detector.yaml", "r") as f:
                config = yaml.safe_load(f)

            self.SCHEDULE_START = dttime(config["schedule"]["start_hour"], 0)
            self.SCHEDULE_END = dttime(config["schedule"]["end_hour"], 0)

            self.ACTIVE_TIMEOUT = config["timeout"]["active"]
            self.DOWN_TIMEOUT = config["timeout"]["down"]
            self.RESPONSE_TIMEOUT = config["timeout"]["response"]

            self.ACTIVE_TEXT = config["phrase"]["active"]
            self.DOWN_TEXT = config["phrase"]["down"]

            self.ACTIVE_FILE = config["audio"]["active"]
            self.DOWN_FILE = config["audio"]["down"]

        except Exception as e:
            print(e)
            print("Failed to load config, using defaults")

    def is_in_schedule(self):
        return self.SCHEDULE_START <= datetime.now().time() <= self.SCHEDULE_END

    @staticmethod
    def create_mp3(text, file):
        print( f"Creating {file}")
        tts = gTTS(text)
        tts.save(file)

    def play(self, file):
        if self.is_in_schedule():
            if platform.system() == "Windows":
                os.system(f"start {file}")
            elif platform.system() == "Darwin":
                os.system(f"afplay {file}")
            else:
                os.system(f"mpg123 {file}")

    @staticmethod
    def is_connected(url):
        try:
            socket.gethostbyname(url)
            return True
        except socket.error as error:
            print(error)
            return False

    def down(self):
        print("Internet is down")

        self.outages_total += 1

        self.outage_current_time = time.time()
        self.timeout = self.DOWN_TIMEOUT
        self.play(self.DOWN_FILE)

        if self.active_current_time:
            current_active_seconds = time.time() - self.active_current_time
            self.active_total_time += current_active_seconds
            print(f"Up for {current_active_seconds}s")
            active_average = self.active_total_time / self.outages_total
            print(f"Total uptime: {self.active_total_time}s, Average uptime: {active_average}s")

    def active(self):
        print("Internet is active")

        self.active_current_time = time.time()
        self.timeout = self.ACTIVE_TIMEOUT
        self.play(self.ACTIVE_FILE)

        if self.outage_current_time:
            current_outage_seconds = time.time() - self.outage_current_time
            self.outages_total_time += current_outage_seconds
            print(f"Down for {current_outage_seconds}s")
            outage_average = self.outages_total_time / self.outages_total
            print(f"Total outages: {self.outages_total}, Average downtime: {outage_average}s")

    def detect(self, url):
        state = self.is_connected(url)

        if state != self.current_state:
            if state:
                self.active()
            else:
                self.down()

            self.current_state = state

        time.sleep(self.timeout)


if __name__ == '__main__':
    dd = DownDetector()

    while True:
        print('.', end='', flush=True)
        dd.detect(URL)
