"""
#########################################################################################################
                                                                                                        #
Waits for a button press which lasts over a defined duration on a defined GPIO pin (pulling pin down).  #
If the script was pressed long enough the backup script is executed                                     #
                                                                                                        #
Author: Jan Wennrich (PCSG)                                                                             #
                                                                                                        #
#########################################################################################################
"""
from time import sleep

import RPi.GPIO as GPIO

from lib.autostart.AbstractAutostart import AbstractAutostart
from lib.button.Button import Button
from lib.buzzer.Buzzer import Buzzer
from lib.display.Display import Display
from lib.util.Backup import Backup
from lib.util.System import System


class BackupButtonListener(AbstractAutostart):
    # How many seconds has the button to be pressed
    BUTTON_HOLD_TIME_MIN = 3

    # After how many seconds of button pressing the event should be ignored?
    BUTTON_HOLD_TIME_MAX = 5

    # Instructions how to use this script
    MESSAGE_INSTRUCTIONS = "Press and hold the button for {0} seconds to create a backup.".format(BUTTON_HOLD_TIME_MIN)

    button = Button.get_instance()

    buzzer = Buzzer.get_instance()

    display = Display.get_instance()

    has_beeped = False

    has_locked_display = False

    def run(self):
        self.button.add_press_listener(self.button_press_listener)

    def button_press_listener(self):
        if not System.is_activated():
            return

        self.has_beeped = False

        self.button.add_hold_listener(self.button_hold_listener)

        if not self.display.Lock.locked():
            self.display.Lock.acquire()
            self.has_locked_display = True

        print("Button pressed. Hold for {0} seconds to create a backup...".format(self.BUTTON_HOLD_TIME_MIN))
        self.display.show("Hold button for", "3 seconds")

    def button_hold_listener(self, seconds: float):
        if self.BUTTON_HOLD_TIME_MAX > seconds > self.BUTTON_HOLD_TIME_MIN and not self.has_beeped:
            self.has_beeped = True

            self.button.add_release_listener(self.button_release_listener)

            self.buzzer.beep()

            print("Release button to start backup")
            self.display.show("Release button to", "start backup")

        if seconds > self.BUTTON_HOLD_TIME_MAX:
            self.button.remove_hold_listener(self.button_hold_listener)
            self.button.remove_release_listener(self.button_release_listener)

    def button_release_listener(self, seconds: float):
        # Check if button was pressed long enough
        if self.BUTTON_HOLD_TIME_MAX > seconds > self.BUTTON_HOLD_TIME_MIN:
            self.display.show("Creating Backup", "")
            self.display.show_loader(2)

            Backup.create()

            print("Backup created!")
            self.display.hide_loader()
            self.display.show("Backup", "created")

            sleep(2)

        self.button.remove_hold_listener(self.button_hold_listener)
        self.button.remove_release_listener(self.button_release_listener)

        # Print that the button can be used again
        print(self.MESSAGE_INSTRUCTIONS)

        if self.has_locked_display:
            self.display.Lock.release()

        self.display.show_default()
