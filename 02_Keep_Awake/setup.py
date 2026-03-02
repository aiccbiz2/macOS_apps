from setuptools import setup

APP = ["keep_awake_app.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "Keep Awake",
        "CFBundleDisplayName": "Keep Awake",
        "CFBundleIdentifier": "com.hh.keepawake",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0",
        "LSUIElement": True,  # 독(Dock)에 안 보이게 (메뉴바 전용)
        "NSAppleEventsUsageDescription": "Keep Awake needs accessibility access.",
    },
    "packages": ["rumps", "pyautogui"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
