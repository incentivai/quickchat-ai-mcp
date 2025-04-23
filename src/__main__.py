from mcp.server import FastMCP

from src.server import (
    API_KEY,
    SCENARIO_ID,
    app_lifespan,
    fetch_mcp_settings,
    send_message,
)

mcp_name, send_message_tool_description = fetch_mcp_settings(SCENARIO_ID, API_KEY)

mcp = FastMCP(mcp_name, lifespan=app_lifespan)

# Register tools by hand
mcp.add_tool(
    fn=send_message, name="Test name", description=send_message_tool_description
)


def run():
    print("Starting Quickchat mcp server")
    mcp.run()
