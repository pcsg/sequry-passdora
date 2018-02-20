#!/usr/bin/env bash

function quiqqer_Echo() {
    echo -e "\033[0;32mquiqqer: $1\033[0m"
}


function quiqqer_DownloadSetup() {
    sudo wget https://update.quiqqer.com/quiqqer.tgz -O /var/www/html/quiqqer.tgz
}


function quiqqer_ExtractSetup() {
	sudo tar -xzf /var/www/html/quiqqer.tgz -C /var/www/html/
}


function quiqqer_CleanupSetup() {
	sudo rm /var/www/html/quiqqer.tgz 
}


function quiqqer_SetDirPermissions() {
    sudo chown -R www-data:www-data /var/www/html/
}


function quiqqer_CopyPresets() {
    # Template Preset
    sudo cp files/default.json /var/www/html/templates/presets/default.json
    
    # Setup Preset
    sudo mkdir -p /var/www/html/var/tmp
    sudo cp files/setup.json /var/www/html/var/tmp/setup.json
}


function quiqqer_StartSetup() {
    (
        cd /var/www/html
        sudo php setup.php --no-interaction
    )
}


function quiqqer_GenerateNginxConfig() {
    (
        cd /var/www/html
        sudo php quiqqer.php --username=admin --password=admin --tool=quiqqer:nginx
    ) 
}


function quiqqer_importSnakeoilCerts() {
    sudo cp /etc/ssl/certs/ssl-cert-snakeoil.pem /var/www/html/etc/nginx/certs/cert.pem
    sudo cp /etc/ssl/private/ssl-cert-snakeoil.key /var/www/html/etc/nginx/certs/key.pem
}


function quiqqer_ExecuteStep() {
    quiqqer_Echo "Downloading setup..."
    quiqqer_DownloadSetup
    
    quiqqer_Echo "Extracting setup..."
    quiqqer_ExtractSetup
    
    
    quiqqer_Echo "Copying presets..."
    quiqqer_CopyPresets
    
    quiqqer_Echo "Starting setup..."
    quiqqer_StartSetup
  
    quiqqer_Echo "Generating nginx config..."
    quiqqer_GenerateNginxConfig

    quiqqer_Echo "Importing snakeoil certificates..."
    quiqqer_importSnakeoilCerts
    
    
    quiqqer_Echo "Setting directory permissions..."
    quiqqer_SetDirPermissions
    
    quiqqer_Echo "Cleaning up..."
    quiqqer_CleanupSetup
}

