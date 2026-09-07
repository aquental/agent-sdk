import anyio
from claude_agent_sdk import query, ResultMessage


# Define an async main function
async def main():
    async for message in query(prompt="Search the web and bring me the latest version of the Claude Agent SDK."):
        # Check if this message is an assistant response
        if isinstance(message, ResultMessage):
            print(f"\n--- Result ---")
            # The final result text (same as last AssistantMessage)
            print(f"Result: {message.result}")
            # Number of reasoning cycles the agent went through
            print(f"Turns: {message.num_turns}")
            # Total cost in USD for this interaction
            print(f"Cost: ${message.total_cost_usd:.4f}")
            # Token usage details
            print(f"Input tokens: {message.usage.get('input_tokens', 0)}")
            print(f"Output tokens: {message.usage.get('output_tokens', 0)}")

if __name__ == "__main__":
    anyio.run(main)