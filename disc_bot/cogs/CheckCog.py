import discord
from discord.ext import commands
from ..server_data import servers

class Checks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def is_blacklisted(self, guild_id, channel_id):
        server = servers.get_server(guild_id)
        if "blacklisted_channels" not in server:
            server["blacklisted_channels"] = []
        return channel_id in server["blacklisted_channels"]

async def setup(bot):
    await bot.add_cog(Checks(bot))
