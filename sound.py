import platform
import os
from gtts import gTTS


class Sound:

    def __init__(self, config):
        self.config = config

    def create_audio_files(self):
        if not os.path.exists(self.config.ACTIVE_FILE):
            self.create_mp3(self.config.ACTIVE_TEXT, self.config.ACTIVE_FILE)

        if not os.path.exists(self.config.DOWN_FILE):
            self.create_mp3(self.config.DOWN_TEXT, self.config.DOWN_FILE)

        if not os.path.exists(self.config.SLOW_FILE):
            self.create_mp3(self.config.LATENCY_HIGH_TEXT, self.config.SLOW_FILE)

        if not os.path.exists(self.config.NORMAL_FILE):
            self.create_mp3(self.config.LATENCY_NORMAL_TEXT, self.config.NORMAL_FILE)

    @staticmethod
    def create_mp3(text, file):
        print(f"Creating {file}")
        tts = gTTS(text)
        tts.save(file)

    def play(self, file):
        if not self.config.is_in_schedule():
            return

        print(f"Playing {file}")
        if platform.system() == "Windows":
            os.system(f"start {file}")
        elif platform.system() == "Darwin":
            os.system(f"afplay {file}")
        else:
            os.system(f"mpg123 {file}")

    def blip(self):
        if not self.config.is_in_schedule():
            return

        print("Blip")
        print('\a')
