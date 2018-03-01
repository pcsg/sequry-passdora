import threading

from lib.display.display_util import Display


class AbstractAutostart(threading.Thread):
    def __init__(self, display, *args, **kwargs):
        super(AbstractAutostart, self).__init__(*args, **kwargs)
        self.Display = display

    def run(self):
        pass
