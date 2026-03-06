# Agent Monitor

macOS menubar app that monitors launchd-based automation agents in real-time.

## What it does

- Shows agent status in the menu bar: `✅ 5/5` (all running) or `⚠️ 3/5` (some down)
- Auto-refreshes every 30 seconds
- Per-agent controls: view logs, restart, stop, start
- Opens `tail -f` in Terminal for live log viewing
- Runs as a menu bar-only app (no Dock icon)

## Monitored Agents

| ID | Agent | launchd Label | Log Path |
|----|-------|---------------|----------|
| 002-1 | YouTube Pipeline | `com.youtube-pipeline.discord-bot` | `~/.youtube-pipeline/logs/discord_bot.log` |
| 002-2 | Agent Ref | `com.agent-ref-pipeline.discord-bot` | `~/.agent-ref-pipeline/logs/discord_bot.log` |
| 002-3 | Insta Notion | `com.insta-notion-pipeline.discord-bot` | `~/.insta-notion-pipeline/logs/discord_bot.log` |
| 002-4 | Discord News | `com.discord-news-notion.bot` | `~/.discord-news-notion-launcher/bot.log` |
| 002-5 | Call Transcript | `com.call-transcript-agent` | `~/.local/call-transcript-agent/logs/agent.log` |

## Quick Start

### Run directly

```bash
pip install rumps
python agent_monitor.py
```

### Build as .app

```bash
pip install rumps py2app
python setup.py py2app -A
open dist/Agent\ Monitor.app
```

### Auto-start on login

```bash
# Edit com.hh.agent-monitor.plist to match your .app path, then:
cp com.hh.agent-monitor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.hh.agent-monitor.plist
```

## Customization

Edit the `AGENTS` list in `agent_monitor.py` to add/remove agents. Each agent needs:

```python
{
    "id": "002-1",                          # Display ID
    "name": "YouTube Pipeline",             # Display name
    "label": "com.youtube-pipeline.discord-bot",  # launchd label
    "log": "~/.youtube-pipeline/logs/discord_bot.log",  # Log file path
}
```

## Tech

- Python 3 + [rumps](https://github.com/jaredks/rumps) (menu bar framework)
- [py2app](https://py2app.readthedocs.io/) for .app bundling
- macOS launchd for auto-start
