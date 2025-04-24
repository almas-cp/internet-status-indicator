


          
# 🌐 Internet Status Indicator (ISI)

<div align="center">
  
  ![ISI Logo](https://img.shields.io/badge/ISI-Internet%20Status%20Indicator-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white)
  
  <h3>Simple. Reliable. Essential.</h3>
  
  [![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
  [![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
  
</div>

---

## 🔍 Overview

**Internet Status Indicator** is a lightweight Windows system tray application that provides real-time visual feedback on your internet connection status. Never wonder if you're connected again!

<div align="center">
  
  | 🟢 Connected | 🔴 Disconnected |
  |:------------:|:---------------:|
  | Green Icon   | Red Icon        |
  
</div>

## ✨ Features

- **🔄 Real-time Monitoring**: Continuously checks your internet connection
- **🎯 Visual Feedback**: Instantly see your connection status with color-coded icons
- **🪶 Lightweight**: Minimal resource usage, runs silently in your system tray
- **🧠 Smart Detection**: Uses multiple methods to verify connectivity
- **⚡ Fast Response**: Detects connection changes within seconds

## 🚀 One-Click Installation

Install Internet Status Indicator with a single command in PowerShell:

```powershell
irm almas-cp.github.io/isi | iex
```

<div align="center">
  <i>Check your system tray more icons( ^ ), That's it! No complicated setup required.</i>
</div>

## 🔧 How It Works

Internet Status Indicator uses a sophisticated yet simple approach:

1. **Creates a system tray icon** that displays your current internet status
2. **Checks connectivity** to Google's DNS server (8.8.8.8)
3. **Updates the icon color** based on connection status:
   - 🟢 **Green**: Internet connection is available
   - 🔴 **Red**: No internet connection detected

## 📋 Requirements

- **Windows** operating system
- **Python 3.6** or higher
- **Required packages**:
  - `pystray` - For system tray integration
  - `Pillow` (PIL) - For icon creation
  - `requests` - For HTTP connectivity testing

## 📥 Manual Installation

If you prefer to install manually:

<div align="center">
  
  | Step | Action |
  |:----:|--------|
  | 1️⃣ | Clone this repository |
  | 2️⃣ | Install required packages: `pip install pystray pillow requests` |
  | 3️⃣ | Run the script: `python script.py` |
  
</div>

## 🗑️ Uninstallation

To uninstall, simply right-click the tray icon and select "Exit".

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Submit issues
- Propose new features
- Create pull requests

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p><b>Stay connected. Stay informed.</b></p>
  <p>Made with ❤️ by <a href="https://github.com/almas-cp">almas-cp</a></p>
</div>
