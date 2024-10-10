import logging
import logging.config
import multiprocessing
import os
import sys

import discord
from dotenv import load_dotenv

from ..bot.main import run

if not load_dotenv():
    raise FileNotFoundError("No .env")


def get_process(token, intents):
    return multiprocessing.Process(name="bot_background_process", target=run, args=(token, intents))


def main():
    background_process = get_process(os.getenv("BOT_TOKEN"), discord.Intents.all())
    background_process.start()
    return 0


if __name__ == "__main__":
    logging.config.fileConfig("disc_bot/config/output_level_2.cfg")
    sys.exit(main())
