from discord.ext import commands

class BlankCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tp(self, ctx):
        await ctx.channel.send("Weeeee")

async def setup(bot):
    await bot.add_cog(BlankCog(bot))
