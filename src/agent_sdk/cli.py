"""Command line entrypoint for the agent."""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections.abc import AsyncIterator

from claude_agent_sdk import CLINotFoundError, ClaudeSDKError

from .agent import DEFAULT_MODEL, build_options, run_once, run_session


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="agent-sdk",
        description="Run a Claude Agent SDK agent over the current project.",
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Prompt to send. Omit to start an interactive session.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model alias or id.")
    parser.add_argument(
        "--max-turns",
        type=int,
        default=None,
        help="Stop the agent after this many turns.",
    )
    parser.add_argument(
        "--permission-mode",
        default="acceptEdits",
        choices=["default", "acceptEdits", "bypassPermissions", "plan"],
        help="How tool permissions are handled.",
    )
    parser.add_argument("--cwd", default=None, help="Working directory for the agent.")
    return parser.parse_args(argv)


async def _stdin_prompts() -> AsyncIterator[str]:
    loop = asyncio.get_running_loop()
    while True:
        try:
            line = await loop.run_in_executor(None, lambda: input("you> "))
        except (EOFError, KeyboardInterrupt):
            print()
            return
        line = line.strip()
        if not line:
            continue
        if line in {"exit", "quit"}:
            return
        yield line


async def _main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    options = build_options(
        model=args.model,
        cwd=args.cwd,
        max_turns=args.max_turns,
        permission_mode=args.permission_mode,
    )

    try:
        if args.prompt:
            async for line in run_once(" ".join(args.prompt), options):
                print(line)
        else:
            print("Interactive session. Type 'exit' to quit.")
            async for line in run_session(_stdin_prompts(), options):
                print(f"agent> {line}")
    except CLINotFoundError:
        print(
            "Claude Code CLI not found. Install it with "
            "`npm install -g @anthropic-ai/claude-code`.",
            file=sys.stderr,
        )
        return 127
    except ClaudeSDKError as exc:
        print(f"agent error: {exc}", file=sys.stderr)
        return 1
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(_main()))


if __name__ == "__main__":
    main()
