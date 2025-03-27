#!/bin/bash
# service-monitor.sh - Controleer en herstart kritieke services

SERVICES=("nginx" "mysql")
for svc in "${SERVICES[@]}"; do
  if ! systemctl is-active --quiet "$svc"; then
    echo "⚠️  $svc is down. Herstarten..."
    sudo systemctl restart "$svc"
  else
    echo "✅ $svc is actief"
  fi
done
