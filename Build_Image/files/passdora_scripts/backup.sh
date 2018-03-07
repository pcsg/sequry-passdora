#!/usr/bin/env bash

#######################################################################
#                                                                     #
# Script that creates an GPG encrypted backup of the Passdora system  #
# Backup includes:                                                    #
#   - QUIQQER database                                                #
#   - QUIQQER etc/ folder                                             #
#                                                                     #
# Author: Jan Wennrich (PCSG)                                         #
#                                                                     #
#######################################################################

# Current date in format YYYY_MM_DD
DATE=$(date '+%F')

# Folder where all backups are stored
GENERAL_BACKUP_FOLDER=/home/pi/backups

# Folder where files are temporarily copied to
TEMP_BACKUP_FOLDER=${GENERAL_BACKUP_FOLDER}/${DATE}

# Location where the encrypted backup file will be stored
ENCRYPTED_BACKUP_FILE=${GENERAL_BACKUP_FOLDER}/${DATE}.tgz.gpg

# Location where usb-drives will be mounted to
USB_MOUNTING_POINT=/media/usb


# Parse restore-key .ini-file and assign variable containg the key
source <(grep = /var/www/html/etc/passdora_restore_key.ini.php)
RESTORE_KEY=$restore_key


# Create backup folder
echo "Creating backup folder..."
mkdir -p ${TEMP_BACKUP_FOLDER}

# TODO: copy backups directly into tar instead of placing them in a folder first

# Dump database
echo "Dumping database..."
sudo mysqldump --databases quiqqer > ${TEMP_BACKUP_FOLDER}/database.sql

# Copy QUIQQER etc/ folder
echo "Copying QUIQQER etc/ folder..."
sudo cp -r /var/www/html/etc ${TEMP_BACKUP_FOLDER}/

# Tar everything in the temporary backup directory and then encrypt it
(
    cd ${TEMP_BACKUP_FOLDER}
    echo "Packing everything into an encrypted archive..."
    tar -cz * | gpg -c --batch --yes --passphrase ${RESTORE_KEY} -o ${ENCRYPTED_BACKUP_FILE}
)

# Remove temp folder
echo "Removing temp folder..."
sudo rm -rf ${TEMP_BACKUP_FOLDER}


# If USB-device is connected...
if [ mountpoint -q ${USB_MOUNTING_POINT} ]; then

    echo "Copying backup to USB-drive..."

    # Create the backup folder
    mkdir ${USB_MOUNTING_POINT}/passdora-backups/

    # Copy the backup
    sudo cp ${ENCRYPTED_BACKUP_FILE} ${USB_MOUNTING_POINT}/passdora-backups/

    echo "Backup successfully copied to USB-drive"
fi
