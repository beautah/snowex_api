#!/bin/bash

echo "Activating Virtual Environment..."
readonly sourceFile="./.venv/bin/activate"

source ${sourceFile}

echo "Virtual Environment Activated!"

readonly projDir=$(pwd)

cd ${projDir}

echo "Deploying awdb_api on port 8041..."

waitress-serve --port=8041 --url-scheme=http api:app