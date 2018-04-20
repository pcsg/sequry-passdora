import subprocess


class SSH:
    @staticmethod
    def is_enabled() -> bool:
        """
        Returns if SSH is start on boot.

        :return: Is SSH started on boot
        """
        output = subprocess.run("sudo service ssh status".split(" "), stdout=subprocess.PIPE).stdout.decode('utf-8')
        return "(running)" in output

    @staticmethod
    def enable() -> None:
        """
        Enables SSH

        :return: Nothing
        """
        subprocess.run("sudo update-rc.d -f ssh enable".split(" "))
        subprocess.run("sudo service ssh start".split(" "))

    @staticmethod
    def disable() -> None:
        """
        Disables SSH

        :return: Nothing
        """
        subprocess.run("sudo service ssh stop".split(" "))
        subprocess.run("sudo pkill --signal HUP sshd".split(" "))
        subprocess.run("sudo update-rc.d -f ssh disable".split(" "))

    @staticmethod
    def toggle() -> bool:
        """
        Toggles SSH status

        :return: Returns True if it's enabled afterwards
        """
        if SSH.is_enabled():
            SSH.disable()
            return False

        SSH.enable()
        return True
