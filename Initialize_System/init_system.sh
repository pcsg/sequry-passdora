#!/usr/bin/env bash

# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

. functions.sh

if ! isInitialized; then
    coloredEcho "Initializing Passdora..."

    # If connected to the internet...
    if ping -q -c 1 -W 1 google.com >/dev/null; then
        coloredEcho "Updating packages..."
        sudo apt update -y
        sudo apt upgrade -y
    fi

    initPasswordFile

    # Set ssh password
    SSH_PW=$(getRandomString)    
    setSshPassword $SSH_PW 
    coloredEcho "ssh password set to: \033[0m$SSH_PW"   
    storePassword "ssh_pw" $SSH_PW 
    
    
    # Set database password
    DB_PW=$(getRandomString)
    setDbPassword $DB_PW
    coloredEcho "Database quiqqer-user password set to: \033[0m$DB_PW"   
    storePassword "db_pw" $DB_PW
    
    
    # Reset QUIQQER admin-user password to random value
    QUIQQER_PW=$(resetQuiqqerPassword)    
    coloredEcho "QUIQQER admin password set to: \033[0m$QUIQQER_PW"   
    storePassword "quiqqer_pw" $QUIQQER_PW
    
    setInitialized
        
    coloredEcho "Initialization completed."
fi

