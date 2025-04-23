from functools import partial
import os

from mcp.server import FastMCP

from src.server import (
    app_lifespan,
    fetch_mcp_settings,
    send_message,
)

SCENARIO_ID: str = os.getenv("SCENARIO_ID")

if SCENARIO_ID is None:
    raise ValueError(
        "SCENARIO_ID environment variable is not set. Please set it in the .env file or in environment variables."
    )

API_KEY: str = os.getenv("API_KEY")

if API_KEY is None:
    # In case API key is not given substitute scenario to allow public usage.
    API_KEY = SCENARIO_ID


mcp_name, send_message_tool_description = fetch_mcp_settings(SCENARIO_ID, API_KEY)

mcp = FastMCP(mcp_name, lifespan=app_lifespan)


send_message = partial(send_message, scenario_id=SCENARIO_ID, api_key=API_KEY)
send_message.__name__ = "send_message"

# Register tools by hand
mcp.add_tool(
    fn=send_message, name="send_message", description=send_message_tool_description
)


def run():
    print("Starting Quickchat mcp server")
    mcp.run()
