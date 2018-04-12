#!/usr/bin/env bash

################################################
#                                              #
# This file contains functions to set up nginx #
#                                              #
# Author: Jan Wennrich (PCSG)                  #
#                                              #
################################################

NGINX_PATH="/etc/nginx"
NGINX_TIMEOUT=600

# Echos a message from nginx context
function nginx_Echo() {
    echo -e "\033[0;32mnginx: $1\033[0m"
}


# Imports the QUIQQER generated nginx site-config into the nginx site-folder 
function nginx_importConfig() {
    sudo cp $NGINX_PATH/sites-available/default $NGINX_PATH/sites-available/default.bk
    echo "include /var/www/html/etc/nginx/nginx.conf;" | sudo tee $NGINX_PATH/sites-available/default > /dev/null
}


function nginx_SetTimeout() {
    sudo sed -i "s/http {/http {\n\n\tfastcgi_read_timeout 600;/" /etc/nginx/nginx.conf
}


function nginx_statusPage_download() {
    sudo wget https://github.com/shevabam/ezservermonitor-web/archive/v2.5.tar.gz -O /var/www/status.tgz
}


function nginx_statusPage_extract() {
    sudo tar -xzf /var/www/status.tgz -C /var/www/

    sudo mv /var/www/ezservermonitor-web-2.5 /var/www/status

    sudo chown www-data:www-data -R /var/www/status
}

function nginx_statusPage_enable() {
    sudo cp files/status /etc/nginx/sites-available/

    sudo ln -s /etc/nginx/sites-available/status /etc/nginx/sites-enabled/
}



# Executes the nginx setup steps in correct order
function nginx_ExecuteStep() {
    nginx_Echo "Importing QUIQQER config..."
    nginx_importConfig

    nginx_Echo "Downloading system-status page..."
    nginx_statusPage_download

    nginx_Echo "Extracting system-status page..."
    nginx_statusPage_extract

    nginx_Echo "Enabling system-status page..."
    nginx_statusPage_enable
    
    nginx_Echo "Setting timeout to $NGINX_TIMEOUT seconds..."
    nginx_SetTimeout
}

