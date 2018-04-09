from lib.autostart.ShowIP import *
from lib.autostart.BackupButtonListener import *
from lib.autostart.ShutdownListener import *
from lib.autostart.RestoreListener import *
from lib.autostart.UpdateListener import *

autostarts = [
   ShowIP(),
   BackupButtonListener(),
   ShutdownListener(),
   RestoreListener(),
   UpdateListener()
]

for Autostart in autostarts:
    Autostart.start()
