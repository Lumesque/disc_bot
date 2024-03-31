import discord
from discord.ext import commands
from ..cog_helpers.server_containers import ServerContainer
from ..config.globals import _G
from ..server_data import servers
from pprint import pprint

class Rank_Commands(commands.Cog):

    def __init__(self, bot, **extras):
        self.bot = bot
        self.servers = servers     

    @commands.command() 
    async def add(self, ctx): 
        members = ctx.message.mentions
        names = [member.display_name for member in members]
        for member in members:
            self.servers.add_player(ctx.guild.id, member.id, name=member.display_name)
        await ctx.send(f"Added {', '.join(names)}")

    @commands.command()
    async def reward(self, ctx, score):
        members = ctx.message.mentions
        names = [member.display_name for member in members]
        for member in members:
            self.servers.get_player(ctx.guild.id, member.id, name=member.display_name).score += int(score)
        await ctx.send(f"Updated scores for {', '.join(names)}")

    @commands.command()
    async def punish(self, ctx, score):
        members = ctx.message.mentions
        names = [member.display_name for member in members]
        for member in members:
            self.servers.get_player(ctx.guild.id, member.id, name=member.display_name).score -= int(score)
        await ctx.send(f"Updated scores for {', '.join(names)}")
        
    @commands.command()
    async def ranks(self, ctx):
        server = self.servers.get_server(ctx.guild.id)
        _list = list(sorted(server.values(), key=lambda x: x.score, reverse=True))
        await ctx.send(_list)
        embed = discord.Embed(
                title = "Leaderboard",
                color = discord.Color.blue(),
        )
        embed.add_field(
                name = "Rank",
                value= "\n".join(str(x) for x in list(range(1, len(_list) + 1))),
                inline = True
        )
        embed.add_field(
                name = "Name",
                value= "\n".join([x.name for x in _list]),
                inline = True
        )
        embed.add_field(
                name = "Score",
                value= "\n".join([str(x) for x in [x.score for x in _list]]),
                inline = True
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def see_server(self, ctx):
        server = self.servers.get_server(ctx.guild.id)
        await ctx.send(server)
