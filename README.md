Claude config:
```
{
  "mcpServers": {
    "Quickchat bot name": {
      "command": "uv",
      "args": [
        "run",
        "quickchat_ai_mcp"
      ],
      "env": {
        "SCENARIO_ID": "<QUICKCHAT_SCENARIO_ID>",
      }
    }
  }
}
```

Cursor / Windsurf config:

```
{
  "mcpServers": {
    "Quickchat test bot": {
      "command": "uv",
      "args": [
        "run" , "quickchat_ai_mcp"
      ],
      "env": {
        "SCENARIO_ID": "<QUICKCHAT_SCENARIO_ID>"
      }
    }
  }
}
```