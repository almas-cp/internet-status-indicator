# Internet Status Indicator 🌐

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/almas-cp/internet-status-indicator/graphs/commit-activity)

<img src="https://raw.githubusercontent.com/almas-cp/internet-status-indicator/main/docs/assets/demo.gif" alt="Demo" width="600"/>

*A sleek system tray application for real-time internet connectivity monitoring*

</div>

## ✨ Features

- 🔔 **Real-time Monitoring**: Instant updates on your internet connection status
- 🎯 **Visual Indicators**: 
  - 🟢 Green icon: Internet connection is active
  - 🔴 Red icon: No internet connection
- 🚀 **System Integration**: 
  - Seamless system tray integration
  - Lightweight and resource-efficient
  - Optional startup with Windows
- 💻 **User-Friendly**: Simple right-click menu for all controls
- ⚡ **Fast Performance**: Written in Python with optimized networking checks

## 🔧 Requirements

- Windows 10 or Windows 11
- For users: Just download and run!
- For developers:
  - Python 3.7 or higher
  - PyQt5 library

## 📦 Installation

### For Users 👥

1. Download the latest release:
   - [⬇️ Download Latest Version](https://github.com/almas-cp/internet-status-indicator/releases/latest)
2. Extract the ZIP file to your preferred location
3. Run `internet-status-indicator.exe`
4. Look for the icon in your system tray! 🎉

### For Developers 👨‍💻

```bash
# Clone the repository
git clone https://github.com/almas-cp/internet-status-indicator.git

# Navigate to the project directory
cd internet-status-indicator

# Install dependencies
pip install -r requirements.txt

# Run the application (Method 1)
python network_status_indicator/network_status_indicator.py

# Or install and run as a package (Method 2)
pip install -e .
python -c "from network_status_indicator import main; main()"
```

## 🎮 Usage

### Basic Usage
1. Launch the application
2. Look for the icon in your system tray:
   - 🟢 Green: You're connected!
   - 🔴 Red: Check your internet connection

### Advanced Features
Right-click the tray icon to access:
- ⚙️ Settings
  - Start with Windows
  - Check interval configuration
- ℹ️ About
- 🚪 Exit

## 🔍 How It Works

The application uses a sophisticated approach to monitor your internet connection:

1. **Connection Checking**: 
   - Primary check: DNS resolution test
   - Secondary check: HTTP request to reliable servers
   - Fallback: Socket connection test

2. **System Integration**:
   - Uses PyQt5 for the system tray interface
   - Efficient event-driven architecture
   - Minimal CPU and memory footprint

3. **Error Handling**:
   - Graceful recovery from network changes
   - Automatic reconnection attempts
   - Robust error logging

## 📁 Project Structure

```
internet-status-indicator/
├── network_status_indicator/
│   ├── __init__.py              # Package initialization
│   └── network_status_indicator.py  # Main application logic
├── requirements.txt             # Project dependencies
├── setup.py                     # Package configuration
├── LICENSE                      # MIT License
└── README.md                    # This documentation
```

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- 🔍 Expected behavior
- 🚫 Current behavior
- 📝 Steps to reproduce
- 💻 System information

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author

**almas-cp**
- GitHub: [@almas-cp](https://github.com/almas-cp)

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with Python and PyQt5
- Inspired by the need for simple network monitoring

---

<div align="center">

Made with ❤️ by almas-cp

⭐ Star this project if you find it useful!

</div>
