#!/bin/bash

# Set up environment
python_script="Network-Tool.py"
class_folder="./classes/"
class_files=("arp.py" "ipinfo.py" "myip.py" "networkint.py" "networkscan.py" "portscanner.py" "traceroute.py")
hidden_imports=$(printf " --hidden-import=%s" "${class_files[@]}")

# Ensure PyInstaller is installed
pip install pyinstaller

# Set location to script's directory
cd "$(dirname "$0")"

# Run PyInstaller
pyinstaller --onefile $hidden_imports "$python_script"

# Move the executable to a desired location
mv "dist/${python_script%.py}" "./output"

echo "Executable created successfully!"