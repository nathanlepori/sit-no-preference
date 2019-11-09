#!/usr/bin/env bash

script_dir=$(dirname "$0")
python="${script_dir}/venv/Scripts/python"
no_preference="${script_dir}/no_preference.py"

eval "$python $no_preference"
