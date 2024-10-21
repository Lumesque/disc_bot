import discord
from discord.ext import commands

from ..cog_helpers.server_containers import IGNORED_KEYS
from ..server_data import servers
from ..utils import is_admin


class Rank_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = servers

    @commands.command()
    @commands.check(is_admin)
    async def add(self, ctx):
        members = ctx.message.mentions
        names = [member.display_name for member in members]
        for member in members:
            self.servers.add_player(ctx.guild.id, member.id, name=member.display_name)
        await ctx.send(f"Added {', '.join(names)}")

    @commands.command()
    @commands.check(is_admin)
    async def reward(self, ctx, score=commands.parameter(converter=float)):
        members = ctx.message.mentions
        names = [member.display_name for member in members]
        scores = self.bot.get_cog("Scores")
        for member in members:
            scores.update_score(ctx, ctx.guild.id, member.id, name=member.display_name, change=score)
        await ctx.send(f"Updated scores for {', '.join(names)}")

    @commands.command()
    @commands.check(is_admin)
    async def punish(self, ctx, score=commands.parameter(converter=float)):
        members = ctx.message.mentions
        names = [member.display_name for member in members]
        scores = self.bot.get_cog("Scores")
        for member in members:
            scores.update_score(ctx, ctx.guild.id, member.id, name=member.display_name, change=-score)
        await ctx.send(f"Updated scores for {', '.join(names)}")

    @commands.command()
    async def ranks(self, ctx):
        "See the current rankings in this server"
        server = self.servers.get_server(ctx.guild.id)
        server = {k: v for k, v in server.items() if k not in IGNORED_KEYS}
        _list = sorted(server.values(), key=lambda x: x.score, reverse=True)
        embed = discord.Embed(
            title="Leaderboard",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Rank", value="\n".join(str(x) for x in list(range(1, len(_list) + 1))), inline=True)
        embed.add_field(name="Name", value="\n".join([x.name for x in _list]), inline=True)
        embed.add_field(name="Score", value="\n".join([str(x) for x in [x.score for x in _list]]), inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Rank_Commands(bot))
