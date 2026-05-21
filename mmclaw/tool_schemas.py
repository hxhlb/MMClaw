from .tools import ShellTool


def _schema(name, description, properties=None, required=None):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "OBJECT",
                "properties": properties or {},
                "required": required or [],
            },
        },
    }


def get_native_tool_schemas(config):
    from .config import ConfigManager

    tools = [
        _schema(
            "shell_execute",
            f"Execute a shell command and return output. Times out after {ShellTool.TIMEOUT}s.",
            {"command": {"type": "STRING"}},
            ["command"],
        ),
        _schema(
            "shell_async",
            "Start a long-running shell command in the background.",
            {"command": {"type": "STRING"}},
            ["command"],
        ),
        _schema(
            "file_read",
            "Read a text file.",
            {"path": {"type": "STRING"}},
            ["path"],
        ),
        _schema(
            "file_write",
            "Write text content to a file.",
            {"path": {"type": "STRING"}, "content": {"type": "STRING"}},
            ["path", "content"],
        ),
        _schema(
            "file_upload",
            "Send a file to the user.",
            {"path": {"type": "STRING"}},
            ["path"],
        ),
        _schema(
            "wait",
            "Wait for a number of seconds.",
            {"seconds": {"type": "NUMBER"}},
            ["seconds"],
        ),
        _schema(
            "memory_add",
            "Save a short fact to global memory.",
            {"memory": {"type": "STRING"}},
            ["memory"],
        ),
        _schema("memory_list", "List global memories."),
        _schema(
            "memory_delete",
            "Delete one or more global memories by index.",
            {
                "indices": {
                    "type": "ARRAY",
                    "items": {"type": "INTEGER"},
                }
            },
            ["indices"],
        ),
    ]

    if ConfigManager.mode != "stateless":
        tools.extend([
            _schema("reset_session", "Clear the current session history."),
            _schema("upgrade", "Upgrade MMClaw via pip and restart the process."),
            _schema(
                "cron_create",
                "Create a cron job.",
                {
                    "name": {"type": "STRING"},
                    "cron": {"type": "STRING"},
                    "prompt": {"type": "STRING"},
                },
                ["name", "cron", "prompt"],
            ),
            _schema(
                "cron_delete",
                "Delete one or more cron jobs by index.",
                {
                    "indices": {
                        "type": "ARRAY",
                        "items": {"type": "INTEGER"},
                    }
                },
                ["indices"],
            ),
            _schema("cron_list", "List cron jobs."),
        ])

    if config.get("browser", {}).get("enabled", False):
        tools.extend([
            _schema("browser_start", "Start the browser."),
            _schema("browser_stop", "Stop the browser."),
            _schema(
                "browser_navigate",
                "Navigate the browser to a URL.",
                {"url": {"type": "STRING"}},
                ["url"],
            ),
            _schema(
                "browser_click",
                "Click an element by CSS selector.",
                {"selector": {"type": "STRING"}},
                ["selector"],
            ),
            _schema(
                "browser_fill",
                "Fill an input by CSS selector.",
                {"selector": {"type": "STRING"}, "text": {"type": "STRING"}},
                ["selector", "text"],
            ),
            _schema(
                "browser_get_text",
                "Get text from the page, optionally by CSS selector.",
                {"selector": {"type": "STRING"}},
            ),
            _schema(
                "browser_screenshot",
                "Take a screenshot only when explicitly requested.",
                {"path": {"type": "STRING"}},
            ),
        ])

    return tools
