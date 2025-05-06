#!/bin/bash
###############################################################################
# start.sh
#
# Purpose:   Professional startup script for initializing Azure OpenAI environment
#            and launching the Docker Compose environment for local development.
#
# Usage:     ./start.sh [OPTIONS]
#            -e, --env-file FILE  Path to .env file (default: ./.env)
#            -h, --help           Display help message and exit
#
# Prereqs:   - .env file with Azure OpenAI credentials
#            - Docker, Docker Compose, Poetry, Python, Node.js, Azure CLI installed
#
# Author:    [Your Name]
# Date:      2025-05-04
#
# Notes:     This script does not modify any application code. It only sets up
#            environment variables and launches the local dev environment.
###############################################################################

# This script sets up the environment variables for Azure OpenAI and runs the Docker Compose environment
# It sources values from the .env file but allows overriding them with command-line arguments

# Default path to .env file
ENV_FILE="./.env"

# Function to display usage information
function show_usage {
  echo "\n\033[1mUsage:\033[0m $0 [OPTIONS]"
  echo "\033[1mOptions:\033[0m"
  echo "  -e, --env-file FILE   Path to .env file (default: ./.env)"
  echo "  -h, --help            Display this help message and exit"
  echo
}

# Parse command-line options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    -h|--help)
      show_usage
      exit 0
      ;;
    *)
      echo "\n\033[31m[ERROR]\033[0m Unknown option: $1"
      show_usage
      exit 1
      ;;
  esac
done

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "\n\033[31m[ERROR]\033[0m Environment file '$ENV_FILE' not found."
  echo "Please create this file with your Azure OpenAI API credentials."
  exit 1
fi

# Load environment variables from .env file more safely
echo -e "\n\033[1m[INFO]\033[0m Loading environment variables from $ENV_FILE..."

# Use a temporary file for cleaned environment variables
TEMP_ENV_FILE=$(mktemp)
grep -v '^#' "$ENV_FILE" | grep -v '^$' | sed 's/=\s*/=/g' > "$TEMP_ENV_FILE"

# Read the file line by line to avoid issues with special characters
while IFS='=' read -r key value; do
  # Remove any trailing whitespace from key and value
  key=$(echo "$key" | xargs)

  # Skip if key contains invalid characters
  if [[ ! "$key" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
    echo -e "\033[33m[WARNING]\033[0m Skipping invalid environment variable: $key"
    continue
  fi

  # Export the variable
  export "$key=$value"
done < "$TEMP_ENV_FILE"

# Clean up
rm "$TEMP_ENV_FILE"

# Check if AZURE_OPENAI_ENDPOINT is set directly, if not, construct it from AZURE_OPENAI_RESOURCE
if [ -z "$AZURE_OPENAI_ENDPOINT" ] && [ -n "$AZURE_OPENAI_RESOURCE" ]; then
  export AZURE_OPENAI_ENDPOINT="https://${AZURE_OPENAI_RESOURCE}.openai.azure.com"
  echo -e "\033[1m[INFO]\033[0m Constructed Azure OpenAI endpoint from resource name: $AZURE_OPENAI_ENDPOINT"
fi

# Verify essential variables are set
if [ -z "$AZURE_OPENAI_ENDPOINT" ] || [ -z "$AZURE_OPENAI_API_KEY" ]; then
  echo -e "\n\033[31m[ERROR]\033[0m Azure OpenAI API credentials not found in $ENV_FILE."
  echo -e "Please ensure AZURE_OPENAI_ENDPOINT (or AZURE_OPENAI_RESOURCE) and AZURE_OPENAI_API_KEY are set."
  exit 1
fi

echo -e "\n\033[1m[INFO]\033[0m Using Azure OpenAI endpoint: $AZURE_OPENAI_ENDPOINT"
echo -e "\033[1m[INFO]\033[0m Using Azure OpenAI model: $AZURE_OPENAI_MODEL"

echo -e "\n\033[1m[STEP]\033[0m Installing Python dependencies via Poetry..."
poetry install

echo -e "\n\033[1m[STEP]\033[0m Starting Docker Compose environment..."
docker-compose -f docker-compose.local.yml down --remove-orphans
docker-compose -f docker-compose.local.yml up --build -d
#docker-compose -f docker-compose.local.yml build

# Note: The environment variables will be passed to Docker Compose
# and then to the containers via ${VAR_NAME} syntax in docker-compose.local.yml
