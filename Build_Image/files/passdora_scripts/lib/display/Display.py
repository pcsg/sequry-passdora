"""
##################################################################
#                                                                #
# Class handling clearing and printing to the connected display. #
#                                                                #
# Author: Jan Wennrich (PCSG)                                    #
#                                                                #
##################################################################
"""

from lib.display.lcddriver import lcd


class Display:
    __instance = None

    isLocked = False

    __LCD = lcd()

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

    def show(self, line1, line2):
        if self.isLocked:
            return False

        self.__LCD.display_string("--==| PASSDORA |==--", 0)
        self.__LCD.display_string("|{0}|".format(line1.center(18)), 1)
        self.__LCD.display_string("|{0}|".format(line2.center(18)), 2)
        self.__LCD.display_string("--------------------", 3)
        return True

    def clear(self):
        self.__LCD.clear()
        self.show("", "")

    def lock(self):
        self.isLocked = True

    def unlock(self):
        self.isLocked = False
