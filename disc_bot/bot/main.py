import os
import discord
import logging

from discord.ext import commands
from ..cogs import cogs_list
from ..utils import is_admin

logger = logging.getLogger("bot")

def run(token, intents):
    bot = commands.Bot(
            command_prefix = '!',
            guild_subscriptions = True,
            intents = intents 
            )

    @bot.event
    async def on_ready():
        await setup(bot)

    async def setup(bot):
        for cog in cogs_list:
            await bot.add_cog(cog(bot))
        logger.debug(
                f"Successfully registered {', '.join([str(x) for x in cogs_list])}"
                )
        # Use this to create a custom event
#        bot.dispatch("test_event", 1, 2)

    @bot.command()
    @commands.check(is_admin)
    async def ping(ctx):
        await ctx.send("Pong!")

    bot.run(token)
