import configparser
import os

from time import sleep

from lib.autostart.AbstractAutostart import *
from lib.display.Display import Display


class RestoreListener(AbstractAutostart):
    dir_quiqqer = '/var/www/html/'
    dir_restore = dir_quiqqer + 'var/package/sequry/passdora/restore/'

    config = configparser.ConfigParser()
    config_file = dir_quiqqer + 'etc/plugins/sequry/passdora.ini.php'
    config.read(config_file)

    display = Display.get_instance()

    def run(self):
        if self.is_restore_requested():
            self.display.Lock.acquire()

            # TODO: Confirm backup with a button press
            print("Processing System-Restore...")

            self.display.show("", "")
            self.display.show_loader(2)

            # Extract files
            print("Extracting files...")
            self.display.show_on_line(1, "Extracting files")
            self.extract_files()

            # Copy QUIQQER etc/ folder
            print("Restoring QUIQQER settings...")
            self.display.show_on_line(1, "Restoring QUIQQER")
            self.restore_quiqqer_config()

            # Copy system etc/ folder
            print("Restoring system settings...")
            self.display.show_on_line(1, "Restoring System")
            self.restore_system_config()

            # Restore MySQL backup
            print("Restoring MySQL database...")
            self.display.show_on_line(1, "Restoring Database")
            self.restore_database()

            # Set is_requested in config to zero and save the file
            self.set_is_requested(0)

            self.display.hide_loader()
            print("Restore completed!")
            self.display.show("Restore", "Complete!")

            sleep(2)

            print("Restarting the system...")
            self.display.show("Restarting", "")
            self.display.show_loader(2)

            sleep(2)

            self.display.turn_off()
            os.system("sudo shutdown now -r")

    def extract_files(self):
        if os.path.isfile(self.dir_restore + "restore.tgz"):
            os.system("sudo tar --same-owner -xpzf " + self.dir_restore + "restore.tgz -C " + self.dir_restore)
            return True
        return False

    def restore_quiqqer_config(self):
        if os.path.isdir(self.dir_restore + "quiqqer_etc"):
            os.system("sudo rsync --delete-after -a " + self.dir_restore + "/quiqqer_etc/ " + self.dir_quiqqer + "etc")
            return True
        return False

    def restore_system_config(self):
        if os.path.isdir(self.dir_restore + "system_etc/"):
            os.system("sudo rsync --delete-after -a " + self.dir_restore + "system_etc/ /etc")
            return True
        return False

    def restore_database(self):
        if os.path.isfile(self.dir_restore + "database.sql"):
            os.system("sudo mysql quiqqer < " + self.dir_restore + "database.sql")
            return True
        return False

    def is_restore_requested(self):
        # Remove '"' from the value and then convert to int
        return int(self.config.get('restore', 'is_requested').replace('"', '')) == 1

    def set_is_requested(self, value):
        self.config.set("restore", "is_requested", '"'+str(value)+'"')
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
