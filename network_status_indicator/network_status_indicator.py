import sys
import subprocess
import platform
import logging
import json
import os
from typing import Optional
from contextlib import contextmanager
from PyQt5.QtWidgets import (
    QSystemTrayIcon, QApplication, QMenu, QColorDialog, 
    QInputDialog, QMessageBox, QWidget
)
from PyQt5.QtGui import QPainter, QPixmap, QIcon, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NetworkStatusIndicator(QSystemTrayIcon):
    """A system tray icon that displays network availability status."""

    status_changed = pyqtSignal(bool)  # Signal for status changes

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setToolTip("Network Status Indicator")
        logging.info("Initializing NetworkStatusIndicator...")
        
        # Default settings
        self.default_settings = {
            "refresh_rate_ms": 1000,
            "target_host": "8.8.8.8",
            "timeout_seconds": 2,
            "circle_size": 40,
            "circle_offset": 12,
            "shape": "circle",
            "border_width": 0,
            "border_color": "#000000",
            "color_available": "#4fde23",
            "color_unavailable": "#f22424"
        }
        
        # Load or create settings
        self.settings_file = os.path.join(os.path.expanduser("~"), ".network_indicator_settings.json")
        self.load_settings()
        
        # Start monitoring
        self.check_connectivity()
        
        # Add context menu
        self.create_context_menu()
        
        self.last_status = None

    def load_settings(self) -> None:
        """Load settings from file or create with defaults."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    # Merge with defaults to handle new settings in updates
                    self.settings = self.default_settings.copy()
                    self.settings.update(saved_settings)
                    # Load colors from settings
                    self.color_available = self.settings['color_available']
                    self.color_unavailable = self.settings['color_unavailable']
                logging.info('Settings loaded from file')
            else:
                self.settings = self.default_settings.copy()
                self.color_available = self.settings['color_available']
                self.color_unavailable = self.settings['color_unavailable']
                self.save_settings()
                logging.info('Created new settings file with defaults')
        except Exception as e:
            logging.error(f'Error loading settings: {e}')
            self.settings = self.default_settings.copy()
            self.color_available = self.settings['color_available']
            self.color_unavailable = self.settings['color_unavailable']

    def save_settings(self) -> None:
        """Save current settings to file."""
        try:
            # Update colors in settings
            self.settings['color_available'] = self.color_available
            self.settings['color_unavailable'] = self.color_unavailable
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logging.info('Settings saved to file')
        except Exception as e:
            logging.error(f'Error saving settings: {e}')

    @contextmanager
    def create_painter(self, pixmap: QPixmap) -> QPainter:
        painter = QPainter(pixmap)
        try:
            yield painter
        finally:
            painter.end()

    def create_status_icon(self, is_available: bool) -> QIcon:
        """Create an icon with the specified color and shape."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)

        with self.create_painter(pixmap) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Set main color
            color = self.color_available if is_available else self.color_unavailable
            painter.setBrush(QBrush(QColor(color)))
            
            # Set border
            if self.settings['border_width'] > 0:
                painter.setPen(QPen(
                    QColor(self.settings['border_color']), 
                    self.settings['border_width']
                ))
            else:
                painter.setPen(Qt.NoPen)
            
            # Draw shape
            size = self.settings['circle_size']
            offset = self.settings['circle_offset']
            
            if self.settings['shape'] == 'circle':
                painter.drawEllipse(offset, offset, size, size)
            elif self.settings['shape'] == 'square':
                painter.drawRect(offset, offset, size, size)
            elif self.settings['shape'] == 'triangle':
                points = [
                    QPoint(offset + size//2, offset),
                    QPoint(offset, offset + size),
                    QPoint(offset + size, offset + size)
                ]
                painter.drawPolygon(points)

        return QIcon(pixmap)

    def check_connectivity(self) -> None:
        """Check network connectivity and update the system tray icon."""
        logging.info('Checking connectivity...')
        try:
            is_available = self.ping(self.settings['target_host'])
            
            if self.last_status != is_available:
                self.status_changed.emit(is_available)
            
            icon = self.create_status_icon(is_available)
            
            self.setIcon(icon)
            status_text = 'Network Available' if is_available else 'Network Unavailable'
            self.setToolTip(status_text)
            
            self.last_status = is_available

        except Exception as e:
            logging.error(f'Error checking connectivity: {e}')
            self.setIcon(self.create_status_icon(False))
            self.setToolTip('Network Unavailable')

        # Schedule next check
        QTimer.singleShot(self.settings['refresh_rate_ms'], self.check_connectivity)

    def ping(self, host: str) -> bool:
        """Execute ping command and return if host is reachable."""
        try:
            command = ['ping', '-n' if platform.system() == "Windows" else '-c', '1', host]
            process = subprocess.run(
                command, 
                capture_output=True, 
                timeout=self.settings['timeout_seconds'],
                text=True
            )
            
            if process.returncode == 0:
                return True
                
            logging.warning(f'Ping failed with return code {process.returncode}')
            return False

        except subprocess.TimeoutExpired:
            logging.error(f'Ping timed out after {self.settings["timeout_seconds"]} seconds')
            return False
        except subprocess.SubprocessError as e:
            logging.error(f'Subprocess error during ping: {e}')
            return False
        except Exception as e:
            logging.error(f'Unexpected error during ping: {e}')
            return False

    def create_context_menu(self) -> None:
        """Create and set up the right-click context menu."""
        menu = QMenu()
        
        # Check now option
        check_now = menu.addAction("Check Now")
        check_now.triggered.connect(self.check_connectivity)
        
        menu.addSeparator()
        
        # Settings submenu
        settings_menu = menu.addMenu("Settings")
        
        # Time settings
        time_action = settings_menu.addAction("Set Check Interval")
        time_action.triggered.connect(self.set_check_interval)
        
        timeout_action = settings_menu.addAction("Set Ping Timeout")
        timeout_action.triggered.connect(self.set_ping_timeout)
        
        # Appearance submenu
        appearance_menu = settings_menu.addMenu("Appearance")
        
        # Colors
        available_color = appearance_menu.addAction("Set Available Color")
        available_color.triggered.connect(self.set_available_color)
        
        unavailable_color = appearance_menu.addAction("Set Unavailable Color")
        unavailable_color.triggered.connect(self.set_unavailable_color)
        
        # Shape
        shape_menu = appearance_menu.addMenu("Shape")
        shapes = ['circle', 'square', 'triangle']
        for shape in shapes:
            action = shape_menu.addAction(shape.capitalize())
            action.triggered.connect(lambda checked, s=shape: self.set_shape(s))
        
        # Size
        size_action = appearance_menu.addAction("Set Size")
        size_action.triggered.connect(self.set_size)
        
        # Border
        border_menu = appearance_menu.addMenu("Border")
        border_width = border_menu.addAction("Set Width")
        border_width.triggered.connect(self.set_border_width)
        border_color = border_menu.addAction("Set Color")
        border_color.triggered.connect(self.set_border_color)
        
        # Target host
        host_action = settings_menu.addAction("Set Target Host")
        host_action.triggered.connect(self.set_target_host)
        
        menu.addSeparator()
        
        # Quit option
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.instance().quit)
        
        self.setContextMenu(menu)

    def set_check_interval(self) -> None:
        """Set the time between connectivity checks."""
        current = self.settings['refresh_rate_ms'] // 1000
        interval, ok = QInputDialog.getInt(
            None, "Set Check Interval",
            "Enter time between checks (seconds):",
            current, 1, 3600
        )
        if ok:
            self.settings['refresh_rate_ms'] = interval * 1000
            self.save_settings()

    def set_ping_timeout(self) -> None:
        """Set the ping timeout duration."""
        current = self.settings['timeout_seconds']
        timeout, ok = QInputDialog.getInt(
            None, "Set Ping Timeout",
            "Enter ping timeout (seconds):",
            current, 1, 10
        )
        if ok:
            self.settings['timeout_seconds'] = timeout
            self.save_settings()

    def set_available_color(self) -> None:
        """Set the color for available status."""
        color = QColorDialog.getColor(QColor(self.color_available))
        if color.isValid():
            self.color_available = color.name()
            self.check_connectivity()
            self.save_settings()

    def set_unavailable_color(self) -> None:
        """Set the color for unavailable status."""
        color = QColorDialog.getColor(QColor(self.color_unavailable))
        if color.isValid():
            self.color_unavailable = color.name()
            self.check_connectivity()
            self.save_settings()

    def set_shape(self, shape: str) -> None:
        """Set the icon shape."""
        self.settings['shape'] = shape
        self.check_connectivity()
        self.save_settings()

    def set_size(self) -> None:
        """Set the icon size."""
        current = self.settings['circle_size']
        size, ok = QInputDialog.getInt(
            None, "Set Size",
            "Enter icon size (pixels):",
            current, 20, 60
        )
        if ok:
            self.settings['circle_size'] = size
            self.settings['circle_offset'] = (64 - size) // 2
            self.check_connectivity()
            self.save_settings()

    def set_border_width(self) -> None:
        """Set the border width."""
        current = self.settings['border_width']
        width, ok = QInputDialog.getInt(
            None, "Set Border Width",
            "Enter border width (pixels):",
            current, 0, 5
        )
        if ok:
            self.settings['border_width'] = width
            self.check_connectivity()
            self.save_settings()

    def set_border_color(self) -> None:
        """Set the border color."""
        color = QColorDialog.getColor(QColor(self.settings['border_color']))
        if color.isValid():
            self.settings['border_color'] = color.name()
            self.check_connectivity()
            self.save_settings()

    def set_target_host(self) -> None:
        """Set the target host to ping."""
        current = self.settings['target_host']
        host, ok = QInputDialog.getText(
            None, "Set Target Host",
            "Enter host to ping (e.g., 8.8.8.8):",
            text=current
        )
        if ok and host:
            self.settings['target_host'] = host
            self.save_settings()

def main() -> None:
    """Application entry point."""
    logging.info('Starting application...')
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    indicator = NetworkStatusIndicator()
    indicator.show()
    
    logging.info('Starting application event loop...')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
