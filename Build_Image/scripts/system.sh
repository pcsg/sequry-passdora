#!/usr/bin/env bash

############################################################
#                                                          #
# This file contains various function to set up the system #
#                                                          #
# Author: Jan Wennrich (PCSG)                              #
#                                                          #
############################################################


# Echos a message from system context
function system_Echo() {
    echo -e "\033[0;32msystem: $1\033[0m"
}


# Reboots the system
function system_Reboot() {
    sudo shutdown now -r
}


# Shuts the system down
function system_Shutdown() {
    sudo shutdown now
}


# Changes the hostname to passdora
function system_SetHostname() {
    echo "passdora" | sudo tee /etc/hostname > /dev/null
    sudo sed -i "s/127\.0\.1\.1.*raspberrypi/127.0.1.1 $1/g" /etc/hosts
}


# Reduces the memory the GPU can use to 16 (minimum)
function system_SetGpuMem() {
    echo "gpu_mem=$1" | sudo tee --append /boot/config.txt > /dev/null
}


# Restarts all components for the webserver (nginx, fpm)
function system_RestartWebserverComponents() {
    sudo /etc/init.d/php7.0-fpm restart
    sudo /etc/init.d/nginx restart
}


function system_appendAutostartCommands() {
    sudo sed -i "s/^exit 0/sudo python3 \/var\/www\/html\/var\/package\/sequry\/passdora\/scripts\/script_loader.py\n\nexit 0/g" /etc/rc.local

    echo "@reboot root cd /home/pi/Initialize_System/ && sudo ./init_system.sh >> /var/log/init_system.log 2>&1" | sudo tee /etc/cron.d/initsystem > /dev/null
}


# Copies scripts to enable automatic mounting of plugged in usb sticks
# See: https://raspberrypi.stackexchange.com/a/66324
function system_setupUsbAutomount() {
    # Udev rule
    sudo cp files/usb_automount/usbstick.rules /etc/udev/rules.d/usbstick.rules

    # Systemd service
    sudo cp files/usb_automount/usbstick-handler@.service /lib/systemd/system/usbstick-handler@.service

    # Mount script
    sudo cp files/usb_automount/automount /usr/local/bin/automount
    sudo chmod +x /usr/local/bin/automount
}


function system_setupFstab() {
    echo "/dev/disk/by-path/platform-3f980000.usb-usb-0:1.4:1.0-scsi-0:0:0:0-part1 /media/system auto defaults 0 0" | sudo tee --append /etc/fstab > /dev/null
    sudo mount -a
}


function system_setupUsbLogs() {
    sudo service rsyslog stop

    mkdir -p /media/system/var/log/
    sudo rsync -a /var/log/ /media/system/var/
    sudo ln -s /media/system/var/log/ /var/log

    sudo service rsyslog start
}


function system_createCrons() {
#    sudo ln -s /var/www/html/var/package/sequry/passdora/scripts/backup.sh /etc/cron.daily/backup.sh
    # Run backup-check script every hour
    echo "0 * * * * root sudo php /var/www/html/var/package/sequry/passdora/scripts/cron_backup.php" | sudo tee /etc/cron.d/backup > /dev/null
}


function system_enableI2C() {
    echo "i2c-dev" | sudo tee --append /etc/modules > /dev/null
    sudo sed -i "s/\#\?dtparam=i2c_arm=\(on\|off\)/dtparam=i2c_arm=on/g" /boot/config.txt
}


function system_setPermissions() {
    sudo adduser www-data gpio
    sudo adduser www-data i2c
}


# Imports the Passdora-Vendor GPG public key for www-data, pi and root user
function system_importGpgKey() {
    # TODO: load cert from an online source(?)
    sudo gpg --import files/gpg.key
    sudo -u pi gpg --import files/gpg.key
    sudo -u www-data gpg --import files/gpg.key
}


function system_copyInterfaceConfig() {
    sudo cp files/passdora.conf /etc/network/interfaces.d/
}


# Renames user pi to a given name
function system_setUsername() {
    sudo usermod -l ${1} pi
    sudo usermod -m -d /home/${1} ${1}

    # TODO: you need to be logged in as root in order to change the username
    # See: https://www.modmypi.com/blog/how-to-change-the-default-account-username-and-password
}


# Executes the system setup steps in correct order
function system_ExecuteStep() {
    #system_Echo "Setting username..."
    #system_setUsername admin

    system_Echo "Copying interface config..."
    system_copyInterfaceConfig

    system_Echo "Changing hostname..."
    system_SetHostname "passdora"
    
    system_Echo "Reducing GPU memory..."
    system_SetGpuMem 16
    
    system_Echo "Appending autostart commands..."
    system_appendAutostartCommands

    system_Echo "Setting up USB auto-mount..."
    system_setupUsbAutomount

    # Ask if logging to USB should be enabled
    read -p "Should the system log to a USB-drive? (y/n): " CHOICE
    case ${CHOICE} in
        y|Y)
            echo "System will log to USB..."

            system_Echo "Setting up fstab..."
            system_setupFstab

            system_Echo "Setting up logging to usb..."
            system_setupUsbLogs
            ;;
        n|N|*)
            echo "System will NOT log to USB"
            ;;
    esac

    system_Echo "Creating Crons..."
    system_createCrons
    
    system_Echo "Enabling I2C..."
    system_enableI2C
    
    system_Echo "Setting user permissions..."
    system_setPermissions

    system_Echo "Importing GPG key..."
    system_importGpgKey
}
