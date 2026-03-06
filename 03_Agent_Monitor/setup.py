from setuptools import setup

APP = ['agent_monitor.py']
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,  # 메뉴바 전용 (Dock 아이콘 숨김)
        'CFBundleName': 'Agent Monitor',
        'CFBundleDisplayName': 'Agent Monitor',
        'CFBundleIdentifier': 'com.hh.agent-monitor',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name='Agent Monitor',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
