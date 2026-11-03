#!/usr/bin/env bash
set -euo pipefail

if ! command -v npm >/dev/null 2>&1; then
  echo "Node.js and npm are required. Install them and rerun this script." >&2
  exit 1
fi

echo "Installing the 21st.dev CLI and skills installer globally..."
npm install --global --ignore-scripts @21st-dev/cli skills

echo
echo "Starting 21st.dev sign-in. Complete the browser flow when it opens..."
21st login

echo
echo "Installing the 21st.dev agent skills into this project..."
skills add 21st-dev/skill

echo
echo "21st.dev CLI setup completed."
echo "Verify your account with: 21st whoami"
echo "Search components with: 21st search \"navigation bar\""
echo
echo "Do not commit API keys or local 21st credentials."
