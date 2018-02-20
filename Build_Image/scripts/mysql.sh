#!/usr/bin/env bash

QUIQQER_DB_NAME="quiqqer"
QUIQQER_DB_USER_NAME="quiqqer"
QUIQQER_DB_USER_PW="quiqqer"

# Todo: set MySQL root-User PW?


function mysql_Echo() {
    echo -e "\033[0;32mmysql: $1\033[0m"
}


function mysql_CreateDB() {
    sudo mysql -e "CREATE DATABASE $QUIQQER_DB_NAME;";
}


function mysql_CreateUser() {
    sudo mysql -e "CREATE USER '$QUIQQER_DB_USER_NAME'@'localhost' IDENTIFIED BY '$QUIQQER_DB_USER_PW';";
}


function mysql_GrantPermissions() {
    sudo mysql -e "GRANT ALL ON $QUIQQER_DB_NAME.* TO '$QUIQQER_DB_USER_NAME'@'localhost';";
}


function mysql_ExecuteStep() {
    mysql_Echo "Creating QUIQQER DB..."
    mysql_CreateDB
    
    mysql_Echo "Creating QUIQQER DB-User..."
    mysql_CreateUser
    
    mysql_Echo "Granting QUIQQER DB-User access to QUIQQER DB..."
    mysql_GrantPermissions
}

