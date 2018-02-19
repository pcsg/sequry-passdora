#!/usr/bin/env bash

. scripts/apt.sh
. scripts/mysql.sh
. scripts/php.sh

apt_ExecuteStep
mysql_ExecuteStep
php_ExecuteStep
