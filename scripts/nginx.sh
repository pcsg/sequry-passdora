#!/usr/bin/env bash

# Import vagrant-shell-scripts
#SCRIPT_DIR="$(dirname "$0")"
#"$SCRIPT_DIR/vagrant-shell-scripts/ubuntu.sh"

update_complete_file = "/etc/passdora_apt_complete"

QUIQQER_DB_NAME = "quiqqer"
QUIQQER_DB_USER_NAME = "quiqqer"
QUIQQER_DB_USER_PW = "quiqqer"

if [! -f "$update_complete_file"]; then

    # Check if device is online
    wget -q --spider https://update.quiqqer.com

    if [ $? -eq 1 ]; then
        echo "You need an internet connection to run the script."
        exit
    fi

    sudo apt update -y
    sudo apt full-upgrade -y
    sudo apt install php nginx mysql php-curl php-dom php-mbstring php-xml php-zip php-imagick php-gd php-mysql php-bcmath php-dev libsodium-dev php-libsodium -y
    
    sudo touch "$update_complete_file"
    
    # Necessary?
    sudo shutdown now -r
fi


# Todo: set MySQL root-User PW?


# Create QUIQQER DB & User and grant him access to the DB
sql_query = "CREATE DATABASE $QUIQQER_DB_NAME; CREATE USER '$QUIQQER_DB_USER_NAME'@'localhost' IDENTIFIED BY '$QUIQQER_DB_USER_PW'; GRANT ALL ON $QUIQQER_DB_NAME.* TO '$QUIQQER_DB_USER_NAME'@'localhost';"

mysql -u "root" -e "$sql_query";


