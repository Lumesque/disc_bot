from discord.ext import commands

class Rank_Commands(commands.Cog):

    def __init__(self, bot, **extras):
        self.bot = bot

    @commands.command()
    async def ranks(self, ctx):
        await ctx.channel.send(ranks)
