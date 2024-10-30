import RPi.GPIO as GPIO


class Hardware:

    def __init__( self ):
        GPIO.setmode(GPIO.BCM)
        self.latency_pin = 23
        self.active_pin = 24

