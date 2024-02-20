import discord
import os
import logging
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
from ..bot.main import run
if not load_dotenv():
    raise FileNotFoundError("No .env")

def main():
    run(os.getenv("BOT_TOKEN"), discord.Intents.all())
    return 0

if __name__ == "__main__":
    exit(main())
