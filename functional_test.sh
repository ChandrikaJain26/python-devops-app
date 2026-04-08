#!/bin/bash
set -e

echo "[Functional] Starting app in background..."
nohup python -m app.main > app.log 2>&1 &
APP_PID=$!

echo "[Functional] Waiting for /health..."
for i in {1..20}; do
  if curl -sSf http://localhost:8080/health >/dev/null; then
    echo "[Functional] App is UP"
    break
  fi
  sleep 1
done

echo "[Functional] Hitting endpoints..."
curl -sSf http://localhost:8080/health
echo ""
curl -sSf http://localhost:8080/add/5/7
echo ""

echo "[Functional] Stopping app..."
kill $APP_PID || true
