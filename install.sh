#!/usr/bin/env bash

# Move to script directory
cd $(dirname "$0")

# Create virtual environment using Python 3
python3 -m venv ./venv

# Install requirements from venv
./venv/Scripts/pip install -r requirements.txt
