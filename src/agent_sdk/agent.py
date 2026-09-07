"""Agent configuration and run helpers built on the Claude Agent SDK."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    Message,
    ResultMessage,
    TextBlock,
    ThinkingBlock,
    query,
)

from .tools import build_tool_server

DEFAULT_SYSTEM_PROMPT = (
    "You are a focused engineering assistant. Prefer reading the repository "
    "before answering, keep responses short, and state assumptions explicitly."
)

DEFAULT_MODEL = os.environ.get("AGENT_SDK_MODEL", "sonnet")


def build_options(
    *,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    model: str = DEFAULT_MODEL,
    cwd: str | None = None,
    max_turns: int | None = None,
    permission_mode: str = "acceptEdits",
) -> ClaudeAgentOptions:
    """Return the options shared by every entrypoint in this project."""
    tool_server = build_tool_server()
    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model,
        cwd=cwd or os.getcwd(),
        max_turns=max_turns,
        permission_mode=permission_mode,
        mcp_servers={"project": tool_server},
        allowed_tools=[
            "Read",
            "Glob",
            "Grep",
            "mcp__project__word_count",
            "mcp__project__project_files",
        ],
    )


def render(message: Message) -> str | None:
    """Turn an SDK message into a line of terminal output, or None to skip it."""
    if isinstance(message, AssistantMessage):
        parts: list[str] = []
        for block in message.content:
            if isinstance(block, TextBlock):
                parts.append(block.text)
            elif isinstance(block, ThinkingBlock):
                continue
        text = "".join(parts).strip()
        return text or None
    if isinstance(message, ResultMessage):
        cost = message.total_cost_usd
        suffix = f" | cost ${cost:.4f}" if cost else ""
        return f"[done: {message.num_turns} turn(s){suffix}]"
    return None


async def run_once(
    prompt: str, options: ClaudeAgentOptions | None = None
) -> AsyncIterator[str]:
    """Run a single prompt to completion, yielding renderable output lines."""
    async for message in query(prompt=prompt, options=options or build_options()):
        line = render(message)
        if line:
            yield line


async def run_session(
    prompts: AsyncIterator[str], options: ClaudeAgentOptions | None = None
) -> AsyncIterator[str]:
    """Run a multi-turn session that keeps context between prompts."""
    async with ClaudeSDKClient(options=options or build_options()) as client:
        async for prompt in prompts:
            await client.query(prompt)
            async for message in client.receive_response():
                line = render(message)
                if line:
                    yield line
