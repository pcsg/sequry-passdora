import threading
import time

import RPi.GPIO as GPIO


class Buzzer:
    __instance = None  # type: Buzzer

    # Which GPIO pin is the button connected to?
    GPIO_PIN = 5

    _PWM = None

    Lock = threading.Lock()  # type: Lock

    def __init__(self) -> None:
        if Buzzer.__instance is not None:
            raise Exception("Button is a Singleton, use get_instance method to get an instance!")

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.OUT)
        self._PWM = GPIO.PWM(self.GPIO_PIN, 1000)

        Buzzer.__instance = self

    @staticmethod
    def get_instance() -> 'Buzzer':
        """
        Returns an instance of this class (Singleton)
        """
        if Buzzer.__instance is None:
            Buzzer()
        return Buzzer.__instance

    def on(self):
        """
        Turns the buzzer on
        """
        self._PWM.start(10)

    def off(self):
        """
        Turns the buzzer off
        """
        self._PWM.stop()

    def beep(self):
        """
        Lets the buzzer beep
        """
        self.on()
        time.sleep(0.05)
        self.off()

    def cleanup(self):
        """
        Cleans up all instantiated objects, especially GPIO
        """
        GPIO.cleanup()

    def __del__(self):
        self.cleanup()
