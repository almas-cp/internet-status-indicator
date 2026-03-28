"""
Internet Status Indicator — System tray app showing real-time internet connectivity.

Green circle  = connected
Red circle    = disconnected

Uses a socket probe to Google DNS (8.8.8.8:53) with an HTTP fallback.
"""

import pystray
import threading
import time
import socket
import logging
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Logging — only log state *changes*, not every poll
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ISI")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CHECK_INTERVAL = 3        # seconds between checks (3s is responsive yet light)
DNS_HOST = "8.8.8.8"     # Google public DNS
DNS_PORT = 53
SOCKET_TIMEOUT = 3        # seconds
HTTP_TIMEOUT = 3          # seconds
HTTP_URL = "https://www.google.com"

# ---------------------------------------------------------------------------
# Icon helpers
# ---------------------------------------------------------------------------

def _make_circle(color: tuple[int, int, int, int]) -> Image.Image:
    """Return a 64×64 RGBA image with a filled circle of *color*."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ImageDraw.Draw(img).ellipse((8, 8, 56, 56), fill=color)
    return img


GREEN_ICON = _make_circle((0, 200, 80, 255))   # connected
RED_ICON   = _make_circle((220, 40, 40, 255))   # disconnected

# ---------------------------------------------------------------------------
# Connectivity check
# ---------------------------------------------------------------------------

def _check_socket() -> bool:
    """Try a TCP connection to the DNS host on port 53."""
    try:
        conn = socket.create_connection((DNS_HOST, DNS_PORT), timeout=SOCKET_TIMEOUT)
        conn.close()
        return True
    except OSError:
        return False


def _check_http() -> bool:
    """Fallback: try an HTTP GET to a well-known URL."""
    try:
        import requests  # lazy import — only needed on fallback
        resp = requests.get(HTTP_URL, timeout=HTTP_TIMEOUT)
        return resp.status_code < 400
    except Exception:
        return False


def is_online() -> bool:
    """Return *True* if the machine can reach the internet."""
    return _check_socket() or _check_http()

# ---------------------------------------------------------------------------
# Monitor thread
# ---------------------------------------------------------------------------

def _monitor(icon: pystray.Icon, stop_event: threading.Event) -> None:
    """Poll connectivity and update the tray icon on state changes."""
    # Give the tray icon a moment to initialize
    time.sleep(0.5)

    previous: bool | None = None  # unknown on first run

    while not stop_event.is_set():
        online = is_online()

        # Only touch the icon / log when the state actually changes
        if online != previous:
            if online:
                icon.icon = GREEN_ICON
                icon.title = "Internet: Connected"
                logger.info("Internet connection: ONLINE ✓")
            else:
                icon.icon = RED_ICON
                icon.title = "Internet: Disconnected"
                logger.warning("Internet connection: OFFLINE ✗")
            previous = online

        # Use the event's wait() so we can be interrupted immediately on exit
        stop_event.wait(CHECK_INTERVAL)

    logger.info("Monitor thread stopped.")

# ---------------------------------------------------------------------------
# Application entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("=== Internet Status Indicator starting ===")

    stop_event = threading.Event()

    # --- build the tray icon ---
    icon = pystray.Icon("InternetStatusIndicator")
    icon.icon = RED_ICON                         # assume offline until first check
    icon.title = "Internet Status Indicator"

    def on_exit(_icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        logger.info("Exit requested.")
        stop_event.set()          # signal the monitor thread to quit
        _icon.stop()              # tear down the tray icon

    icon.menu = pystray.Menu(
        pystray.MenuItem("Exit", on_exit),
    )

    # --- start the background monitor ---
    monitor = threading.Thread(target=_monitor, args=(icon, stop_event), daemon=True)
    monitor.start()

    # --- run the tray icon (blocks until icon.stop()) ---
    try:
        icon.run()
    except Exception as exc:
        logger.error("Tray icon error: %s", exc)
    finally:
        stop_event.set()
        monitor.join(timeout=5)

    logger.info("=== Internet Status Indicator stopped ===")


if __name__ == "__main__":
    main()