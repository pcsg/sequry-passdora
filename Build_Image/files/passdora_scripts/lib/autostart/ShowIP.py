import time

from lib.ip.ip_tools import *
from lib.autostart.AbstractAutostart import *

import socket


class ShowIP(AbstractAutostart):
    def run(self):
        while True:
            self.update(self.Display)
            time.sleep(30)

    @staticmethod
    def update(display):
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
        display.show(hostname_string, ip_string)
