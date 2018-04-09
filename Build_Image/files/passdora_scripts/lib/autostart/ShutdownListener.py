import atexit

import time

from lib.autostart.AbstractAutostart import *
from lib.display.Display import Display


class ShutdownListener(AbstractAutostart):

    @staticmethod
    def __shutdown_listener(self):
        display = Display.get_instance()

        print("Shutting down...")
        display.Lock.acquire()

        display.show_on_line(1, "Shutting down")
        display.show_loader(2)

        time.sleep(3)

        display.turn_off()
        display.hide_loader()

    def run(self):
        atexit.register(self.__shutdown_listener, self)
