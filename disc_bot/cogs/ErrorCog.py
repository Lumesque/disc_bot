import logging

from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MemberNotFound, MissingRequiredArgument


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if any(type(error) is X for X in (MemberNotFound, MissingRequiredArgument, CommandNotFound)):
            await ctx.send(f"Error: {error}")
        else:
            self.logger.warning(
                f"Ignoring exception of type {type(error)} in {ctx.command}: {error}\n{error.__traceback__}"
            )


async def setup(bot):
    await bot.add_cog(Errors(bot))
