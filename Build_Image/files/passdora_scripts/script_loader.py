from lib.autostart.ShowIP import *
from lib.autostart.BackupButtonListener import *
from lib.autostart.ShutdownListener import *
from lib.autostart.RestoreListener import *

autostarts = [
   ShowIP(),
   BackupButtonListener(),
   ShutdownListener(),
   RestoreListener()
]

for Autostart in autostarts:
    Autostart.start()
