"""Keep Awake - macOS menubar app to prevent sleep.

Periodically moves the mouse slightly to keep the system awake.
"""

import rumps
import pyautogui
import random
import threading
import time

pyautogui.FAILSAFE = True

INTERVALS = [
    ("3 sec", 3),
    ("5 sec", 5),
    ("10 sec", 10),
    ("30 sec", 30),
    ("1 min", 60),
    ("5 min", 300),
    ("10 min", 600),
]
DEFAULT_INTERVAL = 30


class KeepAwakeApp(rumps.App):
    def __init__(self):
        super().__init__(
            "Keep Awake",
            icon=None,
            title="💻",
        )
        self.is_active = False
        self.interval = DEFAULT_INTERVAL
        self.worker_thread = None

        # Interval submenu
        self.interval_menu = rumps.MenuItem("Interval")
        for label, seconds in INTERVALS:
            item = rumps.MenuItem(label, callback=self._set_interval)
            item._seconds = seconds
            if seconds == DEFAULT_INTERVAL:
                item.state = True
            self.interval_menu.add(item)

        self.menu = [
            rumps.MenuItem("Prevent Sleep", callback=self.toggle),
            None,
            self.interval_menu,
        ]

    def toggle(self, sender):
        if self.is_active:
            self._stop()
            sender.title = "Prevent Sleep"
        else:
            self._start()
            sender.title = "Allow Sleep"

    def _set_interval(self, sender):
        self.interval = sender._seconds
        for item in self.interval_menu.values():
            if hasattr(item, "_seconds"):
                item.state = (item._seconds == self.interval)
        rumps.notification(
            title="Keep Awake",
            subtitle="Interval Changed",
            message=f"Interval: {sender.title}",
        )

    def _start(self):
        self.is_active = True
        self.title = "🖱️"
        rumps.notification(
            title="Keep Awake",
            subtitle="Started",
            message=f"Moving mouse every {self._interval_label()}.",
        )
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _stop(self):
        self.is_active = False
        self.title = "💻"
        rumps.notification(
            title="Keep Awake",
            subtitle="Stopped",
            message="Mac can sleep again.",
        )

    def _interval_label(self) -> str:
        for label, seconds in INTERVALS:
            if seconds == self.interval:
                return label
        return f"{self.interval}s"

    def _worker(self):
        while self.is_active:
            try:
                x, y = pyautogui.position()
                offset = random.choice([-3, -2, -1, 1, 2, 3])
                pyautogui.moveTo(x + offset, y + offset, duration=0.2)
                pyautogui.moveTo(x, y, duration=0.2)
            except Exception:
                pass
            time.sleep(self.interval)


if __name__ == "__main__":
    KeepAwakeApp().run()
