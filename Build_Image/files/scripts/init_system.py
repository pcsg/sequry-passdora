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
from lib.display.Display import Display


# How many seconds has the button to be pressed
BUTTON_HOLD_TIME = 3

# How many seconds to sleep between while iterations?
SLEEP_TIME = 0.1

# After how many seconds should the script timeout?
SCRIPT_TIMEOUT = 30

# Which GPIO pin is the button connected to?
BUTTON_GPIO_PIN = 18


display = Display.get_instance()

self = object()


try:
    selected_option = sys.argv[1]
except IndexError:
    print("You need to specify an option. Valid options: show_code, init")
    exit(1)


if "show_code" == sys.argv[1]:
    try:
        code = sys.argv[2]
    except IndexError:
        print("You need to specify a code to display.")
        exit(1)

    display.Lock.acquire()
    display.show("Code:", sys.argv[2])
    exit(0)


if "init" == sys.argv[1]:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    scriptStartTime = time.time()

    print("Press and hold the button for {0} seconds to authenticate".format(BUTTON_HOLD_TIME))
    display.show("Hold button for", "{0} seconds".format(BUTTON_HOLD_TIME))

    button_was_pressed = False
    button_held_time = 0

    while True:
        start_time = time.time()

        while not GPIO.input(BUTTON_GPIO_PIN):
            if not button_was_pressed:
                print("Button pressed. Hold for {0} seconds to authenticate...".format(BUTTON_HOLD_TIME))
                display.show_countdown(2, BUTTON_HOLD_TIME, "{0} seconds")

            if button_held_time >= BUTTON_HOLD_TIME:
                display.hide_countdown()

                print("Release button to complete authentication")
                display.show("Release button to", "finish auth")

                # Wait until button is released
                while not GPIO.input(BUTTON_GPIO_PIN):
                    pass
                break

            button_was_pressed = True
            button_held_time = time.time() - start_time
            time.sleep(SLEEP_TIME)

        if button_was_pressed:
            display.hide_countdown()

            if button_held_time > BUTTON_HOLD_TIME:
                print('Authentication successful')
                display.show("Authentication", "successful")
                sys.exit(0)
            else:
                print('Button was not pressed long enough')
                display.show("Button released", "too soon")
                sys.exit(3)

        if time.time() - scriptStartTime > SCRIPT_TIMEOUT:
            print('No interaction')
            display.show("Aborting", "no interaction")
            sys.exit(4)

        time.sleep(SLEEP_TIME)