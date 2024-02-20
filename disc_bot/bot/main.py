import os
import discord
import logging

from discord.ext import commands
from cogs import cogs_list
from dotenv import load_dotenv
if not load_dotenv():
    raise FileNotFoundError("No .env")

logger = logging.getLogger("bot")

def run_bot():
    bot = commands.Bot(
            command_prefix = '!',
            guild_subscriptions = True,
            intents = discord.Intents.all()
            )

    @bot.event
    async def on_ready():
        await setup(bot)

    async def setup(bot):
        for cog in cogs_list:
            bot.add_cog(cog(bot))
        logger.debug(
                f"Successfully registered {', ',join(cogs_list)}"
                )

    bot.run(os.getenv["BOT_TOKEN"])
