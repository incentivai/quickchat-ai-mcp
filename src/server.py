from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
import json
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
import requests

load_dotenv()


BASE_URL: str = os.getenv("BASE_URL", "https://app.quickchat.ai")
CONV_ID: str | None = None


CHAT_ENDPOINT = f"{BASE_URL}/v1/api/mcp/chat"
SETTINGS_ENDPOINT = f"{BASE_URL}/v1/api/mcp/settings"


def fetch_mcp_settings(scenario_id: str, api_key: str):
    response = requests.get(
        url=SETTINGS_ENDPOINT,
        headers={"scenario-id": scenario_id, "X-API-Key": api_key},
    )

    if response.status_code != 200:
        raise ValueError(
            "Configuration error. Please check your API key and scenario ID."
        )

    data = json.loads(response.content)

    try:
        mcp_active, mcp_name, mcp_description = (
            data["active"],
            data["name"],
            data["description"],
        )
    except KeyError:
        raise ValueError("Configuration error")

    if not mcp_active:
        raise ValueError("Quickchat MCP not active.")

    if any(not len(x) > 0 for x in (mcp_name, mcp_description)):
        raise ValueError("MCP name and description cannot be empty.")

    return mcp_name, mcp_description


@dataclass
class AppContext:
    conv_id: str | None


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    yield AppContext(conv_id=CONV_ID)


async def send_message(
    message: str, context: Context, scenario_id: str, api_key: str
) -> str:
    mcp_client_name = context.request_context.session.client_params.clientInfo.name

    response = requests.post(
        url=CHAT_ENDPOINT,
        headers={"scenario-id": scenario_id, "X-API-Key": api_key},
        json={
            "conv_id": context.request_context.lifespan_context.conv_id,
            "text": message,
            "mcp_client_name": mcp_client_name,
        },
    )

    if response.status_code == 401:
        await context.request_context.session.send_log_message(
            level="error",
            data="Unauthorized access. Double-check your scenario_id and api_key.",
        )
        raise ValueError("Configuration error.")
    elif response.status_code != 200:
        await context.request_context.session.send_log_message(
            level="error", data=f"Server error: {response.content}"
        )
        raise ValueError("Server error. Please try again.")
    else:
        data = json.loads(response.content)

        if context.request_context.lifespan_context.conv_id is None:
            context.request_context.lifespan_context.conv_id = data["conv_id"]

        return data["reply"]
