import yaml
import os
from datetime import datetime, time as dttime


class Config:
    SCHEDULE_START = dttime(6, 30)
    SCHEDULE_END = dttime(22, 0)

    ACTIVE_TIMEOUT = 10
    DOWN_TIMEOUT = 5
    RESPONSE_TIMEOUT = 5

    ACTIVE_TEXT = "the internet connection has been restored"
    DOWN_TEXT = "the internet is currently unreachable"
    LATENCY_HIGH_TEXT = "the internet speed is currently slow"
    LATENCY_NORMAL_TEXT = "the internet speed is back to normal"

    ACTIVE_FILE = "audio/active.mp3"
    DOWN_FILE = "audio/down.mp3"
    SLOW_FILE = "audio/slow.mp3"
    NORMAL_FILE = "audio/normal.mp3"

    LATENCY_MIN = 0.200
    LATENCY_COUNT = 3

    NOTIFY_ACTIVE_VOICE = True
    NOTIFY_ACTIVE_LED = False
    NOTIFY_ACTIVE_LOG = False

    NOTIFY_LATENCY_VOICE = True
    NOTIFY_LATENCY_LED = False
    NOTIFY_LATENCY_BEEP = True
    NOTIFY_LATENCY_LOG = True

    LOG_ENABLED = True
    LOG_FILE = "log.csv"
    LOG_ACTIVE = True
    LOG_LATENCY = True

    def __init__(self, file, detector):
        self.CONFIG_FILE = file
        self.config_modified = None
        self.detector = detector
        self.load()

    def load(self):
        self.config_modified = os.path.getmtime(self.CONFIG_FILE)
        try:
            with open(self.CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f)

            self.SCHEDULE_START = dttime(config["schedule"]["start_hour"], 0)
            self.SCHEDULE_END = dttime(config["schedule"]["end_hour"], 0)

            self.ACTIVE_TIMEOUT = config["timeout"]["active"]
            self.DOWN_TIMEOUT = config["timeout"]["down"]
            self.RESPONSE_TIMEOUT = config["timeout"]["response"]

            self.ACTIVE_TEXT = config["phrase"]["active"]
            self.DOWN_TEXT = config["phrase"]["down"]
            self.LATENCY_HIGH_TEXT = config["phrase"]["slow"]
            self.LATENCY_NORMAL_TEXT = config["phrase"]["normal"]

            self.ACTIVE_FILE = config["audio"]["active"]
            self.DOWN_FILE = config["audio"]["down"]
            self.LATENCY_MIN = config["latency"]["min"]
            self.LATENCY_COUNT = config["latency"]["count"]

            self.NOTIFY_ACTIVE_VOICE = config["notify"]["active"]["voice"]
            self.NOTIFY_ACTIVE_LED = config["notify"]["active"]["led"]

            self.NOTIFY_LATENCY_VOICE = config["notify"]["latency"]["voice"]
            self.NOTIFY_LATENCY_LED = config["notify"]["latency"]["led"]
            self.NOTIFY_LATENCY_BEEP = config["notify"]["latency"]["beep"]

            self.LOG_ENABLED = config["log"]["enabled"]
            self.LOG_FILE = config["log"]["file"]
            self.LOG_ACTIVE = config["log"]["active"]
            self.LOG_LATENCY = config["log"]["latency"]

            print("Loaded config file.")

        except Exception as e:
            print( "Error loading log file. Key: " + str(e) )
            print("Failed to load config, using defaults")

    def refresh(self):
        last_modified = os.path.getmtime(self.CONFIG_FILE)
        time_difference = last_modified - self.config_modified

        if time_difference != 0:
            print("Config file changed, reloading...")
            self.load()

    def is_in_schedule(self):
        return self.SCHEDULE_START <= datetime.now().time() <= self.SCHEDULE_END
