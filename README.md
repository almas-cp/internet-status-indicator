# Internet Status Indicator (ISI)

A simple Windows system tray application that monitors your internet connection status in real-time.

## Features

- **Real-time monitoring**: Continuously checks your internet connection
- **Visual indicator**: Green icon when connected, red icon when disconnected
- **Minimal resource usage**: Lightweight application that runs in the system tray
- **Simple interface**: No complicated settings or configuration needed

## Installation

You can install Internet Status Indicator with a single command in PowerShell:

```powershell
irm almas-cp.github.io/isi | iex
```

This command will download and install the application automatically.

## How It Works

Internet Status Indicator works by:

1. Creating a system tray icon that displays your current internet status
2. Checking connectivity to Google's DNS server (8.8.8.8)
3. Updating the icon color based on connection status:
   - Green: Internet connection is available
   - Red: No internet connection detected

## Requirements

- Windows operating system
- Python 3.6 or higher
- Required Python packages:
  - pystray
  - Pillow (PIL)
  - requests

## Manual Installation

If you prefer to install manually:

1. Clone this repository
2. Install required packages: `pip install pystray pillow requests`
3. Run the script: `python script.py`

## Uninstallation

To uninstall, simply right-click the tray icon and select "Exit".

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.