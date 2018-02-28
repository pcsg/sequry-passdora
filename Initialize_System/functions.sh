#!/usr/bin/env bash

IS_INITIALIZED_FILE="/etc/passdora_is_initialized"


# Echos a green message
function coloredEcho() {
    echo -e "\033[0;32m$1\033[0m"
}


# Returns a random 15-digit alphanumeric string
function getRandomString() {
    head /dev/urandom | tr -dc A-HJ-NP-Z1-9 | head -c${1}
}


# Returns if the initialize script was already run
function isInitialized() {
    test -f "$IS_INITIALIZED_FILE"
}


# Creates the file to set the script as initialized
function setInitialized() {
    sudo touch $IS_INITIALIZED_FILE
}


# Sets the ssh password to the given parameter
function setSshPassword() {
    echo "pi:$1" | sudo chpasswd
}


# Sets the QUIQQER database password to the given parameter and updates the QUIQQER config
function setDbPassword() {
    sudo mysql -e "SET PASSWORD FOR quiqqer@localhost = PASSWORD('$1');"
    sudo sed -i "s/password=\".*\"/password=\"$1\"/" /var/www/html/etc/conf.ini.php
}


# Sets the QUIQQER admin-user password to the given parameter
function resetQuiqqerPassword() {
    printf "admin\ny\ny\n" | sudo php /var/www/html/quiqqer.php password-reset | sed -n -e "s/.*password is '\(.*\)'.*/\1/p"
}


function initPasswordFile() {
    echo ";<?php echo \"You should stop sniffing around...\"; exit; ?>" | sudo tee --append /var/www/html/etc/passdora_passwords.ini.php > /dev/null
}


# Writes a password to the passdora passwords file
function storePassword() {
    echo "$1=\"$2\"" | sudo tee --append /var/www/html/etc/passdora_passwords.ini.php > /dev/null
}


function generateSnakeoilCerts() {
    sudo make-ssl-cert generate-default-snakeoil --force-overwrite 

    sudo cp /etc/ssl/certs/ssl-cert-snakeoil.pem /var/www/html/etc/nginx/certs/cert.pem
    sudo cp /etc/ssl/private/ssl-cert-snakeoil.key /var/www/html/etc/nginx/certs/key.pem
}

