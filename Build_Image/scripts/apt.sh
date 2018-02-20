#!/usr/bin/env bash

. scripts/system.sh

APT_UPDATE_COMPLETE_FILE="/etc/passdora_apt_complete"


function apt_Echo() {
    echo -e "\033[0;32mapt: $1\033[0m"
}


function apt_IsUpdated() {
    test -f "$APT_UPDATE_COMPLETE_FILE"
}


function apt_Update() {
    sudo apt update -y
}


function apt_FullUpgrade() {
    sudo apt full-upgrade -y
}


function apt_InstallPackages() {
    sudo apt install ssl-cert nginx mysql-server php-fpm php-curl php-dom php-mbstring php-xml php-zip php-imagick php-gd php-mysql php-bcmath php-dev libsodium-dev php-libsodium -y
}

    
function apt_WriteUpdateCompleteFile() {
    sudo touch "$APT_UPDATE_COMPLETE_FILE"
}


function apt_AutoRemove() {
    sudo apt autoremove -y
}


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
