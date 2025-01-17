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
    PORT=$(python3 -c \
        "from src.core.config import settings; print(settings.port)" 2>/dev/null)
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

increment_version() {
    VERSION_LINE=$(grep 'SERVICE_VERSION' src/core/version.py)
    VERSION=$(echo $VERSION_LINE | sed -E "s/.*\"(.*)\"/\1/")
    echo "Current version: $VERSION"
    IFS='.' read -ra VERSION_PARTS <<<"$VERSION"

    MAJOR=${VERSION_PARTS[0]}
    MINOR=${VERSION_PARTS[1]}
    PATCH=${VERSION_PARTS[2]}

    PS3='Enter which part to increment (1 for MAJOR, 2 for MINOR, 3 for PATCH): '
    options=("MAJOR" "MINOR" "PATCH")
    select opt in "${options[@]}"; do
        case $REPLY in
        1)
            echo "Incrementing MAJOR version from $VERSION"
            MAJOR=$((MAJOR + 1))
            MINOR=0
            PATCH=0
            break
            ;;
        2)
            echo "Incrementing MINOR version from $VERSION"
            MINOR=$((MINOR + 1))
            PATCH=0
            break
            ;;
        3)
            echo "Incrementing PATCH version from $VERSION"
            PATCH=$((PATCH + 1))
            break
            ;;
        *)
            echo "Invalid option. Please select 1, 2, or 3."
            ;;
        esac
    done

    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    echo "New version: $NEW_VERSION"

    sed -i '' -e "s/SERVICE_VERSION = \".*\"/SERVICE_VERSION = \"$NEW_VERSION\"/" src/core/version.py
    echo "Updated version in src/core/version.py"
}

git_push() {
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Enter commit message:"
    read commit_message
    git add .
    git commit -m "$commit_message"
    git push origin $current_branch

    echo "Changes pushed to $current_branch"
}

commit_commit() {
    increment_version
    git_push
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
    cleanup
}

format_code() {
    create_venv
    activate_venv
    install_dependencies

    echo "Running code formatting..."
    if [ -d "tests" ]; then
        black src tests
    else
        black src
    fi
    echo "Formatting complete."

    deactivate
    cleanup
}

run_tests() {
    create_venv
    activate_venv
    install_dependencies
    setup_environment

    echo "Running tests..."
    pytest tests
    echo "Testing complete."

    deactivate
    cleanup_tests_env
    cleanup
}

cleanup() {
    echo "Cleaning up..."
    rm -rf "$VENV_NAME"
    find src/ -type d -name '__pycache__' -exec rm -r {} +
    echo "Cleanup complete."
}

cleanup_tests_env() {
    echo "Cleaning up test environment directories..."
    rm -rf tests/__pycache__
    rm -rf .pytest_cache
    echo "Test environment cleanup complete."
}

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 {start|lint|format|test|cleanup|commit} [environment]"
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
test)
    run_tests
    ;;
cleanup)
    cleanup
    ;;
commit)
    commit_commit
    ;;
*)
    echo "Invalid argument: $1"
    echo "Usage: $0 {start|lint|format|test|cleanup|commit} [environment]"
    exit 1
    ;;
esac
