#!/bin/bash

ENV=$2
VENV_NAME="userhub_env"

create_venv() {
    if [ ! -d "$VENV_NAME" ]; then
        python3 -m venv "$VENV_NAME"
        echo "Virtual environment created."
    fi
}

activate_venv() {
    source "$VENV_NAME/bin/activate"
}

install_dependencies() {
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
}

setup_environment() {
    export PYTHONPATH="$PWD/src:$PYTHONPATH"

    ENV_FILE=".env.$ENV"
    if [ -f "$ENV_FILE" ]; then
        set -o allexport
        source "$ENV_FILE"
        set +o allexport
        echo "Environment set to $ENV"
    else
        echo "No environment file found for $ENV."
        exit 1
    fi
}

get_port() {
    PORT=$(python3 -c "from src.core.config import settings; print(settings.port)" 2>/dev/null)
    if [ -z "$PORT" ]; then
        echo "Port not set in configuration. Exiting."
        deactivate
        exit 1
    fi
}

free_port() {
    echo "Attempting to kill any processes on port ${PORT}..."
    lsof -t -i:${PORT} | xargs kill -9

    echo "Verifying that port ${PORT} is free..."
    if lsof -t -i:${PORT}; then
        echo "Port ${PORT} is still in use. Cannot start Userhub service."
        deactivate
        exit 1
    fi
}

start_service() {
    if [ -z "$ENV" ]; then
        echo "Error: Environment must be specified."
        echo "Usage: $0 start [environment]"
        exit 1
    fi

    create_venv
    activate_venv
    install_dependencies
    setup_environment
    get_port
    free_port

    echo "Starting Userhub service on port ${PORT}..."
    uvicorn src.main:app --host 0.0.0.0 --port $PORT --reload

    echo "Service exited. Performing cleanup..."
    deactivate
    cleanup
}

lint_code() {
    create_venv
    activate_venv
    install_dependencies

    echo "Running code linting..."
    black --check src
    flake8 src
    echo "Linting complete."

    deactivate
}

format_code() {
    create_venv
    activate_venv
    install_dependencies

    echo "Running code formatting..."
    black src tests
    echo "Formatting complete."

    deactivate
}

cleanup() {
    echo "Cleaning up..."
    rm -rf "$VENV_NAME"
    find src/ -type d -name '__pycache__' -exec rm -r {} +
    echo "Cleanup complete."
}

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 {start|lint|format|cleanup} [environment]"
    exit 1
fi

case "$1" in
start)
    start_service
    ;;
lint)
    lint_code
    ;;
format)
    format_code
    ;;
cleanup)
    cleanup
    ;;
*)
    echo "Invalid argument: $1"
    echo "Usage: $0 {start|lint|format|cleanup} [environment]"
    exit 1
    ;;
esac
