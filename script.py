import socket
import threading
import time
from datetime import datetime

import pystray
from pystray import MenuItem
from PIL import Image, ImageDraw


def make_icon(color: str) -> Image.Image:
    """Create a 64x64 RGBA image with a filled colored circle."""
    colors = {
        "green": (34, 197, 94),
        "red": (239, 68, 68),
    }
    rgb = colors[color]

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 62, 62], fill=rgb)
    return img


def is_connected() -> bool:
    """Check internet connectivity via TCP socket to DNS resolvers."""
    targets = [("8.8.8.8", 53), ("1.1.1.1", 53)]

    for host, port in targets:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            sock.connect((host, port))
            return True
        except OSError:
            continue
        finally:
            if sock:
                sock.close()

    return False


def monitor(icon: pystray.Icon, stop_event: threading.Event) -> None:
    """Background thread that monitors connectivity and updates the tray icon."""
    last_state = None

    while not stop_event.is_set():
        current_state = is_connected()

        if current_state != last_state:
            if current_state:
                icon.icon = make_icon("green")
                icon.title = "Internet: Connected"
            else:
                icon.icon = make_icon("red")
                icon.title = "Internet: Disconnected"

            status = "Connected" if current_state else "Disconnected"
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Internet: {status}")

            last_state = current_state

        stop_event.wait(3)


if __name__ == "__main__":
    stop_event = threading.Event()

    def on_exit(icon, item):
        stop_event.set()
        icon.stop()

    menu = pystray.Menu(MenuItem("Exit", on_exit))

    icon = pystray.Icon(
        name="ISI",
        icon=make_icon("red"),
        title="Internet: Disconnected",
        menu=menu,
    )

    def setup(icon):
        icon.visible = True
        thread = threading.Thread(target=monitor, args=(icon, stop_event), daemon=True)
        thread.start()

    icon.run(setup=setup)
