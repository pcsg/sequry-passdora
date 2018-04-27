import threading
import time

import RPi.GPIO as GPIO

from typing import List, Callable

from lib.util.ThreadPoolExecutor import ThreadPoolExecutor


class Button:
    __instance = None  # type: Button

    # How many seconds to sleep between while iterations?
    SLEEP_TIME = 0.1

    # Which GPIO pin is the button connected to?
    GPIO_PIN = 15

    __destroy = False

    executor = ThreadPoolExecutor.get_instance()

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
        while not self.__destroy:
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

    def add_release_listener(self, func: Callable[[float], None]) -> None:
        """
        Adds an EventListener-function which is called when the button is released.
        When the button is released the given function is called.

        :param func: a function that is called when the event occurs
        :return: Nothing
        """
        self.observers_release_functions.append(func)

    def remove_release_listener(self, func: Callable[[float], None]) -> None:
        """
        Removes an EventListener-function for the button release event.

        :param func: the function to remove
        :return: Nothing
        """
        self.observers_release_functions.remove(func)

    def notify_release_observers(self, seconds: float) -> None:
        """
        Calls all functions listening for the button release event.
        The given time after the button was released is passed to the functions as the first argument.

        :param seconds: After how many seconds was the button released
        :return: Nothing
        """
        for func in self.observers_release_functions:
            self.executor.submit(func, seconds)

    def is_release_observer_registered(self, func: Callable[[float], None]) -> bool:
        return func in self.observers_release_functions

    def add_press_listener(self, func: Callable[[], None]) -> None:
        """
        Adds an EventListener-function which is called when the button is initially pressed.

        :param func: a function that is called when the event occurs
        :return: Nothing
        """
        self.observers_press_functions.append(func)

    def remove_press_listener(self, func: Callable[[], None]) -> None:
        """
        Removes an EventListener-function for the button press event.

        :param func: the function to remove
        :return: Nothing
        """
        self.observers_press_functions.remove(func)

    def notify_press_observers(self) -> None:
        """
        Calls all functions listening for the button press event.

        :return: Nothing
        """
        for func in self.observers_press_functions:
            self.executor.submit(func)

    def is_press_observer_registered(self, func: Callable[[], None]) -> bool:
        return func in self.observers_press_functions

    def add_hold_listener(self, func: Callable[[float], None]) -> None:
        """
        Adds an EventListener-function which is called in intervals until the button is released.

        :param func: a function that is called when the event occurs
        :return: Nothing
        """
        self.observers_hold_functions.append(func)

    def remove_hold_listener(self, func: Callable[[float], None]) -> None:
        """
        Removes an EventListener-function for the button hold event.

        :param func: the function to remove
        :return: Nothing
        """
        self.observers_hold_functions.remove(func)

    def notify_hold_observers(self, seconds: float) -> None:
        """
        Calls all functions listening for the button hold event.
        The time for how long the button is currently held is passed to the functions as the first argument.

        :param seconds: The amount of seconds the button is currently held.
        :return: Nothing
        """
        for func in self.observers_hold_functions:
            self.executor.submit(func, seconds)

    def is_hold_observer_registered(self, func: Callable[[float], None]) -> bool:
        return func in self.observers_hold_functions

    def __del__(self):
        self.__destroy = True
        self.executor.shutdown()
