#!/bin/bash

set -e

# Configuration
CHART_DIR="./helm/config-system"
OUTPUT_DIR="./k8s-manifests"
VALUES_FILE="$CHART_DIR/values.yaml"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Generating Kubernetes manifests from Helm chart..."

# Generate manifests using helm template
helm template config-system "$CHART_DIR" \
  --include-crds \
  --output-dir "$OUTPUT_DIR"

# Optionally, combine all files into a single manifest
echo "Combining manifests into a single file..."
find "$OUTPUT_DIR" -name '*.yaml' -exec cat {} \; > "$OUTPUT_DIR/all-in-one.yaml"

echo "Kubernetes manifests generated successfully!"
echo "Output location: $OUTPUT_DIR"
echo "Combined manifest: $OUTPUT_DIR/all-in-one.yaml"

# Optional: You can directly apply these manifests with:
echo "To apply these manifests, run:"
echo "kubectl apply -f $OUTPUT_DIR/all-in-one.yaml"
