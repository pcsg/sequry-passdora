#!/usr/bin/env bash

IS_INITIALIZED_FILE="/etc/passdora_is_initialized"

function coloredEcho() {
    echo -e "\033[0;32m$1\033[0m"
}

function getRandomString() {
    head /dev/urandom | tr -dc A-Za-z0-9 | head -c15
}


function isInitialized() {
    test -f "$IS_INITIALIZED_FILE"
}


function setSshPassword() {
    echo "pi:$1" | sudo chpasswd
}


function setDbPassword() {
    sudo mysql -e "SET PASSWORD FOR quiqqer@localhost = PASSWORD('$1');"
    sudo sed -i "s/password=\"quiqqer\"/password=\"$1\"/" /var/www/html/etc/conf.ini.php
}


function setQuiqqerPassword() {
    echo "todo"
    # sudo php /var/www/html/quiqqer.php password-reset
}

function storePassword() {
    echo "$1=$2" | sudo tee --append /etc/passdora_passwords.ini > /dev/null
}

