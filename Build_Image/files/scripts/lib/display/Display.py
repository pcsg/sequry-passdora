"""
##################################################################
#                                                                #
# Class handling clearing and printing to the connected display. #
#                                                                #
# Author: Jan Wennrich (PCSG)                                    #
#                                                                #
##################################################################
"""
import threading
import time

from lib.display.RPLCD.i2c import CharLCD


class Display:
    __instance = None  # type: Display

    __isLocked = False  # type: bool
    __lockingObject = None  # type: object

    __LCD = CharLCD(
        i2c_expander='PCF8574',
        address=0x27,
        port=1,
        cols=20, rows=4,
        dotsize=8,
        charmap='A02',
        backlight_enabled=True
    )  # type: CharLCD

    __isLoaderShowing = False  # type: bool
    __isCountdownShowing = False  # type: bool

    Lock = threading.Lock()  # type: Lock

    @staticmethod
    def get_instance():
        """
        Returns an instance of this class (Singleton)

        :rtype: Display
        """
        if Display.__instance is None:
            Display()
        return Display.__instance

    def __init__(self):
        if Display.__instance is not None:
            raise Exception("Display is a Singleton, use get_instance method to get an instance!")
        else:
            Display.__instance = self

    def show(self, line1, line2):
        """
        Shows text on the display, overwriting everything on screen

        :param str line1: text to display on the first line
        :param str line2: text to display on the second line

        :return: Returns true if the text was displayed, returns false if the display was locked
        :rtype: bool
        """
        line1 = line1.center(18)
        line2 = line2.center(18)

        text = "--==| PASSDORA |==--\r\n" + \
               "|" + line1 + "|\r\n" + \
               "|" + line2 + "|\r\n" + \
               "--------------------"

        self.__LCD.home()
        self.__LCD.write_string(text)

    def show_on_line(self, line, text):
        """
        Shows the given text on a given line of the display without overwriting the rest of the screen

        :param int line: the line to display the text on (can be 1 or 2)
        :param str text: the text to display

        :raises Exception: throws exception if an invalid line is given

        :return: Returns true if the text was displayed, returns false if the display was locked
        :rtype: bool
        """
        # Place "|" on left and right border, center text in between
        self.__LCD.cursor_pos = (line, 0)
        text = "|{0}|".format(text.center(18))
        self.__LCD.write_string(text)

    def show_default(self):
        """
        Shows the displays default content

        :return: Returns true if the default content was displayed, returns false if the display was locked
        :rtype: bool
        """
        # Show hostname and IP
        from lib.autostart.ShowIP import ShowIP
        ShowIP.show()

    def show_loader(self, line):
        """
        Shows a loader on a given line of the display

        :param int line: the line to display the loader on

        :return: Returns true if the loader was displayed, returns false if the display was locked
        :rtype: bool
        """
        self.__isLoaderShowing = True

        # Start a new thread with the function printing to the screen
        threading.Thread(target=self.__loader_thread_function, args=[line]).start()

        return True

    def __loader_thread_function(self, line):
        """
        Private function that is started in a separate thread.
        Prints the loading text to the display.
        Runs in a separate thread to be asynchronous since it's using sleep

        :param int line: the line the loader text should be displayed on

        :return: Returns nothing
        :rtype: None
        """
        while self.__isLoaderShowing:
            # Move dot from left to right (4 digits)
            for i in range(0, 4):
                if not self.__isLoaderShowing:
                    # Break, because the for loop would finish execution even if the loader should be hidden
                    break

                # Place spaces before and after the dot to move it from left to right
                loader_text = " " * i + "." + " " * (3 - i)

                self.show_on_line(line, loader_text)
                time.sleep(0.2)

    def hide_loader(self):
        """
        Hides the loader

        :return: Returns true if loader was successfully hidden, returns false if the display was locked
        :rtype: bool
        """
        self.__isLoaderShowing = False

    def show_countdown(self, line, seconds, text):
        """
        Shows a countdown on a given line of the display

        :param int line: the line to display the countdown on
        :param int seconds: how many seconds the countdown should count down
        :param str text: additional text to display, "{0}" in the text will be replaced by current countdown value

        :return: Returns true if the countdown was displayed, returns false if the display was locked
        :rtype: bool
        """
        self.__isCountdownShowing = True

        # Start a new thread with the function printing to the screen
        threading.Thread(target=self.__countdown_threaded_function, args=(line, seconds, text)).start()

    def __countdown_threaded_function(self, line, seconds, text):
        """
        Private function that is started in a separate thread.
        Prints the countdown to the display.
        Runs in a separate thread to be asynchronous since it's using sleep

        :param int line: the line the countdown text should be displayed on

        :return: Returns nothing
        :rtype: None
        """
        for second in range(seconds, 0, -1):
            if not self.__isCountdownShowing:
                break
            print(text.format(second))
            self.show_on_line(line, text.format(second))
            time.sleep(1)
        self.hide_countdown()

    def hide_countdown(self):
        """
        Hides the active countdown

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if the countdwon was successfully hidden, returns false if the display was locked
        :rtype: bool
        """
        self.__isCountdownShowing = False

    def clear(self):
        """
        Clears the display. Leaving only the Passdora-text and frame

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)
        :return: Returns true if the display was successfully cleared, returns false if the display was locked
        """
        self.__LCD.clear()
        self.show("", "")

    def turn_off(self):
        """
        Turns the display off

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if the screen was successfully turned off, returns false if the screen was locked
        :rtype: bool
        """
        self.__LCD.backlight_enabled = False
        self.__LCD.display_enabled = False

    def turn_on(self):
        """
        Turns the display on

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if the screen was successfully turned off, returns false if the screen was locked
        :rtype: bool
        """
        self.__LCD.backlight_enabled = True
        self.__LCD.display_enabled = True
        return True
