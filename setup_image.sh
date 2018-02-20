#!/usr/bin/env bash

. scripts/apt.sh
. scripts/mysql.sh
. scripts/php.sh
. scripts/quiqqer.sh
. scripts/nginx.sh
. scripts/system.sh

echo -e "\033[0;32mapt: Starting setup...\033[0m"

#apt_ExecuteStep
#mysql_ExecuteStep
#php_ExecuteStep
#quiqqer_ExecuteStep
#nginx_ExecuteStep
system_ExecuteStep

echo -e "\033[0;32mapt: Setup completed.\033[0m"
