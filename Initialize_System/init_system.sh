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

    :'
    SSH_PW=$(getRandomString)    
    setSshPassword $SSH_PW 
    coloredEcho "ssh password set to: \033[0m$SSH_PW"   
    storePassword "ssh_pw" $SSH_PW 
    '
    
    :'
    DB_PW=$(getRandomString)
    setDbPassword $DB_PW
    coloredEcho "Database quiqqer-user password set to: \033[0m$DB_PW"   
    storePassword "db_pw" $DB_PW
    '
    
    coloredEcho "Initialization completed."
fi

