#!/usr/bin/env bash

. scripts/apt.sh

if ((!apt_IsUpdated)); then 
    echo "not up to date"    
else
    echo "up to date"

fi

