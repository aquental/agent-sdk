# Agent SDK study

## Claude
```shell
uv pip install claude-agent-sdk
```

Requires the Claude Code CLI (`npm install -g @anthropic-ai/claude-code`) and an
`ANTHROPIC_API_KEY` in the environment.

### Layout
- `src/agent_sdk/agent.py` — shared `ClaudeAgentOptions`, one-shot `run_once`, multi-turn `run_session`
- `src/agent_sdk/tools.py` — custom in-process MCP tools (`word_count`, `project_files`)
- `src/agent_sdk/cli.py` — argparse entrypoint exposed as the `agent-sdk` script

### Usage
```shell
# one-shot prompt
uv run agent-sdk "summarize the modules in src/"

# interactive session (context preserved between turns)
uv run agent-sdk

# options
uv run agent-sdk --model sonnet --max-turns 5 --permission-mode plan "review tools.py"
```

The default model comes from `AGENT_SDK_MODEL` (falls back to `sonnet`).

## Open AI
