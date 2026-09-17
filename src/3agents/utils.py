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
                                print(f"{key}: {value}")