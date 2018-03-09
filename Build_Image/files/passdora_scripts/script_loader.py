from lib.autostart.ShowIP import *
from lib.autostart.BackupButtonListener import *
from lib.autostart.ShutdownListener import *

autostarts = [
    ShowIP(),
    BackupButtonListener(),
    ShutdownListener()
]

for Autostart in autostarts:
    Autostart.start()
