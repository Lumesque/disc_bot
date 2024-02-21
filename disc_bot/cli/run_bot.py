import discord
import os
import multiprocessing
import logging
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
from ..bot.main import run
if not load_dotenv():
    raise FileNotFoundError("No .env")

def get_process(token, intents):
    return multiprocessing.Process(name='bot_background_process',
                                   target=run,
                                   args=(token, intents))

def main():
    background_process = get_process(
            os.getenv("BOT_TOKEN"), discord.Intents.all()
            )
    background_process.start()
    #run(os.getenv("BOT_TOKEN"), discord.Intents.all())
    return 0

if __name__ == "__main__":
    exit(main())
