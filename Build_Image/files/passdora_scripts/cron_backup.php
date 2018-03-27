<?php

define('QUIQQER_SYSTEM', true);
require_once '/var/www/html/packages/header.php';

$timestamp = time();

$Config     = QUI::getPackage('sequry/passdora')->getConfig();

$lastBackup = $Config->get('backup', 'last_backup');
$backupInterval = $Config->get('backup', 'interval') * 60 * 60;

if ($timestamp - $lastBackup >= $backupInterval) {
    exec('sudo ./backup.sh', $output, $returnCode);

    if ($returnCode === 0) {
        $Config->setValue('backup', 'last_backup', $timestamp);
        $Config->save();
    }
}
