import asyncio
import logging
import sys

from src.main import startup_bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(startup_bot())
