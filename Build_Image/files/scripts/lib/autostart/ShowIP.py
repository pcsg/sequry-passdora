import time

from lib.display.Display import Display
from lib.ip.ip_tools import *
from lib.autostart.AbstractAutostart import *

import socket

INTERVAL = 30


class ShowIP(AbstractAutostart):
    def run(self):
        while True:
            if not Display.Lock.locked():
                Display.Lock.acquire()
                self.show()
                Display.Lock.release()
            time.sleep(INTERVAL)

    @staticmethod
    def show():
        hostname = socket.gethostname()
        ip = get_lan_ip()

        hostname_string = "Host:"
        if len(hostname) < 15:
            hostname_string += " "
        hostname_string += hostname

        ip_string = "IP:"
        if len(ip) < 15:
            ip_string += " "
        ip_string += ip

        print(hostname_string)
        print(ip_string)
        Display.get_instance().show(hostname_string, ip_string)
