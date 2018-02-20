#!/usr/bin/env bash

NGINX_PATH="/etc/nginx"

function nginx_Echo() {
    echo -e "\033[0;32mnginx: $1\033[0m"
}


function nginx_importConfig() {
    sudo cp $NGINX_PATH/sites-available/default $NGINX_PATH/sites-available/default.bk
    echo "include /var/www/html/etc/nginx/nginx.conf;" | sudo tee $NGINX_PATH/sites-available/default > /dev/null
}


function nginx_ExecuteStep() {
    mysql_Echo "Importing QUIQQER config..."
    nginx_importConfig
}

