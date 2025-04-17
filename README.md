


Claude config:
```
{
  "mcpServers": {
    "Quickchat bot name": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "requests",
        "mcp",
        "run",
        "<PATH_TO_QUICKCHAT_AI_MCP_REPO>/quickchat_ai_mcp/server.py"
      ],
      "env": {
        "SCENARIO_ID": <QUICKCHAT_SCENARIO_ID>,
        "API_KEY": <QUICKCHAT_API_KEY>
      }
    }
  }
}
```

Cursor / Windsurf config:

```
{
  "mcpServers": {
    "Quickchat bot name": {
      "command": "/usr/local/bin/python",  # import sys, print(sys.executable)
      "args": [
        "<PATH_TO_QUICKCHAT_AI_MCP_REPO>/quickchat_ai_mcp/server.py"
      ],
      "env": {
        "SCENARIO_ID": <QUICKCHAT_SCENARIO_ID>,
        "API_KEY": <QUICKCHAT_API_KEY>
      }
    }
  }
}
```