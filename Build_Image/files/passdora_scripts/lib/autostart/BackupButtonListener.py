'''
#########################################################################################################
                                                                                                        #
Waits for a button press which lasts over a defined duration on a defined GPIO pin (pulling pin down).  #
If the script was pressed long enough the backup script is executed                                     #
                                                                                                        #
Author: Jan Wennrich (PCSG)                                                                             #
                                                                                                        #
#########################################################################################################
'''

import RPi.GPIO as GPIO
import time
import subprocess

from lib.autostart.AbstractAutostart import AbstractAutostart
from lib.display.Display import Display


class BackupButtonListener(AbstractAutostart):
    # How many seconds has the button to be pressed
    BUTTON_HOLD_TIME = 3

    # How many seconds to sleep between while iterations?
    SLEEP_TIME = 0.15

    # How many seconds to sleep after the button is released?
    # Prevents starting the backup again if the button is not released immediately
    SLEEP_TIME_BUTTON_RELEASED = 2

    # Which GPIO pin is the button connected to?
    BUTTON_GPIO_PIN = 23

    # Instructions how to use this script
    MESSAGE_INSTRUCTIONS = "Press and hold the button for {0} seconds to create a backup.".format(BUTTON_HOLD_TIME)

    def __init__(self, *args, **kwargs):
        super(BackupButtonListener, self).__init__(*args, **kwargs)

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        # Initialize variables
        button_was_pressed = False
        button_held_time = 0

        display = Display.get_instance()

        # Print what the user can do
        print(self.MESSAGE_INSTRUCTIONS)

        # Run forever
        while True:

            # Check if the button is currently pressed
            if not GPIO.input(self.BUTTON_GPIO_PIN):

                display.lock(self)

                # Time the button press starts
                button_press_start_time = time.time()

                # While the button is held not longer than the button has to be held...
                while not GPIO.input(self.BUTTON_GPIO_PIN) and button_held_time < self.BUTTON_HOLD_TIME:
                    if not button_was_pressed:
                        button_was_pressed = True
                        print("Button pressed. Hold for {0} seconds to create a backup...".format(self.BUTTON_HOLD_TIME))
                        display.show("Hold button for", "", self)
                        display.show_countdown(2, self.BUTTON_HOLD_TIME, "{0} seconds", self)

                    # Increase the time the button is held
                    button_held_time = time.time() - button_press_start_time
                    time.sleep(self.SLEEP_TIME)

                # If the button was pressed...
                if button_was_pressed:
                    # Check if button was pressed long enough
                    if button_held_time > self.BUTTON_HOLD_TIME:
                        print('Creating backup... You may release the button now.')
                        display.hide_countdown(self)

                        display.show("Creating Backup", "", self)
                        display.show_loader(2, self)
                        subprocess.Popen('/var/www/html/passdora_scripts/backup.sh').wait()
                        print("Backup created!")
                        display.hide_loader(self)
                        display.show("Backup", "created", self)
                    else:
                        print("Button was not pressed long enough!")
                        display.show("Button released", "too soon", self)

                    # Wait a few seconds to prevent backup starting again immediately
                    print('Waiting {0} seconds before the button can be pressed again...'.format(
                        self.SLEEP_TIME_BUTTON_RELEASED))
                    time.sleep(self.SLEEP_TIME_BUTTON_RELEASED)

                    # Reset variables to default
                    button_was_pressed = False
                    button_held_time = 0

                    # Print that the button can be used again
                    print(self.MESSAGE_INSTRUCTIONS)

                display.unlock(self)
                display.show_default()

            time.sleep(self.SLEEP_TIME)
