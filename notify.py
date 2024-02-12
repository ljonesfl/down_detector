from sound import Sound
from log import Log
import time


class Notify:
    def __init__(self, config):
        self.config = config

        self.sound = Sound(self.config)
        self.outages_total = 0
        self.outage_current_time = 0
        self.outages_total_time = 0

        self.active_total_time = 0
        self.active_current_time = 0

        self.sound.create_audio_files()

    def active(self):
        print("Internet is active")

        self.active_current_time = time.time()

        if self.outage_current_time:
            current_outage_seconds = time.time() - self.outage_current_time
            self.outages_total_time += current_outage_seconds
            print(f"Down for {current_outage_seconds}s")
            outage_average = self.outages_total_time / self.outages_total
            print(f"Total outages: {self.outages_total}, Average downtime: {outage_average}s")

        if self.config.NOTIFY_ACTIVE_VOICE:
            self.sound.play(self.config.ACTIVE_FILE)

    def down(self):
        print("Internet is down")

        self.outages_total += 1

        self.outage_current_time = time.time()

        if self.active_current_time:
            current_active_seconds = time.time() - self.active_current_time
            self.active_total_time += current_active_seconds
            print(f"Up for {current_active_seconds}s")
            active_average = self.active_total_time / self.outages_total
            print(f"Total uptime: {self.active_total_time}s, Average uptime: {active_average}s")

        if self.config.NOTIFY_ACTIVE_VOICE:
            self.sound.play(self.config.DOWN_FILE)

    def speed_slow(self):
        print("Internet is slow")

        if self.config.NOTIFY_LATENCY_VOICE:
            self.sound.play(self.config.SLOW_FILE)

    def speed_normal(self):
        print("Internet speed is normal")

        if self.config.NOTIFY_LATENCY_VOICE:
            self.sound.play(self.config.NORMAL_FILE)

    def latency(self):
        if self.config.NOTIFY_LATENCY_BEEP:
            self.sound.blip()
