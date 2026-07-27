#!/bin/bash
set -e

PORT=${API_INT_PORT:-1111}
WORKERS=${API_WORKERS:-1}

echo "app is starting..."

if [ "${PROD,,}" = "true" ]; then
    echo "Running in production mode..."
    fastapi run main.py --host 0.0.0.0 --port "$PORT" --workers "$WORKERS"
else
    echo "Running in development mode..."
    fastapi dev main.py --host 0.0.0.0 --port "$PORT"
fi
