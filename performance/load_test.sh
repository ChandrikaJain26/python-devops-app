#!/bin/bash
set -e
echo "[Perf] Running 200 requests to /health..."
for i in {1..200}; do
  curl -s http://localhost:8080/health >/dev/null
done
echo "[Perf] Done"
