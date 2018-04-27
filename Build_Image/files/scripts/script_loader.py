from lib.autostart.ShowIP import *
from lib.autostart.BackupButtonListener import *
from lib.autostart.ShutdownListener import *
from lib.autostart.RestoreListener import *
from lib.autostart.SshListener import SshListener
from lib.autostart.UpdateListener import *
from lib.autostart.SetupListener import *
from lib.autostart.RebootListener import *

autostarts = [
    ShowIP(),
    BackupButtonListener(),
    ShutdownListener(),
    RestoreListener(),
    UpdateListener(),
    SetupListener(),
    SshListener(),
    RebootListener()
]

for Autostart in autostarts:
    Autostart.start()
