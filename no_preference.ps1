# Get venv python interpreter
$python = Join-Path -Path $PSScriptRoot -ChildPath "venv\Scripts\python.exe"
# Get entrypoint script
$no_preference = Join-Path -Path $PSScriptRoot -ChildPath "no_preference.py"

# Execute using the venv Python interpreter
& $python $no_preference
