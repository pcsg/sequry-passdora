import configparser
import os

from time import sleep

from lib.autostart.AbstractAutostart import *
from lib.display.Display import Display


class SetupListener(AbstractAutostart):
    dir_quiqqer = '/var/www/html/'

    config = configparser.ConfigParser()
    config_file = dir_quiqqer + 'etc/plugins/sequry/passdora.ini.php'
    config.read(config_file)

    display = Display.get_instance()

    def run(self):
        if self.is_setup_requested():
            self.display.Lock.acquire()

            # TODO: Confirm setup with a button press
            print("Executing system-setup...")

            self.display.show("System setting up", "")
            self.display.show_loader(2)

            self.handle_hostname()

            self.handle_dhcp()

            self.handle_wifi()

            # Set is_requested in config to zero and save the file
            self.set_is_requested(0)

            self.display.hide_loader()
            print("Setup completed!")
            self.display.show("Setup", "Complete!")

            sleep(2)

            print("Restarting the system...")
            self.display.show("Restarting", "")
            self.display.show_loader(2)

            sleep(2)

            self.display.turn_off()
            os.system("sudo shutdown now -r")

    def handle_hostname(self):
        hostname = self.config.get('setup', 'hostname')
        os.system('echo "{0}" | sudo tee /etc/hostname > /dev/null'.format(hostname))
        os.system('sudo sed -i "s/127\.0\.1\.1.*passdora/127.0.1.1 {0}/g" /etc/hosts'.format(hostname))

    def is_setup_requested(self):
        # Remove '"' from the value and then convert to int
        return int(self.config.get('setup', 'is_requested').replace('"', '')) == 1

    def handle_dhcp(self):
        file_interfaces = open("/etc/network/interfaces.d/passdora.conf", "w")

        file_interfaces.write("auto lo\n")
        file_interfaces.write("iface lo inet loopback\n")

        if self.config.get('setup', 'isDhcpEnabled') == '"1"':
            file_interfaces.write("eth0 inet dhcp\n")
            file_interfaces.write("wlan0 inet dhcp\n")
        else:
            ip = self.config.get('setup', 'ip').replace('"', '')
            subnetmask = self.config.get('setup', 'subnetmask').replace('"', '')

            file_interfaces.write("auto eth0:1\n")
            file_interfaces.write("iface eth0:1 inet static\n")
            file_interfaces.write("address " + ip + "\n")
            file_interfaces.write("netmask " + subnetmask + "\n")

            file_interfaces.write("auto wlan0:1\n")
            file_interfaces.write("iface wlan0:1 inet static\n")
            file_interfaces.write("address " + ip + "\n")
            file_interfaces.write("netmask " + subnetmask + "\n")

        file_interfaces.close()

    def handle_wifi(self):
        if self.config.get('setup', 'isWifiEnabled') == '"1"':
            ssid = self.config.get('setup', 'wifiSsid').replace('"', '')
            password = self.config.get('setup', 'wifiPassword').replace('"', '')

            file_wifi = open("/etc/wpa_supplicant/wpa_supplicant.conf", "a")

            file_wifi.write('\n')
            file_wifi.write('network={\n')
            file_wifi.write('    ssid="{0}"\n'.format(ssid))
            file_wifi.write('    psk="{0}"\n'.format(password))
            file_wifi.write('}\n')

            file_wifi.close()

    def set_is_requested(self, value):
        self.config.set("setup", "is_requested", '"' + str(value) + '"')
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
