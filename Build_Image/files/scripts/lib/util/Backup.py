import subprocess


class Backup:

    folder = "/var/www/html/var/package/sequry/passdora/backups/"

    @staticmethod
    def create():
        subprocess.Popen('/var/www/html/var/package/sequry/passdora/scripts/backup.sh').wait()
