import os
from contextlib import suppress

import discord
from discord.ext import commands
from dotenv import load_dotenv

from ...cli.run_bot import get_process
from ...exceptions.handling import print_traceback

if not load_dotenv():
    raise FileNotFoundError("No .env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
DISC_CHANNEL = int(os.getenv("CHANNEL_ID"))


def get_channel(bot_obj):
    return bot_obj.get_channel(DISC_CHANNEL)


process = get_process(BOT_TOKEN, discord.Intents.all())
process.start()
bot = commands.Bot(command_prefix="!", guild_subscriptions=True, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(dir(process))
    with print_traceback("Bot did not translate"):
        assert await assert_bot_translates(bot, get_channel(bot)), "Bot did not translate"
        print("Bot translated correctly!")
    # fuck dat shit up
    process.kill()
    await bot.close()


def check(m):
    return m.content == "My love"


async def assert_bot_translates(bot, channel):
    await channel.send("Mi amor")
    with suppress(TimeoutError):
        await bot.wait_for("message", check=check, timeout=3)
        return True
    return False


bot.run(TEST_TOKEN)
