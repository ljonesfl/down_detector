import platform
import os
import simpleaudio
import numpy
from gtts import gTTS


class Sound:

    def __init__(self, config):
        self.config = config

        self.sound_blip = self.create_blip()

    @staticmethod
    def create_blip():
        duration = 0.075  # Duration of the blip in seconds
        frequency = 2000  # Frequency of the blip in Hz
        volume = 0.125  # Volume adjustment factor (0.0 to 1.0)

        # Generate the blip sound
        t = numpy.linspace(0, duration, int(duration * 44100), False)  # Time array
        blip = numpy.sin(frequency * 2 * numpy.pi * t)  # Generate the blip waveform

        # Scale the blip sound to adjust the volume
        blip_adjusted = blip * volume

        # Scale the adjusted blip sound to 16-bit integers (-32768 to 32767)
        return numpy.int16(blip_adjusted * 32767)

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

        if platform.system() == "Windows":
            os.system(f"start {file}")
        elif platform.system() == "Darwin":
            os.system(f"afplay {file}")
        else:
            os.system(f"mpg123 {file}")

    def blip(self):
        if not self.config.is_in_schedule():
            return

        # Play the blip sound
        play_obj = simpleaudio.play_buffer(self.sound_blip, 1, 2, 44100)

        # Wait for the blip sound to finish playing
        play_obj.wait_done()
