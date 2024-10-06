import os
import discord
import logging
import json

from discord.ext import commands, tasks
from ..cogs import extensions_list
from ..utils import is_admin, is_blacklisted
from ..server_data import servers, history

logger = logging.getLogger("bot")


def run(token, intents):
    bot = commands.Bot(
        command_prefix='!',
        guild_subscriptions=True,
        intents=intents
    )

    @bot.event
    async def on_ready():
        await setup(bot)

    async def setup(bot):
        for cog in extensions_list:
            print(cog)
            await bot.load_extension(cog)
        extension_names = [x.split('.')[-1] for x in extensions_list]
        logger.debug(
            f"Successfully registered {', '.join(extension_names)}"
        )

    @bot.command()
    @commands.check(is_admin)
    async def ping(ctx):
        await ctx.send("Pong!")

    @bot.command()
    @commands.check(is_admin)
    async def unload(ctx, extension):
        out = await bot.unload_extension(f"disc_bot.cogs.{extension}")
        await ctx.channel.send(f"Unloaded {out}")

    @bot.command()
    @commands.check(is_admin)
    async def load(ctx, extension):
        out = await bot.load_extension(f"disc_bot.cogs.{extension}")
        await ctx.channel.send(f"Loaded {out}")

    @bot.command()
    @commands.check(is_admin)
    async def reload(ctx, extension):
        out = await bot.reload_extension(f"disc_bot.cogs.{extension}")
        await ctx.channel.send(f"Reloaded {out}")

    @bot.command()
    @commands.check(is_admin)
    async def loggerlevel(
        ctx,
        level=commands.parameter(converter=int)
    ):
        if level not in range(1,6):
            raise ValueError("Level must be from 1-5")
        logging.config.fileConfig(f"disc_bot/config/output_level_{level}.cfg")

    @tasks.loop(hours=6)
    async def save():
        history_data = servers.to_json()
        with history.open(mode="w") as f:
            json.dump(history_data, f, indent=4)
        logger.info(f"Saved json data")

    bot.add_check(is_blacklisted)

    bot.run(token)
