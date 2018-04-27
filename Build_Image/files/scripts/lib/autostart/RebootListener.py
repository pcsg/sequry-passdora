"""
#############################################################################
                                                                            #
Waits for a button press which lasts over a defined duration .              #
If the button was pressed long enough the SSH is toggled on/off executed    #
                                                                            #
Author: Jan Wennrich (PCSG)                                                 #
                                                                            #
#############################################################################
"""

import RPi.GPIO as GPIO

from lib.autostart.AbstractAutostart import AbstractAutostart
from lib.button.Button import Button
from lib.buzzer.Buzzer import Buzzer
from lib.display.Display import Display
from lib.util.System import System


class RebootListener(AbstractAutostart):
    # How many seconds has the button to be pressed
    BUTTON_HOLD_TIME_MIN = 30

    # After how many seconds of button pressing the event should be ignored?
    BUTTON_HOLD_TIME_MAX = 32

    button = Button.get_instance()

    display = Display.get_instance()

    buzzer = Buzzer.get_instance()

    has_beeped = False

    has_locked_display = False

    def run(self):
        self.button.add_press_listener(self.button_press_listener)

    def button_press_listener(self):
        self.has_beeped = False
        self.has_locked_display = False
        self.button.add_hold_listener(self.button_hold_listener)

    def button_hold_listener(self, seconds: float):
        if not self.has_beeped and self.button_press_time_in_range(seconds):
            self.has_beeped = True

            self.button.add_release_listener(self.button_release_listener)

            self.buzzer.beep(3, 0.1)

            if not self.display.Lock.locked():
                self.display.Lock.acquire()
                self.has_locked_display = True

            print("Release button to reboot")
            self.display.show("Release button to", "reboot")

        if seconds > self.BUTTON_HOLD_TIME_MAX:
            self.cleanup()

    def button_release_listener(self, seconds: float):
        self.cleanup()

        # Check if button was pressed long enough
        if self.button_press_time_in_range(seconds):
            self.display.show("Rebooting", "")
            self.display.show_loader(2)

            System.reboot()

    def button_press_time_in_range(self, seconds):
        return self.BUTTON_HOLD_TIME_MAX > seconds > self.BUTTON_HOLD_TIME_MIN

    def cleanup(self):
        self.button.remove_hold_listener(self.button_hold_listener)
        self.button.remove_release_listener(self.button_release_listener)

        if self.has_locked_display:
            self.display.Lock.release()
