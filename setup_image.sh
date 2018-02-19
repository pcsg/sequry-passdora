#!/usr/bin/env bash

. scripts/apt.sh
. scripts/mysql.sh
. scripts/php.sh
. scripts/quiqqer.sh

apt_ExecuteStep
mysql_ExecuteStep
php_ExecuteStep
quiqqer_ExecuteStep
