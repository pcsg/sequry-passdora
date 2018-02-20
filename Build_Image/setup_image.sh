#!/usr/bin/env bash

# exit when any command fails
set -e

# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG

# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

. scripts/apt.sh
. scripts/mysql.sh
. scripts/php.sh
. scripts/quiqqer.sh
. scripts/nginx.sh
. scripts/system.sh

echo -e "\033[0;32mStarting setup...\033[0m"

#apt_ExecuteStep
mysql_ExecuteStep
#php_ExecuteStep
quiqqer_ExecuteStep
#nginx_ExecuteStep
#system_ExecuteStep

echo -e "\033[0;32mSetup completed.\033[0m"

exit 0
