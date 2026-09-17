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

## Agent Examples (`src/agents/`, `src/1agents/`, `src/3agents/`)

Three directories explore the Claude Agent SDK's agent orchestration capabilities:

### `src/agents/` — Single sub-agent

A lead orchestrator (haiku) delegates **code analysis** to a specialized `analyzer` sub-agent (sonnet), then applies fixes and documentation itself. Basic delegation pattern.

```shell
uv run agents
```

### `src/1agents/` — Three sub-agents

Same orchestrator but delegates to **three** specialized sub-agents: `analyzer`, `fixer` (sonnet), and `documenter` (haiku). Each owns one stage of the improvement pipeline.

```shell
uv run agent1
```

### `src/3agents/` — MCP server + sub-agent

Demonstrates MCP tool sharing with sub-agents. An orchestrator delegates documentation lookups to a `researcher` sub-agent (haiku) that uses the **Context7 MCP server** (`mcp__context7__resolve-library-id` / `mcp__context7__get-library-docs`) to search library docs. MCP servers are registered via `mcp_servers` in `ClaudeAgentOptions`.

```shell
uv run agent3
```
