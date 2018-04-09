import configparser
import os

from time import sleep

from lib.autostart.AbstractAutostart import *
from lib.display.Display import Display


class UpdateListener(AbstractAutostart):
    dir_quiqqer = '/var/www/html/'
    dir_update = dir_quiqqer + 'var/package/sequry/passdora/update/'
    dir_update_files = dir_update + 'files/'

    file_update_archive = dir_update + "update.tgz"
    file_version = dir_update + "VERSION"
    file_update_script = dir_update + "update.sh"

    config = configparser.ConfigParser()
    config_file = dir_quiqqer + 'etc/plugins/sequry/passdora.ini.php'
    config.read(config_file)

    display = Display.get_instance()

    def run(self):
        if self.is_update_requested():
            self.display.lock(self)

            # TODO: Confirm update with a button press
            print("Processing System-Update...")

            self.display.show("", "", self)
            self.display.show_loader(2, self)

            print("Extracting files...")
            self.display.show_on_line(1, "Extracting files")
            self.extract_files()

            print("Moving files...")
            self.display.show_on_line(1, "Moving files")
            self.move_files()

            print("Running update-script...")
            self.display.show_on_line(1, "Executing scripts")
            self.run_update_script()

            # Set is_requested in config to zero and save the file
            self.set_is_requested(0)

            self.display.hide_loader(self)
            print("Update completed!")
            self.display.show("Update", "Complete!", self)

            sleep(2)

            print("Restarting the system...")
            self.display.show("Restarting", "", self)
            self.display.show_loader(2, self)

            sleep(2)

            self.display.turn_off(self)
            os.system("sudo shutdown now -r")

    def extract_files(self):
        if os.path.isfile(self.file_update_archive):
            os.system("sudo tar --same-owner -xpzf " + self.file_update_archive + " -C " + self.dir_update)
            return True
        return False

    def move_files(self):
        os.system("sudo rsync -a " + self.dir_update_files + " /")

    def run_update_script(self):
        os.system("sudo bash " + self.file_update_script)

    def get_update_version(self):
        with open(self.file_version) as file:
            return file.read().strip()

    def is_update_requested(self):
        # Remove '"' from the value and then convert to int
        return int(self.config.get('update', 'is_requested').replace('"', '')) == 1

    def set_is_requested(self, value):
        self.config.set("update", "is_requested", '"' + str(value) + '"')
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
