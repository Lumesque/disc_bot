import json
import logging
from contextlib import suppress
from datetime import datetime

import discord
from discord.ext import commands, tasks

from ..cogs import delayed_extension_list, extensions_list
from ..server_data import RESOURCE_PATH, history, servers
from ..utils import is_admin, is_blacklisted, startup_check

logger = logging.getLogger("bot")


def run(token, intents):
    bot = commands.Bot(command_prefix="!", guild_subscriptions=True, intents=intents)

    @bot.event
    async def on_ready():
        await setup(bot)

    async def setup(bot):
        for cog in extensions_list:
            await bot.load_extension(cog)
        extension_names = [x.split(".")[-1] for x in extensions_list]
        logger.debug(f"Successfully registered {', '.join(extension_names)}")
        if "last_online" in servers:
            await update(datetime.fromtimestamp(servers["last_online"]))  # noqa DTZ006
        for cog in delayed_extension_list:
            await bot.load_extension(cog)
        logger.info("Bot finished setup, letting all cogs do their own")
        bot.dispatch("setup", RESOURCE_PATH)
        await save()
        bot.remove_check(startup_check)

    async def update(date):
        for guild in bot.guilds:
            for chnl in guild.text_channels:
                with suppress(discord.errors.Forbidden):
                    async for msg in chnl.history(after=date):
                        bot.dispatch("message", msg)
                        for reaction in msg.reactions:
                            bot.dispatch("reaction", reaction, msg.author)

    @bot.command(hidden=True)
    @commands.check(is_admin)
    async def shutdown(ctx):
        servers["last_online"] = datetime.now().timestamp()
        write_json_data()
        await ctx.channel.send("Bot has officially shutdown, bye!")
        bot.dispatch("close", RESOURCE_PATH)
        await bot.close()

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
    async def loggerlevel(ctx, level=commands.parameter(converter=int)):
        if level not in range(1, 6):
            raise ValueError("Level must be from 1-5")
        logging.config.fileConfig(f"disc_bot/config/output_level_{level}.cfg")
        await ctx.channel.send(f"Changed logger level to {level}")

    @tasks.loop(hours=6)
    async def save():
        servers["last_online"] = datetime.now().timestamp()
        servers["last_save"] = datetime.now().timestamp()
        write_json_data()
        logger.info("Saved json data, dispatching to bots")
        bot.dispatch("save", RESOURCE_PATH)

    def write_json_data():
        history_data = servers.to_json()
        with history.open(mode="w") as f:
            json.dump(history_data, f, indent=4)

    bot.add_check(is_blacklisted)
    # This is so that nothing starts up and sends something
    bot.add_check(startup_check)

    bot.run(token)
