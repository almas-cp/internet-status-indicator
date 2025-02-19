# Install required packages if not already installed
Write-Host "Installing required packages..."
pip install pyinstaller

# Clean previous builds
Write-Host "Cleaning previous builds..."
Remove-Item -Path "dist" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "installer" -Recurse -ErrorAction SilentlyContinue

# Create executable using PyInstaller
Write-Host "Creating executable..."
pyinstaller --noconfirm --onedir --windowed `
    --add-data "LICENSE;." `
    --add-data "README.md;." `
    --icon "network_status_indicator/icons/app.ico" `
    --name "internet-status-indicator" `
    "network_status_indicator/network_status_indicator.py"

# Create installer directory
Write-Host "Creating installer..."
New-Item -ItemType Directory -Path "installer" -ErrorAction SilentlyContinue

# Check if Inno Setup is installed
$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (Test-Path $innoSetupPath) {
    # Build installer
    Write-Host "Building installer..."
    & $innoSetupPath "installer_config.iss"
    Write-Host "Installer created successfully!"
} else {
    Write-Host "Inno Setup not found. Please install Inno Setup 6 from https://jrsoftware.org/isdl.php"
    Write-Host "After installing, run this script again."
} 