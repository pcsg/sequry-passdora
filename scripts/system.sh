#!/usr/bin/env bash

function system_Echo() {
    echo -e "\033[0;32msystem: $1\033[0m"
}


function system_Reboot() {
    sudo shutdown now -r
}


function system_ChangeHostname() {
    echo "passdora" | sudo tee /etc/hostname > /dev/null
    sudo sed -i "s/127\.0\.1\.1.*raspberrypi/127.0.1.1 passdora/g" /etc/hosts
}


function system_ReduceGpuMem() {
    echo "gpu_mem=16" | sudo tee --append /boot/config.txt > /dev/null
}

function system_ExecuteStep() {
    system_Echo "Changing hostname..."
    system_ChangeHostname
    
    system_Echo "Reducing GPU memory..."
    system_ReduceGpuMem
}
