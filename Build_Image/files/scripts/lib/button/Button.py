import threading
import time

import RPi.GPIO as GPIO

from typing import List, Callable


class Button:
    __instance = None  # type: Button

    # How many seconds to sleep between while iterations?
    SLEEP_TIME = 0.1

    # Which GPIO pin is the button connected to?
    GPIO_PIN = 18

    def __init__(self) -> None:
        if Button.__instance is not None:
            raise Exception("Button is a Singleton, use get_instance method to get an instance!")

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.observers_release_functions = []  # type: List[function]
        self.observers_press_functions = []  # type: List[function]
        self.observers_hold_functions = []  # type: List[function]

        Button.__instance = self

        threading.Thread(target=self.__listening_function).start()

    @staticmethod
    def get_instance() -> 'Button':
        """
        Returns an instance of this class (Singleton)

        :rtype: Button
        """
        if Button.__instance is None:
            Button()
        return Button.__instance

    def __listening_function(self) -> None:
        """
        Infinite loop listening for button interactions.
        Should run in a separate thread to prevent blocking.

        :return: None
        """
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

    def add_release_listener(self, func: Callable[[int], None]) -> None:
        """
        Adds an observer listening for a button release.
        When the button is released the on_button_released() function of the observer is called.

        :param func: a function that is called when the event occurs
        :return: Nothing
        """
        self.observers_release_functions.append(func)

    def remove_release_listener(self, func: Callable[[int], None]) -> None:
        self.observers_release_functions.remove(func)

    def notify_release_observers(self, seconds) -> None:
        for func in self.observers_release_functions:
            func(seconds)

    def add_press_listener(self, func: Callable[[], None]) -> None:
        self.observers_press_functions.append(func)

    def remove_press_listener(self, func: Callable[[], None]) -> None:
        self.observers_press_functions.remove(func)

    def notify_press_observers(self) -> None:
        for func in self.observers_press_functions:
            func()

    def add_hold_listener(self, func: Callable[[int], None]) -> None:
        self.observers_hold_functions.append(func)

    def remove_hold_listener(self, func: Callable[[int], None]) -> None:
        self.observers_hold_functions.remove(func)

    def notify_hold_observers(self, seconds) -> None:
        for func in self.observers_hold_functions:
            func(seconds)
