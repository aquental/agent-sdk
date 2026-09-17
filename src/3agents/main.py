import anyio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AgentDefinition
)
from claude_agent_sdk import (
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    UserMessage,
    ToolResultBlock
)

async def display_response(client: ClaudeSDKClient):
    """Helper function to display agent messages with formatting"""
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\n💬 Claude Response:")
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"\n🔧 [Tool: {block.name}]")
                    # Display input if tool is Task
                    if block.name == "Task":
                        if block.input:
                            for key, value in block.input.items():
                                print(f"\t🔧 - {key}: {value}")

async def main():
    # Define external MCP server configuration
    context7_config = {
        "type": "stdio",  # Communicates via stdin/stdout
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"]
    }

    # Create a researcher_agent using AgentDefinition
    # - Give it a description identifying it as a documentation research specialist
    # - Write a prompt explaining its role is to search library documentation
    # - Provide it with the MCP tools: "mcp__context7__resolve-library-id" and "mcp__context7__get-library-docs"
    researcher_agent = AgentDefinition(
        description=(
            "Documentation research specialist. Use for any library/SDK "
            "documentation lookup or API usage question."
        ),
        prompt=(
            "You search library docs. Call mcp__context7__resolve-library-id "
            "then mcp__context7__get-library-docs. Return cited excerpts. "
            "Do not invent APIs."
        ),
        tools=[
            "mcp__context7__resolve-library-id",
            "mcp__context7__get-library-docs",
        ],
        model="haiku",
    )

    # Configure the orchestrator below:
    # - Register the researcher_agent in an 'agents' parameter with key "researcher"
    # - Add a 'system_prompt' that instructs the orchestrator to delegate documentation research to the researcher
    # - Keep the MCP tools in 'allowed_tools' - this is required for sub-agents to use them
    options = ClaudeAgentOptions(
        model="haiku",
        max_turns=10,
        mcp_servers={"context7": context7_config},
        allowed_tools=[
            "Task",
            "Agent",
            "Read",
            "Grep",
            "mcp__context7__resolve-library-id",
            "mcp__context7__get-library-docs",
        ],
        agents={"researcher": researcher_agent},
        system_prompt=(
            "You are an orchestrator. You do not look up library docs yourself.\n"
            "For ANY documentation question you MUST spawn the 'researcher' "
            "subagent (Task/Agent tool, subagent_type='researcher').\n"
            "After it returns, summarize. Report after each step."
        ),
    )
    
    # Run the agent
    async with ClaudeSDKClient(options=options) as client:
        await client.query(
            "Search for documentation on how the "
            "Claude Agent SDK (Python) uses MCP servers."
        )
        
        await display_response(client)


if __name__ == "__main__":
    anyio.run(main)