# Keep Awake

A macOS menubar app that prevents your Mac from sleeping by periodically moving the mouse.

## Features

- **Menubar toggle** — "Prevent Sleep" / "Allow Sleep" with one click
- **Status icons** — `laptop` (idle) / `mouse` (active)
- **Interval selector** — 3 sec, 5 sec, 10 sec, 30 sec, 1 min, 5 min, 10 min
- **macOS notifications** on start/stop and interval change
- **Failsafe** — move mouse to top-left corner to emergency stop (PyAutoGUI failsafe)
- **Menubar-only** — does not appear in Dock (LSUIElement)

## Requirements

- macOS
- Python 3.9+
- Dependencies: `rumps`, `pyautogui`

## Install Dependencies

```bash
pip install rumps pyautogui
```

## Run

```bash
python keep_awake_app.py
```

## Build as .app

Using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name "Keep Awake" --noconfirm keep_awake_app.py
```

The app will be at `dist/Keep Awake.app`.

To hide from Dock, add to `dist/Keep Awake.app/Contents/Info.plist`:

```xml
<key>LSUIElement</key>
<true/>
```

## How It Works

When activated, the app moves the mouse by a few pixels at the configured interval, then returns it to the original position. This prevents macOS from entering sleep mode while keeping the movement barely noticeable.
