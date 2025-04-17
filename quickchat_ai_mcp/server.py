from mcp.server.fastmcp import FastMCP, Context
import requests
import json
from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import os
from dotenv import load_dotenv
load_dotenv()

api_key: str = os.getenv("API_KEY", "missing")
scenario_id: str = os.getenv("SCENARIO_ID", "missing")
conv_id: str | None = None

CHAT_ENDPOINT = "https://chat.quickchat.ai/chat"
SETTINGS_ENDPOINT = "https://app.quickchat.ai/mcp_settings"

def fetch_mcp_settings(scenario_id: str, api_key: str):
    response = requests.get(url=SETTINGS_ENDPOINT, headers={"scenario-id": scenario_id, "X-API-Key": api_key})

    data = json.loads(response.content)

    try:
        mcp_active, mcp_name, mcp_description = data["active"], data["name"], data["description"]
    except KeyError:
        raise ValueError("Configuration error")

    if not mcp_active:
        raise ValueError("Quickchat MCP not active.")

    if any(not len(x) > 0 for x in (mcp_name, mcp_description)):
        raise ValueError("MCP name and description cannot be empty.")

    return mcp_name, mcp_description

mcp_name, mcp_description = fetch_mcp_settings(scenario_id, api_key)

@dataclass
class AppContext:
    conv_id: str | None

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    yield AppContext(conv_id=conv_id)

mcp = FastMCP(mcp_name, lifespan=app_lifespan)

async def send_message(message: str, context: Context) -> str:

    mcp_client_name = context.request_context.session.client_params.clientInfo.name


    response = requests.post(url=CHAT_ENDPOINT, json={"api_key": api_key, "scenario_id": scenario_id, "conv_id": context.request_context.lifespan_context.conv_id, "text": message, "mcp_client_name": mcp_client_name})

    if response.status_code == 401:
        await context.request_context.session.send_log_message(level="error",
                                                               data=f"Unauthorized access. Double-check your scenario_id and api_key.")
        raise ValueError("Configuration error.")
    elif response.status_code != 200:
        await context.request_context.session.send_log_message(level="error",
                                                               data=f"Server error: {response.content}")
        raise ValueError("Server error. Please try again.")
    else:
        data = json.loads(response.content)

        if context.request_context.lifespan_context.conv_id is None:
            context.request_context.lifespan_context.conv_id = data["conv_id"]

        return data["reply"]

send_message.__doc__ = mcp_description
send_message = mcp.tool()(send_message)