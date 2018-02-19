#!/usr/bin/env bash

PHP_DIRECTORY="/etc/php/7.0"

PHP_DEFAULT_TIMEZONE="Europe/Berlin"
PHP_UPLOAD_LIMIT="8M"


function php_Echo() {
    echo -e "\033[0;32mphp: $1\033[0m"
}


function php_AppendToConfig() {
    echo $1 | sudo tee --append $PHP_DIRECTORY/cli/conf.d/passdora.ini > /dev/null
    echo $1 | sudo tee --append $PHP_DIRECTORY/fpm/conf.d/passdora.ini > /dev/null
}


function php_SetTimezone() {
    php_AppendToConfig "date.timezone = $PHP_DEFAULT_TIMEZONE"
}


function php_SetUploadLimit() {
    php_AppendToConfig "upload_max_filesize = $PHP_UPLOAD_LIMIT"
}


function php_ExecuteStep() {
    php_Echo "Setting default timezone..."
    php_SetTimezone
    
    php_Echo "Setting upload limit..."
    php_SetUploadLimit
}

