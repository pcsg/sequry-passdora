'''
Waits for a button press which lasts over a defined duration on GPIO pin 18 (pulling pin down).
The script then exits with a success or an error code accordingly.
Exit codes:
    0: button was pressed long enough and in time
    3: button wasn't pressed long enough
    4: button wasn't pressed in time
'''

import RPi.GPIO as GPIO
import sys
import time


# How many seconds has the button to be pressed
BUTTON_PRESS_TIME = 3

# How many seconds to sleep between while iterations?
SLEEP_TIME = 0.1

# After how many seconds should the script timeout?
SCRIPT_TIMEOUT = 30

# Which GPIO pin is the button connected to?
BUTTON_GPIO_PIN = 18


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


scriptStartTime = time.time()

print "Press and hold the button for {0} seconds to verify".format(BUTTON_PRESS_TIME)

while True:

    buttonWasPressed = False
    buttonPressedTime = 0
    
    startTime = time.time()

    while GPIO.input(BUTTON_GPIO_PIN) == False and buttonPressedTime < BUTTON_PRESS_TIME:
        if not buttonWasPressed:
            print "Button pressed. Hold for {0} seconds to verify...".format(BUTTON_PRESS_TIME)
    
        buttonWasPressed = True
        buttonPressedTime = time.time() - startTime
        time.sleep(SLEEP_TIME)

    if buttonWasPressed:
        if buttonPressedTime > BUTTON_PRESS_TIME:
    	    print 'Verified'
    	    sys.exit(0)
        else:
	        print 'Button was not pressed long enough'
	        sys.exit(3)
	        
    if time.time() - scriptStartTime > SCRIPT_TIMEOUT:
        print 'No interaction'
        sys.exit(4)
        
    time.sleep(SLEEP_TIME)

