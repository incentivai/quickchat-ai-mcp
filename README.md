<p align="center">
  <img src="img/background.jpg"/>
</p>

# Quickchat AI MCP server

The Quickchat AI MCP (Model Context Protocol) server allows you to let anyone plug in your Quickchat AI Agent into their favourite AI app such as Claude Desktop, Cursor, VS Code or Windsurf.

## Quickstart
1. Create a Quickchat AI account and start a 7-day trial of any plan.
2. Set up your AI's Knowledge Base, capabilities and settings.
3. Go to the MCP page to activate your MCP, give it Name, Description and (optional) Command. They are important, AI apps need to understand when to contact your AI, what its capabilities and knowledge are.
4. That's it! Now you're ready to test your Quickchat AI via any AI app and show it to the world!

<p align="center">
  <img src="img/claude_tool_anatomy.png" alt="Claude tool anatomy" width="600"/>
  <br/>
  <sub>Claude tool anatomy</sub>
</p>

## Test with Claude Desktop

### Prerequisite
Install `uv` using `curl -LsSf https://astral.sh/uv/install.sh | sh` or read more [here](https://docs.astral.sh/uv/getting-started/installation/).

### Configuration
Go to Settings > Developer > Edit Config. Open to edit the claude_desktop_config.json file in a text editor. If you're just starting out, the file is going to look like this:

```JSON
{
  "mcpServers": {}
}
```

This is where you can define all the MCPs your Claude Desktop has access to. Here is how you add your Quickchat AI MCP:

```JSON
{
  "mcpServers": {
    "< QUICKCHAT AI MCP NAME >": {
      "command": "uvx",
      "args": ["quickchat-ai-mcp"],
      "env": {
        "SCENARIO_ID": "< QUICKCHAT AI SCENARIO ID >",
        "API_KEY": "< QUICKCHAT AI API KEY >"
      }
    }
  }
}
```

Go to the Quickchat AI app > MCP > Integration to find the above snippet with the values of MCP Name, Scenario Id and API Key filled out.

## Test with Cursor

### Prerequisite
Install the Quickchat AI MCP Python package: `pip install quickchat-ai-mcp`

### Configuration
Go to Settings > Cursor Settings > MCP > Add new global MCP server and include the following:

```JSON
{
  "mcpServers": {
    "< QUICKCHAT AI MCP NAME >": {
      "command": "<YOUR PYTHON PATH>",
      "args": [
        "-m",
        "quickchat-ai-mcp"
      ],
      "env": {
        "SCENARIO_ID": "< QUICKCHAT AI SCENARIO ID >",
        "API_KEY": "< QUICKCHAT AI API KEY >"
      }
    }
  }
}
```

As before, you can find values for MCP Name, Scenario Id and API Key at Quickchat AI app > MCP > Integration.

### How to find YOUR PYTHON PATH?
Open the Python console (type python into your command line) and run:
```Python
import sys
print(sys.executable)
```

## Test with other AI apps

Other AI apps will most likely require the same configuration as the one show above ☝️but the actual steps to include it in the App itself will be different. We will be expanding this README as we go along.

## Launch your Quickchat AI MCP to the world! 

```
⛔️ Do not publish your Quickchat API key to your users!
```

Once you're ready to let other users connect your Quickchat AI MCP to their AI apps, share the configuration steps. However, you need to make sure they can use your Quickchat AI MCP without your Quickchat API key. Here is how to do that:
1. On the Quickchat App MCP page, turn the Require API key toggle OFF.
2. Share the configuration snippet without the API key. Below is the Claude Desktop example:

```JSON
{
  "mcpServers": {
    "< QUICKCHAT AI MCP NAME >": {
      "command": "uvx",
      "args": ["quickchat-ai-mcp"],
      "env": {
        "SCENARIO_ID": "< QUICKCHAT AI SCENARIO ID >"
      }
    }
  }
}
```
---

### Cool features
- You can control all aspects of your MCP from the Quickchat dashboard. One click and your change is deployed. That includes the MCP name and description - all your users need to do is refresh their MCP connection.
- View all conversations in the Quickchat Inbox. Remember: those won't be the exact messages your users send to their AI app but rather the transcript of the AI <> AI interaction between their AI app and your Quickchat AI. 🤯
- Unlike most MCP implementation, this isn't a static tool handed to an AI. It's an open-ended way to send messages to Quickchat AI Agents you create. 