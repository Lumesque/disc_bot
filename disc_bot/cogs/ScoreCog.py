import logging

import discord
from discord.ext import commands

from ..server_data import servers


def get_roles(new_score, role_info):
    new_roles = []
    for _id in role_info:
        lower, higher = role_info[_id]
        if new_score > lower and new_score < higher:
            new_roles.append(_id)
    return new_roles


class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = servers
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_role_threshold(self, user, role_info, new_role_ids, guild):
        roles_to_remove = [x for x in role_info if x not in new_role_ids]
        self.logger.info(
            f"Role threshold crossed for user {user.name},\n"
            f"\tupdating for new role(s) {new_role_ids}\n"
            f"\tremoving roles {roles_to_remove}"
        )
        for _id in roles_to_remove:
            await user.remove_roles(discord.utils.get(guild.roles, id=_id))
        for _id in new_role_ids:
            await user.add_roles(discord.utils.get(guild.roles, id=_id))
        player = self.servers.get_player(guild.id, user.id)
        player.rank_role = new_role_ids

    def update_score(self, ctx, guild_id, member_id, name, change):
        player = self.servers.get_player(guild_id, member_id, name)
        old_score = player.score  # noqa F841
        player.score += change
        role_info = servers.get_server(guild_id).get("roles", {})
        user = discord.utils.get(ctx.guild.members, id=member_id)
        old_role = player.rank_role
        new_role = get_roles(player.score, role_info)

        if old_role != new_role:
            guild = user.guild
            self.bot.dispatch("role_threshold", user, role_info, new_role, guild)

    def update_score_no_ctx(self, user, guild_id, member_id, name, change):
        player = self.servers.get_player(guild_id, member_id, name)
        old_score = player.score  # noqa: F841
        player.score += change
        role_info = servers.get_server(guild_id).get("roles", {})
        old_roles = player.rank_role or []
        new_roles = get_roles(player.score, role_info)
        self.logger.debug(f"New roles are {new_roles}, old_roles = {old_roles}")

        if not all(x in new_roles for x in old_roles):
            guild = user.guild
            self.bot.dispatch("role_threshold", user, role_info, new_roles, guild)


async def setup(bot):
    await bot.add_cog(Scores(bot))
