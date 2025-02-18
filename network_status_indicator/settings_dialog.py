from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QSpinBox, QLineEdit,
    QColorDialog, QComboBox, QFormLayout, QGroupBox,
    QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import copy

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = copy.deepcopy(settings) if settings else {}
        self.original_settings = copy.deepcopy(settings) if settings else {}
        
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.create_general_tab()
        self.create_appearance_tab()
        self.create_network_tab()
        
        layout.addWidget(self.tab_widget)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)

    def create_general_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        
        # Refresh rate
        self.refresh_rate = QSpinBox()
        self.refresh_rate.setRange(500, 10000)
        self.refresh_rate.setSingleStep(500)
        self.refresh_rate.setValue(self.settings.get('refresh_rate_ms', 1000))
        self.refresh_rate.setSuffix(" ms")
        layout.addRow("Check Interval:", self.refresh_rate)
        
        # Start with Windows option
        self.autostart = QComboBox()
        self.autostart.addItems(["Yes", "No"])
        self.autostart.setCurrentText("Yes" if self.settings.get('autostart', False) else "No")
        layout.addRow("Start with Windows:", self.autostart)
        
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "General")

    def create_appearance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Colors group
        colors_group = QGroupBox("Colors")
        colors_layout = QFormLayout()
        
        self.available_color = QPushButton()
        self.available_color.setFixedWidth(100)
        self.set_button_color(self.available_color, self.settings.get('color_available', '#4fde23'))
        self.available_color.clicked.connect(lambda: self.choose_color('available'))
        colors_layout.addRow("Available:", self.available_color)
        
        self.unavailable_color = QPushButton()
        self.unavailable_color.setFixedWidth(100)
        self.set_button_color(self.unavailable_color, self.settings.get('color_unavailable', '#f22424'))
        self.unavailable_color.clicked.connect(lambda: self.choose_color('unavailable'))
        colors_layout.addRow("Unavailable:", self.unavailable_color)
        
        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)
        
        # Shape and size group
        shape_group = QGroupBox("Shape and Size")
        shape_layout = QFormLayout()
        
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Circle", "Square", "Triangle"])
        self.shape_combo.setCurrentText(self.settings.get('shape', 'circle').capitalize())
        shape_layout.addRow("Shape:", self.shape_combo)
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(20, 60)
        self.size_spin.setValue(self.settings.get('circle_size', 40))
        shape_layout.addRow("Size:", self.size_spin)
        
        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)
        
        # Border group
        border_group = QGroupBox("Border")
        border_layout = QFormLayout()
        
        self.border_width = QSpinBox()
        self.border_width.setRange(0, 5)
        self.border_width.setValue(self.settings.get('border_width', 0))
        border_layout.addRow("Width:", self.border_width)
        
        self.border_color = QPushButton()
        self.border_color.setFixedWidth(100)
        self.set_button_color(self.border_color, self.settings.get('border_color', '#000000'))
        self.border_color.clicked.connect(lambda: self.choose_color('border'))
        border_layout.addRow("Color:", self.border_color)
        
        border_group.setLayout(border_layout)
        layout.addWidget(border_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Appearance")

    def create_network_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        
        # Target host
        self.target_host = QLineEdit()
        self.target_host.setText(self.settings.get('target_host', '8.8.8.8'))
        layout.addRow("Target Host:", self.target_host)
        
        # Timeout
        self.timeout = QSpinBox()
        self.timeout.setRange(1, 10)
        self.timeout.setValue(self.settings.get('timeout_seconds', 2))
        self.timeout.setSuffix(" seconds")
        layout.addRow("Timeout:", self.timeout)
        
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Network")

    def set_button_color(self, button, color):
        button.setStyleSheet(
            f"background-color: {color}; "
            "border: 1px solid #CCCCCC; "
            "border-radius: 3px;"
        )
        button.color = color

    def choose_color(self, button_type):
        current_color = getattr(self, f"{button_type}_color").color
        color = QColorDialog.getColor(QColor(current_color), self)
        
        if color.isValid():
            self.set_button_color(getattr(self, f"{button_type}_color"), color.name())

    def apply_settings(self):
        # Update settings dictionary
        self.settings.update({
            'refresh_rate_ms': self.refresh_rate.value(),
            'autostart': self.autostart.currentText() == "Yes",
            'color_available': self.available_color.color,
            'color_unavailable': self.unavailable_color.color,
            'shape': self.shape_combo.currentText().lower(),
            'circle_size': self.size_spin.value(),
            'border_width': self.border_width.value(),
            'border_color': self.border_color.color,
            'target_host': self.target_host.text(),
            'timeout_seconds': self.timeout.value()
        })
        
        # Emit signal or call callback to update main application
        if hasattr(self, 'settings_changed_callback'):
            self.settings_changed_callback(self.settings)

    def get_settings(self):
        return self.settings

    def accept(self):
        self.apply_settings()
        super().accept() 