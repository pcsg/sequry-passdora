from lib.autostart.ShowIP import *
from lib.autostart.BackupButtonListener import *


autostarts = [
    ShowIP(),
    BackupButtonListener()
]

for Autostart in autostarts:
    Autostart.start()
