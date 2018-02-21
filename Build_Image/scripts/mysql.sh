#!/usr/bin/env bash

QUIQQER_DB_NAME="quiqqer"
QUIQQER_DB_USER_NAME="quiqqer"
QUIQQER_DB_USER_PW="quiqqer"

# Todo: set MySQL root-User PW?


# Ecgos a message from mysql context
function mysql_Echo() {
    echo -e "\033[0;32mmysql: $1\033[0m"
}


# Creates the QUIQQER database
function mysql_CreateDB() {
    sudo mysql -e "CREATE DATABASE $QUIQQER_DB_NAME;";
}


# Creates the QUIQQER database user
function mysql_CreateUser() {
    sudo mysql -e "CREATE USER '$QUIQQER_DB_USER_NAME'@'localhost' IDENTIFIED BY '$QUIQQER_DB_USER_PW';";
}


# Grants the QUIQQER database user acces to the QUIQQER database
function mysql_GrantPermissions() {
    sudo mysql -e "GRANT ALL ON $QUIQQER_DB_NAME.* TO '$QUIQQER_DB_USER_NAME'@'localhost';";
}


# Executes the mysql steps in correct order
function mysql_ExecuteStep() {
    mysql_Echo "Creating QUIQQER DB..."
    mysql_CreateDB
    
    mysql_Echo "Creating QUIQQER DB-User..."
    mysql_CreateUser
    
    mysql_Echo "Granting QUIQQER DB-User access to QUIQQER DB..."
    mysql_GrantPermissions
}

