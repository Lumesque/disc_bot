from discord.ext import commands

from ..utils import is_admin


class BlankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tp(self, ctx):
        await ctx.channel.send("Weeeee")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def test(self, ctx):
        await ctx.channel.send(":white_square_button:")


async def setup(bot):
    await bot.add_cog(BlankCog(bot))
