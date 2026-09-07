import anyio
from claude_agent_sdk import query, AssistantMessage, TextBlock, ResultMessage


async def main():
    # query() returns an async generator that yields message objects
    async for message in query(prompt="Hi Claude! Please introduce yourself."):
        
        # Display assistant message responses
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        
        # elif branch here to handle ResultMessage and display metrics
        elif isinstance(message, ResultMessage):
            # - Print a separator line
            print("\n --- Result ---")
            # - Print the result text
            print(f"Result: {message.result}")
            # - Print the number of turns
            print(f"\nTurns        : {message.num_turns}")
            # - Print the cost formatted
            print(f"Cost         : ${message.total_cost_usd:.4f}")
            # - Print input token count
            print(f"Input tokens : {message.usage.get('input_tokens', 0)}")
            # - Print output token count
            print(f"Output tokens: {message.usage.get('output_tokens', 0)}")


if __name__ == "__main__":
    anyio.run(main)