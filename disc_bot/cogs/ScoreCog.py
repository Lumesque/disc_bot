import discord
from discord.ext import commands
from ..config.globals import _G
from ..server_data import servers
import logging
logger = logging.getLogger("score_manager")

def get_roles(old_score, new_score, role_info):
    new_role = None
    for _id in role_info:
        lower, higher = role_info[_id]
        if new_score > lower and new_score < higher:
            new_role = _id
    return new_role

class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = servers

    @commands.Cog.listener()
    async def on_role_threshold(self, ctx, user, role_info, new_role_id):
        roles_to_remove = [x for x in role_info if x != new_role_id]
        print("Roles:", role_info)
        print("Roles to remove:", roles_to_remove)
        print("Roles to add:", new_role_id)
        for _id in roles_to_remove:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, id=_id))
        if new_role_id is not None:
            await user.add_roles(discord.utils.get(ctx.guild.roles, id=new_role_id))
            player = self.servers.get_player(ctx.guild.id, user.id)
            player.rank_role = new_role_id

    def update_score(self, ctx, guild_id, member_id, name, change):
        player = self.servers.get_player(guild_id, member_id, name)
        old_score = player.score
        player.score += change
        role_info = servers.get_server(guild_id).get("roles", {})
        user = discord.utils.get(ctx.guild.members, id=member_id)
        old_role = player.rank_role
        new_role = get_roles(old_score, player.score, role_info)
        print("Got", old_role, new_role)

        if old_role != new_role:
            self.bot.dispatch("role_threshold", ctx, user, role_info, new_role)
