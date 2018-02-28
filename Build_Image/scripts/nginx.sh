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


# Executes the nginx setup steps in correct order
function nginx_ExecuteStep() {
    nginx_Echo "Importing QUIQQER config..."
    nginx_importConfig
    
    nginx_Echo "Setting timeout to $NGINX_TIMEOUT seconds..."
    nginx_SetTimeout
}

