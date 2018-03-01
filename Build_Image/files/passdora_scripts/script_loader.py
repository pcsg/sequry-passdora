from lib.autostart.ShowIP import *
from lib.autostart.BackupButtonListener import *

Display = Display()

autostarts = [ShowIP(Display), BackupButtonListener(Display)]

for Autostart in autostarts:
    Autostart.run()
