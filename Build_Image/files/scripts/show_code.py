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

from lib.display.Display import Display

try:
    code = sys.argv[1]
except IndexError:
    print("You need to specify a code to display.")
    exit(1)

display = Display.get_instance()
display.Lock.acquire()
display.show("Code:", sys.argv[2])
exit(0)
