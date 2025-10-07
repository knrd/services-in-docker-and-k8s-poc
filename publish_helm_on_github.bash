#!/bin/bash

set -ex

# Configuration
CHART_DIR="./helm/config-system"
PACKAGE_DIR="./helm-packages"
DOCS_DIR="./docs"
GITHUB_PAGES_URL="https://knrd.github.io/services-in-docker-and-k8s-poc"  # TODO: Replace with your GitHub Pages URL

# Create necessary directories
mkdir -p "$PACKAGE_DIR"
mkdir -p "$DOCS_DIR"

# Package the Helm chart
echo "📦 Packaging Helm chart..."
helm package "$CHART_DIR" -d "$PACKAGE_DIR"

# Move packaged chart to docs directory
mv "$PACKAGE_DIR"/*.tgz "$DOCS_DIR/"

# Generate or update the Helm repository index
echo "📑 Updating Helm repository index..."
if [ -f "$DOCS_DIR/index.yaml" ]; then
    helm repo index "$DOCS_DIR" --url "$GITHUB_PAGES_URL" --merge "$DOCS_DIR/index.yaml"
else
    helm repo index "$DOCS_DIR" --url "$GITHUB_PAGES_URL"
fi

# Cleanup
rm -rf "$PACKAGE_DIR"

# Git operations
# echo "🚀 Pushing changes to GitHub..."
# git add "$DOCS_DIR"
# git commit -m "Update Helm repository"
# git push origin master

# echo "✅ Helm chart published successfully!"
# echo "Repository is available at: $GITHUB_PAGES_URL"
