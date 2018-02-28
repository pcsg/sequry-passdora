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

hostname = "Host: "+socket.gethostname()
ip = "IP: "+get_lan_ip()    

print hostname
print ip
Display.show(hostname, ip)
