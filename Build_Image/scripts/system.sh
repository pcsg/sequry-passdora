#!/usr/bin/env bash

# Echos a message from system context
function system_Echo() {
    echo -e "\033[0;32msystem: $1\033[0m"
}


# Reboots the system
function system_Reboot() {
    sudo shutdown now -r
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


# Executes the system setup steps in correct order
function system_ExecuteStep() {
    system_Echo "Changing hostname..."
    system_SetHostname "passdora"
    
    system_Echo "Reducing GPU memory..."
    system_SetGpuMem 16
}
