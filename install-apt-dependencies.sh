#!/bin/bash
# exit immediately if a command exits with a non-zero status
set -e

echo "Updating apt-get..."
sudo apt-get update -y

echo "Installing graphviz..."
sudo apt-get install -y graphviz

echo "Dependencies installed."
