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

import RPi.GPIO as GPIO
import subprocess

from lib.autostart.AbstractAutostart import AbstractAutostart
from lib.button.Button import Button
from lib.display.Display import Display


class BackupButtonListener(AbstractAutostart):
    # How many seconds has the button to be pressed
    BUTTON_HOLD_TIME = 3

    # Instructions how to use this script
    MESSAGE_INSTRUCTIONS = "Press and hold the button for {0} seconds to create a backup.".format(BUTTON_HOLD_TIME)

    button = Button.get_instance()

    display = Display.get_instance()

    def __init__(self, *args, **kwargs):
        super(BackupButtonListener, self).__init__(*args, **kwargs)

    def run(self):
        self.button.add_release_listener(self.button_release_listener)
        self.button.add_press_listener(self.button_press_listener)
        self.button.add_hold_listener(self.button_hold_listener)

    def button_press_listener(self):
        self.display.Lock.acquire()

        print("Button pressed. Hold for {0} seconds to create a backup...".format(self.BUTTON_HOLD_TIME))
        self.display.show("Hold button for", "3 seconds")

        self.display.show_countdown(2, self.BUTTON_HOLD_TIME, "{0} seconds")

    def button_hold_listener(self, seconds: float):
        if seconds >= self.BUTTON_HOLD_TIME:
            self.display.hide_countdown()

            print("Release button to start backup")
            self.display.show("Release button to", "start backup")

    def button_release_listener(self, seconds: float):
        self.display.hide_countdown()

        # Check if button was pressed long enough
        if seconds > self.BUTTON_HOLD_TIME:
            print('Creating backup... You may release the button now.')

            self.display.show("Creating Backup", "")
            self.display.show_loader(2)

            subprocess.Popen('/var/www/html/var/package/sequry/passdora/scripts/backup.sh').wait()

            print("Backup created!")
            self.display.hide_loader()
            self.display.show("Backup", "created")
        else:
            print("Button was not pressed long enough!")
            self.display.show("Button released", "too soon")

        # Print that the button can be used again
        print(self.MESSAGE_INSTRUCTIONS)

        self.display.Lock.release()
        self.display.show_default()
