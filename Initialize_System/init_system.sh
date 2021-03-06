#!/usr/bin/env bash

########################################################################################
#                                                                                      #
# This script initializes the Passdora system when the system boots for the first time #
#                                                                                      #
# Author: Jan Wennrich (PCSG)                                                          #
#                                                                                      #
########################################################################################


# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT


. functions.sh
. ../Build_Image/scripts/system.sh



if ! isInitialized; then
    coloredEcho "Initializing Passdora..."

    # If connected to the internet...
#    if ping -q -c 1 -W 1 google.com > /dev/null; then
#        coloredEcho "Updating packages..."
#        sudo apt update -y
#        sudo apt upgrade -y
#    fi

    # Wait for MySQL
    while [ $(service mysql status | grep "active (running)" | wc -l) -ne 1 ]; do
       echo "Waiting for MySQL..."
       sleep 1
    done

    initPasswordFile

    # Set ssh password
    SSH_PW=$(getRandomString 15)
    setSshPassword $SSH_PW 
    coloredEcho "ssh password set to: \033[0m$SSH_PW"   
    storePassword "ssh_pw" $SSH_PW 
    
    
    # Set database password
    DB_PW=$(getRandomString 15)
    setDbPassword $DB_PW
    coloredEcho "Database quiqqer-user password set to: \033[0m$DB_PW"   
    storePassword "db_pw" $DB_PW
    
    
    # Reset QUIQQER admin-user password to random value
    QUIQQER_PW=$(resetQuiqqerPassword)    
    coloredEcho "QUIQQER admin password set to: \033[0m$QUIQQER_PW"   
    storePassword "quiqqer_pw" $QUIQQER_PW
    
    
    #Generate snakeoil SSL certs
    coloredEcho "Generating snakeoil certificates..."
    generateSnakeoilCerts
    
    
    # Restart nginx & php-fpm
    system_RestartWebserverComponents


    # Generate and store restore key
    initRestoreKeyFile
    RESTORE_KEY=$(generateRestoreKey)
    coloredEcho "Restore Key: \033[0m${RESTORE_KEY}"
    storeRestoreKey ${RESTORE_KEY}


    # Creates a file to set the system as initialized
    setInitialized
    
        
    coloredEcho "Initialization completed."
fi

