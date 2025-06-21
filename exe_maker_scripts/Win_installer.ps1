$pythonScript = "main.py"
$class_folder = "$PSScriptRoot\classes"

$classFiles = @(
    "arp.py",
    "ipinfo.py",
    "myip.py",
    "networkint.py",
    "networkscan.py",
    "portscanner.py",
    "traceroute.py"
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