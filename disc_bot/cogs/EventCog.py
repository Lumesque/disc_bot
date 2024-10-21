import logging
from collections import defaultdict
from typing import ClassVar

from discord.ext import commands

from ..cog_helpers.message_history import MessageHistory
from ..server_data import servers


class Events(commands.Cog):
    # Needed for on reaction add,
    # for if people like the same message multiple times
    RUNTIME_GLOBAL: ClassVar = defaultdict(MessageHistory)

    def __init__(self, bot):
        self.bot = bot
        self.servers = servers
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        guild = reaction.message.guild
        server = servers.get_server(guild.id)
        player = servers.get_player(guild.id, user.id, name=user.name)
        msg = reaction.message
        author = msg.author
        checker = self.bot.get_cog("Checks")
        if checker.is_blacklisted(guild.id, msg.channel.id):
            return
        elif author.id == user.id:
            self.logger.debug(f"User {author} reacted to their own msg")
            return
        history = self.RUNTIME_GLOBAL[guild.id]
        if history.has_user_reacted(msg, player, str(reaction.emoji)):
            return
        if reaction.emoji in server.get("positive_emojis", []) and "on_reaction_add_positive" in server.get(
            "events", {}
        ):
            history.add_user_message(msg, player, str(reaction.emoji))
            point_change = server["events"]["on_reaction_add_positive"]
            scores = self.bot.get_cog("Scores")
            scores.update_score_no_ctx(user, guild.id, user.id, user.name, change=point_change)
            scores.update_score_no_ctx(author, guild.id, author.id, author.name, change=point_change // 2)
            self.logger.debug(
                f"User {user.name} reacted *positively* to {author.name} message, adding {point_change} to {user.name} and {point_change//2} to {author.display_name}"
            )
        if reaction.emoji in server.get("negative_emojis", []) and "on_reaction_add_negative" in server.get(
            "events", {}
        ):
            history.add_user_message(msg, player, str(reaction.emoji))
            point_change = server["events"]["on_reaction_add_negative"]
            scores = self.bot.get_cog("Scores")
            scores.update_score_no_ctx(user, guild.id, user.id, user.name, change=-point_change)
            scores.update_score_no_ctx(author, guild.id, author.id, author.name, change=-(point_change // 2))
            self.logger.debug(
                f"User {user.name} reacted *negatively* to {author.name} message, removing {point_change} to {user.name} and {point_change//2} to {author.display_name}"
            )

    @commands.Cog.listener()
    async def on_message(self, msg):
        checker = self.bot.get_cog("Checks")
        if checker.is_blacklisted(msg.guild.id, msg.channel.id):
            return
        elif msg.author != self.bot.user:
            server = self.servers.get_server(msg.guild.id)
            events = server.get("events", {})
            if "on_message" in events:
                point_change = server["events"]["on_message"]
                scores = self.bot.get_cog("Scores")
                scores.update_score_no_ctx(
                    msg.author, msg.guild.id, msg.author.id, msg.author.name, change=point_change
                )


async def setup(bot):
    await bot.add_cog(Events(bot))
