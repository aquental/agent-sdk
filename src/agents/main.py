import anyio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AgentDefinition,
)
from agents.utils import display_response


async def main():
    # Analyzer Agent: Uses Sonnet for deep reasoning and Read/Grep tools to explore the codebase
    analyzer_agent = AgentDefinition(
        description="Code analysis specialist",
        prompt="You are a code analyzer. Review code for issues, patterns, and improvements.",
        tools=["Read", "Grep"],
        model="sonnet"
    )

    # Configure the main agent (The Orchestrator)
    options = ClaudeAgentOptions(
        model="haiku",
        max_turns=15,
        allowed_tools=["Read", "Write", "Bash", "Grep"],
        permission_mode="acceptEdits",
        agents={
            "analyzer": analyzer_agent
        },
        system_prompt=(
            "You are a Lead Developer. Your goal is to improve code quality.\n"
            "When asked to improve a file, you MUST follow this strict process:\n"
            "1. Delegate to 'analyzer' to find issues\n"
            "2. Fix the issues yourself using your tools\n"
            "3. Add documentation yourself using your tools\n"
            "Report back after each step."
        )
    )

    # Run the agent
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Please improve the sample.py file.")

        await display_response(client)


if __name__ == "__main__":
    anyio.run(main)