#!/bin/bash

####################################################################
# Writes and reads to/from a specified file and outputs the speed. #
#                                                                  #
# Author: PCSG (Jan Wennrich)                                      #
#                                                                  #
# Inspired by: https://github.com/aikoncwd/rpi-benchmark           #
####################################################################

# Check if enough arguments
if [ ! $# -eq 2 ]
  then
    echo "Not enough arguments, exiting."
    echo "Usage: $0 <file_to_write_to> <MiB_to_write>"
    exit 1
fi

# Check if file to write to already exists
if [ -e $1 ]
then
    read -r -p "The file $1 already exists. Do you want to overwrite it? [y/N] " response

    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
    then
	echo "Aborting."
        exit 0
    fi
fi

# Check if root
[ "$(whoami)" == "root" ] || { echo "Must be run as root!"; exit 1; }

echo "Will write $2 MiB to $1"

read -r -p "Are you sure? [y/N] " response

if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    echo "Aborting."
    exit 0
fi

# Write to specified file the specified amount of blocks/MiB
echo "Writing $2 MiB to $1..."
rm -f $1 && sync && dd if=/dev/zero of=$1 bs=1M count=$2 conv=fsync 2>&1 | grep -v records

# Read content of the written file
echo "Reading from $1..."
echo -e 3 > /proc/sys/vm/drop_caches && sync && dd if=$1 of=/dev/null bs=1M 2>&1 | grep -v records

# Remove the written file
rm -f $1

exit 0
