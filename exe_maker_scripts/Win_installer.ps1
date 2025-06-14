$pythonScript = "Network-Tool.py"
$class_folder = "$PSScriptRoot\classes\"

$classFiles = @(
    "$class_folder\arp.py",
    "$class_folder\ipinfo.py",
    "$class_folder\myip.py",
    "$class_folder\networkint.py",
    "$class_folder\networkscan.py",
    "$class_folder\portscanner.py",
    "$class_folder\traceroute.py"
)

$hiddenImports = $classFiles -join " --hidden-import="

# Set location to script's folder
Set-Location -Path $PSScriptRoot

# Ensure PyInstaller is installed
if (-Not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    pip install pyinstaller
}

Write-Host "Building executable..."
pyinstaller --onefile --hidden-import=$hiddenImports $pythonScript

Write-Host "Executable created successfully!"