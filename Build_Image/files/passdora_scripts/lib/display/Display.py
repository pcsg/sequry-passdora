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
    __instance = None

    __isLocked = False
    __lockingObject = None

    __LCD = lcd()

    __isLoaderShowing = False

    @staticmethod
    def get_instance():
        if Display.__instance is None:
            Display()
        return Display.__instance

    def __init__(self):
        if Display.__instance is not None:
            raise Exception("Display is a Singleton, use get_instance method to get an instance!")
        else:
            Display.__instance = self

    def show(self, line1, line2, caller=None):
        if not self.can_access(caller):
            return False

        self.__LCD.display_string("--==| PASSDORA |==--", 0)
        self.show_on_line(1, line1, caller)
        self.show_on_line(2, line2, caller)
        self.__LCD.display_string("--------------------", 3)
        return True

    def show_on_line(self, line, text, caller=None):
        if not self.can_access(caller):
            return False

        if (line is not 1) and (line is not 2):
            raise Exception("Can't write to line " + line)

        self.__LCD.display_string("|{0}|".format(text.center(18)), line)
        return True

    def can_access(self, caller):
        if self.__isLocked and caller is not self.__lockingObject:
            return False
        return True

    def show_default(self, caller=None):
        if not self.can_access(caller):
            return False

        from lib.autostart.ShowIP import ShowIP
        ShowIP.show()
        return True

    def show_loader(self, line, caller=None):
        if not self.can_access(caller):
            return False

        self.__isLoaderShowing = True
        threading.Thread(target=self.__loader_thread_function, args=(line, caller)).start()
        return True

    def __loader_thread_function(self, line, caller):
        while self.__isLoaderShowing:
            for i in range(0, 4):
                if not self.__isLoaderShowing:
                    break

                loader_text = " " * i + "." + " " * (3 - i)
                self.show_on_line(line, loader_text, caller)
                time.sleep(0.1)

    def hide_loader(self, caller=None):
        if not self.can_access(caller):
            return False

        self.__isLoaderShowing = False
        return True

    def clear(self, caller=None):
        if not self.can_access(caller):
            return False

        self.__LCD.clear()
        self.show("", "")
        return True

    def lock(self, locker):
        if self.__isLocked:
            return False

        self.__isLocked = True
        self.__lockingObject = locker
        return True

    def unlock(self, locker):
        if locker is self.__lockingObject:
            self.__isLocked = False
            self.__lockingObject = None
        else:
            raise Exception("You're not permitted to unlock the display.")
