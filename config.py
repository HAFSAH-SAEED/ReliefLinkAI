"""Central configuration for ReliefLink AI.

Keep user-facing labels, version metadata, page settings, and future environment
configuration in one place so later integrations can reuse them consistently.
"""

APP_TITLE = "ReliefLink AI"
APP_SUBTITLE = "AI-powered Disaster Relief Reporting Assistant"
APP_DESCRIPTION = (
    "ReliefLink AI is a prototype built during MLH Global Hack Week: Agents. "
    "It demonstrates how AI agents with persistent memory can help disaster "
    "victims report situations more effectively by remembering important context "
    "across conversations."
)

PROJECT_VERSION = "0.1"
PROJECT_STATUS = "Prototype"

PAGE_CONFIG = {
    "page_title": "ReliefLink AI",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

