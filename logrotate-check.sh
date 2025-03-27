#!/bin/bash
# logrotate-check.sh - Toon configuratie en potentiële problemen

echo "Logrotate configurations in /etc/logrotate.d:"
echo "---------------------------------------------"
for file in /etc/logrotate.d/*; do
  echo "→ $file:"
  grep -E '^(rotate|daily|weekly|monthly)' "$file"
  echo
done
