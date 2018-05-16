"""
###################################################################################################
#                                                                                                 #
# Waits for a button press which lasts over a defined duration on GPIO pin 18 (pulling pin down). #
# The script then exits with a success or an error code accordingly.                              #
# Exit codes:                                                                                     #
#     0: button was pressed long enough and in time                                               #
#     3: button wasn't pressed long enough                                                        #
#     4: button wasn't pressed in time                                                            #
#                                                                                                 #
# Author: Jan Wennrich (PCSG)                                                                     #
#                                                                                                 #
###################################################################################################
"""

import RPi.GPIO as GPIO
import sys
import time

from lib.button.Button import Button
from lib.display.Display import Display


class InitSystem:
    # How many seconds has the button to be pressed
    BUTTON_HOLD_TIME = 3

    # After how many seconds should the script timeout?
    SCRIPT_TIMEOUT = 30

    display = Display.get_instance()

    button = Button.get_instance()

    _exit = False

    _exit_code = 0

    def wait_for_authentication(self):
        script_start_time = time.time()

        self.button.add_press_listener(self.on_button_pressed)
        self.button.add_release_listener(self.on_button_released)

        while not self._exit:
            if (time.time() - script_start_time) > self.SCRIPT_TIMEOUT:
                print('No interaction')
                self.display.show("Aborting", "no interaction")
                self.request_exit(4)
            time.sleep(0.5)

        self.cleanup()

        return self._exit_code

    def cleanup(self):
        if self.display.Lock.locked():
            self.display.Lock.release()

        if self.button.is_hold_observer_registered(self.on_button_held):
            self.button.remove_hold_listener(self.on_button_held)

        if self.button.is_press_observer_registered(self.on_button_pressed):
            self.button.remove_press_listener(self.on_button_pressed)

        if self.button.is_release_observer_registered(self.on_button_released):
            self.button.remove_release_listener(self.on_button_released)

        self.button.__del__()

    def request_exit(self, exitcode):
        self._exit = True
        self._exit_code = exitcode

    def on_button_pressed(self):
        self.display.Lock.acquire()
        self.button.add_hold_listener(self.on_button_held)
        print("Button pressed. Hold for {0} seconds to authenticate...".format(self.BUTTON_HOLD_TIME))
        self.display.show_countdown(2, self.BUTTON_HOLD_TIME, "{0} seconds")

    def on_button_held(self, seconds: float):
        if seconds >= self.BUTTON_HOLD_TIME:
            self.button.remove_hold_listener(self.on_button_held)
            print("Release button to complete authentication")
            self.display.show("Release button to", "finish auth")

    def on_button_released(self, seconds: float):
        self.display.hide_countdown()

        if seconds >= self.BUTTON_HOLD_TIME:
            print('Authentication successful')
            self.display.show("Authentication", "successful")
            exitcode = 0
        else:
            print('Button was not pressed long enough')
            self.display.show("Button released", "too soon")
            exitcode = 3

        self.request_exit(exitcode)


sys.exit(InitSystem().wait_for_authentication())
