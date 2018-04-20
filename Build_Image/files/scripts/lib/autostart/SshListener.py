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
from lib.util.SSH import SSH


class SshListener(AbstractAutostart):
    # How many seconds has the button to be pressed
    BUTTON_HOLD_TIME_MIN = 10

    # After how many seconds of button pressing the event should be ignored?
    BUTTON_HOLD_TIME_MAX = 12

    # Instructions how to use this script
    MESSAGE_INSTRUCTIONS = "Press and hold the button for {0} seconds to toggle SSH.".format(BUTTON_HOLD_TIME_MIN)

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
        print(self.MESSAGE_INSTRUCTIONS)

    def button_hold_listener(self, seconds: float):
        if self.button_press_time_in_range(seconds) and not self.has_beeped:
            self.has_beeped = True

            self.button.add_release_listener(self.button_release_listener)

            self.buzzer.beep(2)

            if not self.display.Lock.locked():
                self.display.Lock.acquire()
                self.has_locked_display = True

            print("Release button to toggle SSH")
            self.display.show("Release button to", "toggle SSH")

            if self.has_locked_display:
                self.display.Lock.release()

        if seconds > self.BUTTON_HOLD_TIME_MAX:
            self.button.remove_hold_listener(self.button_hold_listener)
            self.button.remove_release_listener(self.button_release_listener)

    def button_release_listener(self, seconds: float):
        # Check if button was pressed long enough
        if self.button_press_time_in_range(seconds):
            self.display.show("Toggling SSH", "")
            self.display.show_loader(2)

            is_ssh_enabled_now = SSH.toggle()

            self.display.hide_loader()

            if is_ssh_enabled_now:
                print("SSH is enabled now.")
                self.display.show("SSH", "enabled")
            else:
                print("SSH is disabled now.")
                self.display.show("SSH", "disabled")

            if self.has_locked_display:
                self.display.Lock.release()

            self.display.show_default()

        self.button.remove_hold_listener(self.button_hold_listener)
        self.button.remove_release_listener(self.button_release_listener)

    def button_press_time_in_range(self, seconds):
        return self.BUTTON_HOLD_TIME_MAX > seconds > self.BUTTON_HOLD_TIME_MIN
