"""Custom in-process tools exposed to the agent via an SDK MCP server."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from claude_agent_sdk import McpSdkServerConfig, create_sdk_mcp_server, tool


@tool(
    "word_count",
    "Count words, lines, and characters in a block of text.",
    {"text": str},
)
async def word_count(args: dict[str, Any]) -> dict[str, Any]:
    text: str = args["text"]
    summary = (
        f"lines={len(text.splitlines())} "
        f"words={len(text.split())} "
        f"chars={len(text)}"
    )
    return {"content": [{"type": "text", "text": summary}]}


@tool(
    "project_files",
    "List files tracked in the project source tree, filtered by glob pattern.",
    {"pattern": str},
)
async def project_files(args: dict[str, Any]) -> dict[str, Any]:
    pattern: str = args.get("pattern") or "**/*.py"
    root = Path.cwd()
    matches = sorted(
        str(path.relative_to(root))
        for path in root.glob(pattern)
        if path.is_file() and ".venv" not in path.parts and ".git" not in path.parts
    )
    listing = "\n".join(matches[:200]) or "no matches"
    return {"content": [{"type": "text", "text": listing}]}


def build_tool_server() -> McpSdkServerConfig:
    """Bundle the project tools into a server the agent can call."""
    return create_sdk_mcp_server(
        name="project",
        version="0.1.0",
        tools=[word_count, project_files],
    )
