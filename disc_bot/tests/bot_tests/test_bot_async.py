import os
from ...cli.run_bot import main
from ...bot.main import run
import pytest
import discord
import asyncio
from discord.ext import commands

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
GUILD = os.getenv("GUILD_ID")
CHANNEL = os.getenv("CHANNEL_ID")

main()
test_bot = commands.Bot(
        command_prefix = '!',
        guild_subscriptions = True,
        intents = discord.Intents.all()
        )
test_bot.run(TEST_TOKEN)



