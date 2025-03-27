#!/bin/bash
# diskusage-report.sh - Toon schijfgebruik met waarschuwingen

echo "Disk Usage Report - $(date)"
echo "--------------------------------"
df -hT | awk 'NR==1 || $6+0 >= 80 {print}' | column -t
echo
df -hT | awk '$6+0 >= 90 {print "⚠️  CRITICAL: " $7 " is over 90% used!"}'
