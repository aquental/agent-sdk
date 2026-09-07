import anyio


async def main():
    print("Starting task...")
    await anyio.sleep(2)
    print("Task complete!")


if __name__ == "__main__":
    anyio.run(main)