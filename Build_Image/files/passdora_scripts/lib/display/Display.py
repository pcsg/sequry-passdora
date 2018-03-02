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

from lib.display.lcddriver import lcd


class Display:
    __instance = None  # type: Display

    __isLocked = False  # type: bool
    __lockingObject = None  # type: object

    __LCD = lcd()  # type: lcd

    __isLoaderShowing = False  # type: bool

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

    def show(self, line1, line2, caller=None):
        """
        Shows text on the display, overwriting everything on screen

        :param str line1: text to display on the first line
        :param str line2: text to display on the second line
        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if the text was displayed, returns false if the display was locked
        :rtype: bool
        """
        if not self.can_access(caller):
            return False

        self.__LCD.display_string("--==| PASSDORA |==--", 0)
        self.show_on_line(1, line1, caller)
        self.show_on_line(2, line2, caller)
        self.__LCD.display_string("--------------------", 3)
        return True

    def show_on_line(self, line, text, caller=None):
        """
        Shows the given text on a given line of the display without overwriting the rest of the screen

        :param int line: the line to display the text on (can be 1 or 2)
        :param str text: the text to display
        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :raises Exception: throws exception if an invalid line is given

        :return: Returns true if the text was displayed, returns false if the display was locked
        :rtype: bool
        """
        if not self.can_access(caller):
            return False

        # Only allowed to print to line 1 and 2
        if (line is not 1) and (line is not 2):
            raise Exception("Can't write to line " + line)

        # Place "|" on left and right border, center text in between
        self.__LCD.display_string("|{0}|".format(text.center(18)), line)
        return True

    def can_access(self, caller):
        """
        Returns if a given object is allowed to access the display

        :param object caller: the object that should be tested

        :return: Returns true if the object is allowed to access the display or false if it isn't
        :rtype: bool
        """
        if self.__isLocked and caller is not self.__lockingObject:
            return False
        return True

    def show_default(self, caller=None):
        """
        Shows the displays default content

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if the default content was displayed, returns false if the display was locked
        :rtype: bool
        """
        if not self.can_access(caller):
            return False

        # Show hostname and IP
        from lib.autostart.ShowIP import ShowIP
        ShowIP.show()
        return True

    def show_loader(self, line, caller=None):
        """
        Shows a loader on a given line of the display

        :param int line: the line to display the loader on
        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if the loader was displayed, returns false if the display was locked
        :rtype: bool
        """
        if not self.can_access(caller):
            return False

        self.__isLoaderShowing = True

        # Start a new thread with the function printing to the screen
        threading.Thread(target=self.__loader_thread_function, args=(line, caller)).start()

        return True

    def __loader_thread_function(self, line, caller):
        """
        Private function that is started in a separate thread.
        Prints the loading text to the display.
        Runs in a separate thread to be asynchronous since it's using sleep

        :param int line: the line the loader text should be displayed on
        :param object caller: the object that called the show_loader function (required to check if it is allowed to manipulate the display)

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

                self.show_on_line(line, loader_text, caller)
                time.sleep(0.1)

    def hide_loader(self, caller=None):
        """
        Hides the loader

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)

        :return: Returns true if loader was successfully hidden, returns false if the display was locked
        :rtype: bool
        """
        if not self.can_access(caller):
            return False

        self.__isLoaderShowing = False
        return True

    def clear(self, caller=None):
        """
        Clears the display. Leaving only the Passdora-text and frame

        :param object caller: the object calling this function (required to check if it is allowed to manipulate the display)
        :return: Returns true if the display was successfully cleared, returns false if the display was locked
        """
        if not self.can_access(caller):
            return False

        self.__LCD.clear()
        self.show("", "")
        return True

    def lock(self, locker):
        """
        Locks the screen for a given object.
        This means that only the given object can manipulate the display until the object unlocks the display again.
        This is useful if a script needs to show something on the display without background scripts overwriting it.

        :param object locker: The object trying to lock the screen

        :return: Returns true if the screen was successfully locked, returns false if the screen is already locked
        :rtype: bool
        """

        if self.__isLocked:
            return False

        self.__isLocked = True
        self.__lockingObject = locker
        return True

    def unlock(self, locker):
        """
        Unlocks the screen.
        The object that locked the screen needs to be passed as an argument to unlock the screen.
        This means that every object may now manipulate the display again

        :param object locker: the object that initially locked the screen

        :raises Exception: Raises an exception if an object is passed to unlock the display that did not lock the screen

        :return: Returns nothing
        """

        if locker is self.__lockingObject:
            self.__isLocked = False
            self.__lockingObject = None
        else:
            raise Exception("You're not permitted to unlock the display.")
