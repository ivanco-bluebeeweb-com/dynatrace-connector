"""Extension declaration, capabilities, health check for Dynatrace Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "dynatrace-connector",
    version="0.1.0",
    display_name="Dynatrace",
    icon="icon.svg",
    capabilities=["dynatrace:manage"],
    description="Official Imperal connector for Dynatrace (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("dynatrace_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Dynatrace connection(s) configured." if count else "Not connected yet."
    }
