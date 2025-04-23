#!/bin/bash

echo "===== [setupEnv.sh] Setting up local development environment ====="

# changing ownership of the workspace directory to the current user
# this is probably not necessary and not secure (required because repo cloned from WSL root)
# TODO: real developer fix this please
sudo chown -R vscode:vscode /workspace

# Ensure Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "[ERROR] Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Output for confirmation
echo "===== [setupEnv.sh] Setting up local development Environment Components Done ====="

pip install --upgrade pip

pip install poetry

# https://pypi.org/project/poetry-plugin-export/
pip install poetry-plugin-export

poetry env use python3.11

poetry config warnings.export false

poetry install --with dev

poetry run pre-commit install

(cd ./code/frontend; npm install)

(cd ./tests/integration/ui; npm install)
