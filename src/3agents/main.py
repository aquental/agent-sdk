import anyio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AgentDefinition,
)
from utils import display_response


async def main():
    # 1. Define custom sub-agents individually
    
    # Analyzer Agent: Uses Sonnet for deep reasoning and Read/Grep tools to explore the codebase
    analyzer_agent = AgentDefinition(
        description="Code analysis specialist",
        prompt="You are a code analyzer. Review code for issues, patterns, and improvements.",
        tools=["Read", "Grep"],
        model="sonnet"
    )

    # Define the fixer_agent that fixes bugs
    # Hint: Its prompt should focus on identifying and fixing code issues
    fixer_agent = AgentDefinition(
        description="Bug fixing specialist",
        prompt="You are a bug fixer. Identify and fix code issues efficiently.",
        tools=["Read", "Write"],
        model="sonnet"
    )

    # Define the documenter_agent that writes documentation
    # Hint: Its prompt should focus on creating clear, comprehensive documentation
    documenter_agent = AgentDefinition(
        description="Documentation specialist",
        prompt="You are a documentation writer. Create clear, comprehensive documentation.",
        tools=["Read", "Write"],
        model="haiku"
    )

    # 2. Configure the main agent (The Orchestrator)
    options = ClaudeAgentOptions(
        model="haiku",
        max_turns=15,
        allowed_tools=["Read", "Write", "Bash", "Grep"],
        permission_mode="acceptEdits",
        # Add the fixer and documenter agents to the agents dictionary
        agents={
            "analyzer": analyzer_agent,
            "fixer": fixer_agent,
            "documenter": documenter_agent
        },
        # Update steps 2 and 3 to delegate to 'fixer' and 'documenter' agents
        system_prompt=(
            "You are a Lead Developer. Your goal is to improve code quality.\n"
            "When asked to improve a file, you MUST follow this strict process:\n"
            "1. Analyze the file for issues\n"
            "2. Delegate to 'fixer' to resolve them\n"
            "3. Delegate to 'documenter' to add docs\n"
            "Report back after each step."
        )
    )

    # 3. Run the agent
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Please improve the sample.py file.")

        await display_response(client)


if __name__ == "__main__":
    anyio.run(main)