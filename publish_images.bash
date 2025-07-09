#!/bin/bash

set -e

# Check if a version was provided as an argument
if [ -z "$1" ]; then
  echo "❌ Usage: $0 <version>"
  exit 1
fi

VERSION="$1"
USERNAME="knrd"

# List of service directories to build and push
SERVICES=("config_sender" "web_service")

# Loop through each service
for SERVICE in "${SERVICES[@]}"; do
  IMAGE_NAME="$USERNAME/$SERVICE"

  echo "📦 Building image: $IMAGE_NAME:$VERSION from ./$SERVICE"

  # Build the Docker image using the Dockerfile in the service directory
  docker build -t "$IMAGE_NAME:$VERSION" "$SERVICE"
  
  # Push the image to Docker Hub
  echo "🚀 Pushing image: $IMAGE_NAME:$VERSION"
  docker push "$IMAGE_NAME:$VERSION"
done

echo "✅ All images built and pushed successfully!"
