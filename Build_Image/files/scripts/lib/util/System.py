import configparser
import os


class System:
    DIR_QUIQQER = '/var/www/html/'

    @staticmethod
    def is_activated() -> bool:
        config = configparser.ConfigParser()
        config_file = System.DIR_QUIQQER + 'etc/plugins/sequry/passdora.ini.php'
        config.read(config_file)

        return config.get('general', 'is_activated') == '"1"'

    @staticmethod
    def reboot():
        return os.system("sudo reboot")
