#!/bin/bash
# backup-home.sh - Maak back-up van /home naar /mnt/backup met datum

backupdir="/mnt/backup/home-$(date +%F)"
mkdir -p "$backupdir"
rsync -av --delete /home/ "$backupdir"
echo "Back-up voltooid in: $backupdir"
