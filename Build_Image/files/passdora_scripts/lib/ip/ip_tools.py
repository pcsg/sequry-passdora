"""
#########################################################################################
#                                                                                       #
# Function to get the devices local IP address                                          #
#                                                                                       #
# Author: Jamieson Becker (Stackoverflow: https://stackoverflow.com/a/28950776/3002417) #
#                                                                                       #
#########################################################################################
"""

import socket


def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

