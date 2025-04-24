import pystray
import threading
import time
import requests
from PIL import Image, ImageDraw
import socket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('InternetStatusIndicator')

# Default settings - now hardcoded since settings menu is removed
CHECK_INTERVAL = 1  # seconds
HOST_IP = "8.8.8.8"  # Google DNS

# Function to create icon images
def create_icon(color):
    # Create a blank image with transparent background
    image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    # Draw a filled circle with the specified color
    dc.ellipse((8, 8, 56, 56), fill=color)
    
    return image

# Icons for different states
GREEN_ICON = create_icon((0, 255, 0, 255))  # Connected
RED_ICON = create_icon((255, 0, 0, 255))    # Disconnected

# Flag to control the update thread
running = True

# Function to check internet connectivity
def check_internet():
    logger.info(f"Checking internet connection to {HOST_IP}...")
    
    # Try method 1: Socket connection
    try:
        logger.info(f"Attempting socket connection to {HOST_IP}:53 with timeout of 3 seconds")
        start_time = time.time()
        socket.create_connection((HOST_IP, 53), timeout=3)
        elapsed = time.time() - start_time
        logger.info(f"Socket connection successful! Response time: {elapsed:.3f} seconds")
        return True
    except OSError as e:
        logger.warning(f"Socket connection failed: {str(e)}")
        
        # Try method 2: HTTP request
        try:
            logger.info("Attempting fallback HTTP request to https://www.google.com")
            start_time = time.time()
            response = requests.get("https://www.google.com", timeout=3)
            elapsed = time.time() - start_time
            logger.info(f"HTTP request successful! Status code: {response.status_code}, Response time: {elapsed:.3f} seconds")
            return True
        except Exception as e:
            logger.error(f"HTTP request failed: {str(e)}")
            return False

# Function to update the icon based on internet status
def update_icon_status(icon):
    logger.info("Starting automatic connection monitoring")
    
    # Wait a moment for the icon to be fully initialized
    time.sleep(1)
    
    while running:
        # Check internet connection
        logger.info(f"Running scheduled check (interval: {CHECK_INTERVAL}s)")
        connection_status = check_internet()
        
        if connection_status:
            logger.info("Internet connection is AVAILABLE - Setting GREEN icon")
            icon.icon = GREEN_ICON
            icon.title = "Internet: Connected"
        else:
            logger.warning("Internet connection is UNAVAILABLE - Setting RED icon")
            icon.icon = RED_ICON
            icon.title = "Internet: Disconnected"
            
        # Wait before checking again
        logger.info(f"Waiting {CHECK_INTERVAL} seconds until next check")
        time.sleep(CHECK_INTERVAL)
    
    logger.info("Update thread terminated")

# Function to exit the application
def exit_action(icon):
    logger.info("Exit requested by user")
    global running
    running = False
    icon.stop()

# Create the system tray icon
def create_tray_icon():
    logger.info("=== Internet Status Indicator Starting ===")
    logger.info(f"Using check_interval={CHECK_INTERVAL}s, host_ip={HOST_IP}")
    
    # Create the icon
    icon = pystray.Icon("InternetStatusIndicator")
    icon.title = "Internet Status Indicator"
    icon.icon = RED_ICON  # Start with red until first check
    logger.info("System tray icon created")
    
    # Create a minimal menu with just exit option
    icon.menu = pystray.Menu(
        pystray.MenuItem("Exit", exit_action)
    )
    logger.info("Menu created with only Exit option")
    
    # Start the update thread
    update_thread = threading.Thread(target=update_icon_status, args=(icon,))
    update_thread.daemon = True
    update_thread.start()
    logger.info("Background monitoring thread started")
    
    # Run the icon
    logger.info("Starting system tray icon - application is now running")
    try:
        icon.run()
        logger.info("Application terminated normally")
    except Exception as e:
        logger.error(f"Error running system tray icon: {str(e)}")
    
    # Make sure to signal the thread to stop
    global running
    running = False

if __name__ == "__main__":
    create_tray_icon()