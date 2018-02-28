'''
################################################################
#                                                              #
# Displays the hostname and IP on a display connected via I2C. #
#                                                              #
# Author: Jan Wennrich (PCSG)                                  #
#                                                              #
################################################################
'''

from lib.ip.ip_tools import *
from lib.display.display_util import *
import socket

Display = Display()

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

print hostname_string
print ip_string
Display.show(hostname_string, ip_string)

