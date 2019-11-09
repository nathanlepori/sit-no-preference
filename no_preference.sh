#!/usr/bin/env bash

# Get script dir
script_dir=$(dirname "$0")
# Get venv python interpreter
python="${script_dir}/venv/bin/python"
# Get entrypoint script
no_preference="${script_dir}/no_preference.py"

# Execute using the venv Python interpreter
eval "$python $no_preference"
