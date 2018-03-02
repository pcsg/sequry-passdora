#!/usr/bin/env bash

#######################################################
#                                                     #
# This file contains functions to set up apt packages #
#                                                     #
# Author: Jan Wennrich (PCSG)                         #
#                                                     #
#######################################################

. scripts/system.sh


APT_UPDATE_COMPLETE_FILE="/etc/passdora_apt_complete"


# Echos a message from apt context
function apt_Echo() {
    echo -e "\033[0;32mapt: $1\033[0m"
}


# Checks if the apt setup was already run
function apt_IsUpdated() {
    test -f "$APT_UPDATE_COMPLETE_FILE"
}


# Updates the apt package list
function apt_Update() {
    sudo apt update -y
}


# Upgrades all packages
function apt_FullUpgrade() {
    sudo apt full-upgrade -y
}


# Installs all dependencies
function apt_InstallPackages() {
    sudo apt install ssl-cert nginx mysql-server php-fpm php-curl php-dom php-mbstring php-xml php-zip php-imagick php-gd php-mysql php-bcmath php-dev libsodium-dev php-libsodium python-smbus i2c-tools -y
}

    
# Stores a file to set the apt setup as run
function apt_WriteUpdateCompleteFile() {
    sudo touch "$APT_UPDATE_COMPLETE_FILE"
}


# Autoremoves unused packages
function apt_AutoRemove() {
    sudo apt autoremove -y
}


# Executes the apt steps
function apt_ExecuteStep() {   
    if ! apt_IsUpdated; then
        apt_Echo "Updating package list..."
        apt_Update
              
        apt_Echo "Upgrading default packages..."
        apt_FullUpgrade
       
        apt_Echo "Installing dependencies..."
        apt_InstallPackages
                      
        apt_Echo "Cleaning up..."
        apt_AutoRemove
        
        apt_Echo "Storing apt complete state..."
        apt_WriteUpdateCompleteFile
        
        apt_Echo "Rebooting..."
        system_Reboot
    fi
}
