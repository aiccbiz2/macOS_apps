#!/usr/bin/env python3
"""
Agent Monitor — macOS Menu Bar App
002 시리즈 에이전트 5개를 메뉴바에서 모니터링
"""

import subprocess
import os
import rumps

AGENTS = [
    {
        "id": "002-1",
        "name": "YouTube Pipeline",
        "label": "com.youtube-pipeline.discord-bot",
        "log": os.path.expanduser("~/.youtube-pipeline/logs/discord_bot.log"),
    },
    {
        "id": "002-2",
        "name": "Agent Ref",
        "label": "com.agent-ref-pipeline.discord-bot",
        "log": os.path.expanduser("~/.agent-ref-pipeline/logs/discord_bot.log"),
    },
    {
        "id": "002-3",
        "name": "Insta Notion",
        "label": "com.insta-notion-pipeline.discord-bot",
        "log": os.path.expanduser("~/.insta-notion-pipeline/logs/discord_bot.log"),
    },
    {
        "id": "002-4",
        "name": "Discord News",
        "label": "com.discord-news-notion.bot",
        "log": os.path.expanduser("~/.discord-news-notion-launcher/bot.log"),
    },
    {
        "id": "002-5",
        "name": "Call Transcript",
        "label": "com.call-transcript-agent",
        "log": os.path.expanduser("~/.local/call-transcript-agent/logs/agent.log"),
    },
]

LOG_LINES = 30


def get_agent_status(label):
    """launchctl list에서 에이전트 상태 확인. (pid, exit_code) 반환."""
    try:
        result = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return None, None
        pid = None
        exit_code = None
        for line in result.stdout.splitlines():
            if '"PID"' in line:
                pid = line.split("=")[-1].strip().rstrip(";")
            elif '"LastExitStatus"' in line:
                exit_code = line.split("=")[-1].strip().rstrip(";")
        return pid, exit_code
    except Exception:
        return None, None


def get_log_tail(log_path, lines=LOG_LINES):
    """로그 파일 마지막 N줄 읽기."""
    if not os.path.exists(log_path):
        return f"(로그 파일 없음: {log_path})"
    try:
        result = subprocess.run(
            ["tail", f"-{lines}", log_path],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout or "(빈 로그)"
    except Exception as e:
        return f"(로그 읽기 실패: {e})"


class AgentMonitorApp(rumps.App):
    def __init__(self):
        super().__init__("", quit_button=None)
        self.menu_items = {}
        self._build_menu()
        self._update_status(None)

    def _build_menu(self):
        for agent in AGENTS:
            # 에이전트 상태 항목
            status_item = rumps.MenuItem(
                f"{agent['id']} {agent['name']}: ...",
                callback=None
            )
            status_item.set_callback(None)

            # 하위 메뉴: 로그 보기, 재시작, 중지
            log_item = rumps.MenuItem(
                "로그 보기 (Terminal)",
                callback=self._make_log_callback(agent)
            )
            restart_item = rumps.MenuItem(
                "재시작",
                callback=self._make_restart_callback(agent)
            )
            stop_item = rumps.MenuItem(
                "중지",
                callback=self._make_stop_callback(agent)
            )
            start_item = rumps.MenuItem(
                "시작",
                callback=self._make_start_callback(agent)
            )

            status_item.add(log_item)
            status_item.add(restart_item)
            status_item.add(stop_item)
            status_item.add(start_item)

            self.menu.add(status_item)
            self.menu_items[agent["label"]] = status_item

        self.menu.add(rumps.separator)

        refresh_item = rumps.MenuItem("새로고침", callback=self._update_status)
        self.menu.add(refresh_item)

        self.menu.add(rumps.separator)
        quit_item = rumps.MenuItem("종료", callback=self._quit)
        self.menu.add(quit_item)

    def _make_log_callback(self, agent):
        def callback(_):
            log_path = agent["log"]
            # Terminal.app에서 tail -f 실행
            script = f'''
            tell application "Terminal"
                activate
                do script "echo '=== {agent['id']} {agent['name']} 로그 ===' && tail -f '{log_path}'"
            end tell
            '''
            subprocess.Popen(["osascript", "-e", script])
        return callback

    def _make_restart_callback(self, agent):
        def callback(_):
            label = agent["label"]
            subprocess.run(["launchctl", "stop", label], timeout=5)
            subprocess.run(["launchctl", "start", label], timeout=5)
            rumps.notification(
                "Agent Monitor",
                f"{agent['id']} {agent['name']}",
                "재시작 완료",
                sound=False
            )
            self._update_status(None)
        return callback

    def _make_stop_callback(self, agent):
        def callback(_):
            label = agent["label"]
            subprocess.run(["launchctl", "stop", label], timeout=5)
            rumps.notification(
                "Agent Monitor",
                f"{agent['id']} {agent['name']}",
                "중지됨",
                sound=False
            )
            self._update_status(None)
        return callback

    def _make_start_callback(self, agent):
        def callback(_):
            label = agent["label"]
            subprocess.run(["launchctl", "start", label], timeout=5)
            rumps.notification(
                "Agent Monitor",
                f"{agent['id']} {agent['name']}",
                "시작됨",
                sound=False
            )
            self._update_status(None)
        return callback

    def _quit(self, _):
        rumps.quit_application()

    @rumps.timer(30)
    def _update_status(self, _):
        """30초마다 상태 갱신."""
        all_up = True
        for agent in AGENTS:
            pid, exit_code = get_agent_status(agent["label"])
            item = self.menu_items[agent["label"]]

            if pid and pid != "0":
                icon = "●"
                status_text = f"PID {pid}"
            else:
                icon = "○"
                status_text = "STOPPED"
                all_up = False

            item.title = f"{icon} {agent['id']} {agent['name']}  —  {status_text}"

        # 메뉴바 아이콘: 전부 살아있으면 초록, 아니면 빨강
        self.title = f"{'✅' if all_up else '⚠️'} {sum(1 for a in AGENTS if get_agent_status(a['label'])[0] not in (None, '0'))}/5"


if __name__ == "__main__":
    AgentMonitorApp().run()
