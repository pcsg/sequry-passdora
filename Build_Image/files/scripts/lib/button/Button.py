import threading
import time

import RPi.GPIO as GPIO

from typing import List
from lib.button.ButtonObserver import ButtonObserver


class Button:
    __instance = None  # type: Button

    # How many seconds to sleep between while iterations?
    SLEEP_TIME = 0.1

    # Which GPIO pin is the button connected to?
    GPIO_PIN = 18

    def __init__(self):
        if Button.__instance is not None:
            raise Exception("Button is a Singleton, use get_instance method to get an instance!")

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.observers_release = []  # type: List[ButtonObserver]
        self.observers_press = []  # type: List[ButtonObserver]
        self.observers_hold = []  # type: List[ButtonObserver]

        Button.__instance = self

        threading.Thread(target=self.__listening_function).start()

    @staticmethod
    def get_instance():
        """
        Returns an instance of this class (Singleton)

        :rtype: Button
        """
        if Button.__instance is None:
            Button()
        return Button.__instance

    def __listening_function(self):
        # Run forever
        while True:
            hold_time = 0

            # Check if the button is currently pressed
            if not GPIO.input(self.GPIO_PIN):

                # Time the button press starts
                button_press_start_time = time.time()
                self.notify_press_observers()

                # While the button is held not longer than the button has to be held...
                while not GPIO.input(self.GPIO_PIN):
                    # Increase the time the button is held
                    hold_time = time.time() - button_press_start_time
                    self.notify_hold_observers(hold_time)
                    time.sleep(self.SLEEP_TIME)

                # If the button was released...
                self.notify_release_observers(hold_time)

            time.sleep(self.SLEEP_TIME)

    def add_release_listener(self, observer: ButtonObserver):
        self.observers_release.append(observer)

    def remove_release_listener(self, observer: ButtonObserver):
        self.observers_release.remove(observer)

    def notify_release_observers(self, seconds):
        for observer in self.observers_release:
            observer.on_button_released(seconds)

    def add_press_listener(self, observer: ButtonObserver):
        self.observers_press.append(observer)

    def remove_press_listener(self, observer: ButtonObserver):
        self.observers_press.remove(observer)

    def notify_press_observers(self):
        for observer in self.observers_press:
            observer.on_button_pressed()

    def add_hold_listener(self, observer: ButtonObserver):
        self.observers_hold.append(observer)

    def remove_hold_listener(self, observer: ButtonObserver):
        self.observers_hold.remove(observer)

    def notify_hold_observers(self, seconds):
        for observer in self.observers_hold:
            observer.on_button_held(seconds)
