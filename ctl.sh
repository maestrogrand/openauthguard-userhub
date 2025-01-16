#!/bin/bash

ENV=${1:-dev}
VENV_NAME="userhub_env"

if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv $VENV_NAME
    echo "Virtual environment created."
fi

source $VENV_NAME/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

export PYTHONPATH="$PWD/src:$PYTHONPATH"

ENV_FILE=".env.$ENV"
if [ -f "$ENV_FILE" ]; then
    set -o allexport
    source $ENV_FILE
    set +o allexport
    echo "Environment set to $ENV"
else
    echo "No environment file found for $ENV."
    exit 1
fi

PORT=$(python3 -c "from src.core.config import settings; print(settings.port)" 2>/dev/null)
if [ -z "$PORT" ]; then
    echo "Port not set in configuration. Exiting."
    deactivate
    exit 1
fi

echo "Attempting to kill any processes on port ${PORT}"
lsof -t -i:${PORT} | xargs kill -9

echo "Verifying that port ${PORT} is free..."
if lsof -t -i:${PORT}; then
    echo "Port ${PORT} is still in use. Cannot start Userhub service."
    deactivate
    exit 1
else
    echo "Port ${PORT} is free. Starting Userhub service."
fi

uvicorn src.main:app --host 0.0.0.0 --port $PORT --reload

deactivate

echo "Cleaning up..."
rm -rf $VENV_NAME
find src/ -type d -name '__pycache__' -exec rm -r {} +

echo "Done."
