$python = Join-Path -Path $PSScriptRoot -ChildPath "venv\Scripts\python.exe"
$no_preference = Join-Path -Path $PSScriptRoot -ChildPath "no_preference.py"

& $python $no_preference
