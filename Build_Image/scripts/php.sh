#!/usr/bin/env bash

##############################################
#                                            #
# This file contains functions to set up php #
#                                            #
# Author: Jan Wennrich (PCSG)                #
#                                            #
##############################################

PHP_DIRECTORY="/etc/php/7.0"

PHP_DEFAULT_TIMEZONE="Europe/Berlin"
PHP_UPLOAD_LIMIT="8M"
PHP_TIMEOUT=600


# Echos a message from php context
function php_Echo() {
    echo -e "\033[0;32mphp: $1\033[0m"
}


# Appends a given setting plus value (e.g. someSetting=value) the php configs
function php_AppendToConfig() {
    echo $1 | sudo tee --append $PHP_DIRECTORY/cli/conf.d/passdora.ini > /dev/null
    echo $1 | sudo tee --append $PHP_DIRECTORY/fpm/conf.d/passdora.ini > /dev/null
}


# Writes the default timezone to the php configs 
function php_SetTimezone() {
    php_AppendToConfig "date.timezone = $PHP_DEFAULT_TIMEZONE"
}


# Writes the upload limit to the php configs
function php_SetUploadLimit() {
    php_AppendToConfig "upload_max_filesize = $PHP_UPLOAD_LIMIT"
}


function php_SetTimeouts() {
    sudo sed -i "s/max_execution_time = [0-9]*/max_execution_time = $1/" /etc/php/7.0/fpm/php.ini
    sudo sed -i "s/max_execution_time = [0-9]*/max_execution_time = $1/" /etc/php/7.0/cli/php.ini
}


# Executes the php setup steps in correct order
function php_ExecuteStep() {
    php_Echo "Setting default timezone..."
    php_SetTimezone
    
    php_Echo "Setting upload limit..."
    php_SetUploadLimit
    
    php_Echo "Setting timeouts to $PHP_TIMEOUT seconds..."
    php_SetTimeouts $PHP_TIMEOUT
}

