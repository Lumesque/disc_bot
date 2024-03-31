from discord.ext import commands
from ..cog_helpers.server_containers import ServerContainer
from ..config.globals import _G
from pprint import pprint

class Rank_Commands(commands.Cog):

    def __init__(self, bot, **extras):
        self.bot = bot
        for key, value in extras.items():
            setattr(self, key, value)
        if not hasattr(self, "servers"):
            self.servers = ServerContainer()     


    @commands.command()
    async def pprint_servers(self, ctx):
        pprint(self.servers)

    @commands.command()
    async def add_server(self, ctx):
        self.servers.add_server(ctx.guild.id)

    @commands.command() 
    async def add_player(self, ctx): 
        for member in ctx.message.mentions:
            self.servers.add_player(ctx.guild.id, member.id)
        pprint(self.servers)

    @commands.command()
    async def flush(self, ctx): 
        self.servers.remove_server(ctx.guild.id)
        pprint(self.servers)

    @commands.command()
    async def get_player(self, ctx):
        pprint(self.servers.get_player(ctx.guild.id, ctx.author.id))

         
    @commands.command() 
    async def add_one(self, ctx): 
        self.servers.get_player_from_context(ctx).score += 1
        pprint(self.servers)

         
    @commands.command()
    async def remove_global(self, ctx):
        _G.AUTOCREATE = False

    @commands.command()
    async def reward_player(self, ctx, score):
        for member in ctx.message.mentions:
            self.servers.get_player_from_context(ctx).score += int(score)
        pprint(self.servers)

    @commands.command()
    async def punish_player(self, ctx, score):
        for member in ctx.message.mentions:
            self.servers.get_player(ctx.guild.id, member.id).score -= int(score)
        pprint(self.servers)
