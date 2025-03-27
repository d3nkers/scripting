#!/bin/bash
# user-audit.sh - Gebruikers, sudo-rechten en status

echo "Sudo group members:"
getent group sudo

echo -e "\nLaatste logins:"
lastlog | grep -v 'Never'

echo -e "\nGeblokkeerde accounts:"
while IFS=: read -r user _; do
  status=$(passwd -S "$user" 2>/dev/null)
  if [[ $status == *" L "* ]]; then
    echo "$user is locked"
  fi
done < /etc/passwd
