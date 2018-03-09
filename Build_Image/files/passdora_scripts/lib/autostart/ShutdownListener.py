import atexit

import time

from lib.autostart.AbstractAutostart import *
from lib.display.Display import Display


class ShutdownListener(AbstractAutostart):

    @staticmethod
    def __shutdown_listener(self):
        display = Display.get_instance()

        print("Shutting down...")
        display.lock(self)

        display.show_on_line(1, "Shutting down", self)
        display.show_loader(2, self)

        time.sleep(3)

        display.turn_off()
        display.hide_loader(self)

    def run(self):
        atexit.register(self.__shutdown_listener, self)
