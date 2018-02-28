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


# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize variables
buttonWasPressed = False
buttonHeldTime = 0

# Print what the user can do
print MESSAGE_INSTRUCTIONS

# Run forever
while True:
    
    # Check if the button is currently pressed
    if GPIO.input(BUTTON_GPIO_PIN) == False:
        
        # Time the button press starts
        buttonPressStartTime = time.time()

        # While the button is held not longer than the button has to be held...
        while GPIO.input(BUTTON_GPIO_PIN) == False and buttonHeldTime < BUTTON_HOLD_TIME:
            if not buttonWasPressed:
                buttonWasPressed = True
                print "Button pressed. Hold for {0} seconds to create a backup...".format(BUTTON_HOLD_TIME)

            # Increase the time the button is held        
            buttonHeldTime = time.time() - buttonPressStartTime
            time.sleep(SLEEP_TIME)


        # If the button was pressed...
        if buttonWasPressed:
            # Check if button was pressed long enough
            if buttonHeldTime > BUTTON_HOLD_TIME:
                print 'Creating backup... You may release the button now.'
                subprocess.Popen('/var/www/html/passdora_scripts/backup.sh').wait()
                print "Backup created!"
            else:
                print "Button was not pressed long enough!"
            
            # Wait a few seconds to prevent backup starting again immediately
            print 'Waiting {0} seconds before the button can be pressed again...'.format(SLEEP_TIME_BUTTON_RELEASED)
            time.sleep(SLEEP_TIME_BUTTON_RELEASED)
            
            # Reset variables to default
            buttonWasPressed = False
            buttonHeldTime = 0
            
            # Print that the button can be used again
            print MESSAGE_INSTRUCTIONS
                
    time.sleep(SLEEP_TIME)

