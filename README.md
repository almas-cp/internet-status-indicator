# Internet Status Indicator 🌐

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/almas-cp/internet-status-indicator/graphs/commit-activity)

<img src="https://raw.githubusercontent.com/almas-cp/internet-status-indicator/main/docs/assets/demo.gif" alt="Demo" width="600"/>

*A powerful, lightweight system tray application for real-time internet connectivity monitoring with speed measurements*

[Installation](#-installation) • [Features](#-features) • [Configuration](#-configuration) • [FAQ](#-faq) • [Contributing](#-contributing)

</div>

## 🚀 Key Features

- 🔄 **Real-time Network Monitoring**
  - Instant connection status updates
  - Download and upload speed measurements
  - Configurable check intervals

- 🎨 **Customizable Visual Indicators**
  - Multiple shape options (circle, square, triangle)
  - Customizable colors for connected/disconnected states
  - Adjustable size and border options

- ⚡ **Performance Optimized**
  - Asynchronous network checks
  - Minimal CPU and memory usage
  - Fast startup and response time

- 🔧 **Advanced Configuration**
  - Custom target host for connectivity checks
  - Adjustable timeout settings
  - Configurable refresh rates

- 💻 **System Integration**
  - Windows startup integration
  - System tray quick actions
  - Persistent settings storage

## 🛠️ Requirements

### For Users
- Windows 10 or Windows 11
- No additional software required

### For Developers
- Python 3.7 or higher
- Dependencies:
  - PyQt5 ≥ 5.15.0 (UI framework)
  - aiohttp ≥ 3.8.0 (async network operations)
  - asyncio ≥ 3.4.3 (async support)

## 📦 Installation

### Quick Start (Users)
1. Download the latest release from our [releases page](https://github.com/almas-cp/internet-status-indicator/releases/latest)
2. Extract the ZIP file
3. Run `internet-status-indicator.exe`
4. Look for the indicator in your system tray

### Developer Installation
```bash
# Clone the repository
git clone https://github.com/almas-cp/internet-status-indicator.git
cd internet-status-indicator

# Method 1: Direct run
pip install -r requirements.txt
python network_status_indicator/network_status_indicator.py

# Method 2: Install as package
pip install -e .
python -c "from network_status_indicator import main; main()"
```

## ⚙️ Configuration

### Visual Settings
- **Indicator Shape**: Choose between circle, square, or triangle
- **Colors**: Customize for both connected and disconnected states
- **Size & Border**: Adjust indicator size and border properties

### Network Settings
- **Target Host**: Default is 8.8.8.8 (Google DNS)
- **Check Interval**: Configurable from 500ms to 10000ms
- **Timeout**: Adjustable from 1 to 10 seconds

### System Settings
- **Auto-start**: Option to launch with Windows
- **Tray Menu**: Quick access to all settings

## 🔍 How It Works

### Network Monitoring
1. **Connectivity Check**
   - HTTP request to configured target host
   - Fallback to alternative methods if primary fails

2. **Speed Measurement**
   - Download speed test using Cloudflare's speed test endpoints
   - Upload speed measurement with optimized data packets
   - Real-time speed updates in tooltip

3. **Status Updates**
   - Asynchronous network operations
   - Event-driven UI updates
   - Efficient error handling and recovery

## ❓ FAQ

### General Questions

**Q: How accurate are the speed measurements?**
A: Speed measurements use Cloudflare's speed test infrastructure, providing reliable results comparable to dedicated speed test services.

**Q: Will this slow down my internet?**
A: No, the application uses minimal bandwidth for checks and optimizes network requests to avoid impact on your connection.

**Q: Can I change the check frequency?**
A: Yes, you can adjust the check interval from 500ms to 10 seconds in the settings.

### Troubleshooting

**Q: The indicator shows I'm offline when I'm not**
A: Try:
1. Checking your target host setting
2. Increasing the timeout value
3. Verifying firewall settings

**Q: The application won't start with Windows**
A: Ensure you have administrator privileges when enabling auto-start.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Code Contributions**
   - Fork the repository
   - Create a feature branch
   - Submit a pull request

2. **Bug Reports**
   - Use the issue tracker
   - Include detailed reproduction steps
   - Provide system information

3. **Feature Requests**
   - Open an issue with the "enhancement" label
   - Describe the feature and its benefits

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

## 👨‍💻 Author

**almas-cp**
- GitHub: [@almas-cp](https://github.com/almas-cp)

## 🌟 Acknowledgments

- Built with Python and PyQt5
- Speed testing powered by Cloudflare
- Icons and UI inspired by modern design principles

---

<div align="center">

Made with ❤️ by almas-cp

⭐ Star this project if you find it useful!

</div>
