#!/usr/bin/env bash
# Deploy the D-Kevin guestbook to a server.
# Run this ON the target server (from the app directory), as root.
#
# Prerequisites: python3, python3-venv, MySQL running locally.
# Configuration is read from /opt/d-kevin/.env (see .env.example).
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/d-kevin}"

cd "$APP_DIR"

# 1. Python virtualenv + dependencies
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# 2. Database schema (uses root creds from .env via mysql defaults file caller)
#    Expected to be created separately; see README.

# 3. systemd service
cp deploy/d-kevin.service /etc/systemd/system/d-kevin.service
systemctl daemon-reload
systemctl enable d-kevin
systemctl restart d-kevin

echo "Deployed. Service status:"
systemctl --no-pager status d-kevin | head -20
