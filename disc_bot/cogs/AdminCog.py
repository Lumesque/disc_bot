import discord
from discord.ext import commands
from ..config.globals import _G
from ..server_data import servers, history
from ..utils import is_admin
from typing import Any
import argparse
import shlex
import re
import json
import logging

def get_role_ids(_msg):
    return [int(x) for x in re.findall("\d{19}", _msg)]

def get_channel_ids(_msg):
    return [int(x) for x in re.findall("\d+", _msg)]


class toggle_autocreate_user(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        _G.AUTOCREATE_USER = not _G.AUTOCREATE_USER


class toggle_autocreate_server(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        _G.AUTOCREATE_SERVER = not _G.AUTOCREATE_SERVER


def override__G(attr, type=str):
    class Action(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(_G, attr, type(*values))
    return Action


class Admin_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.command(hidden=True)
    async def print(self, ctx):
        await ctx.channel.send(ctx.message.content)
        await ctx.channel.send(ctx.message.clean_content)

    @commands.command(hidden=True)
    async def addposemoji(self, ctx, emoji):
        server = servers.get_server(ctx.guild.id)
        if not "positive_emojis" in server:
            server["positive_emojis"] = []
        server["positive_emojis"].append(emoji)
        ctx.channel.send(f"Added {emoji} to positive emojis")

    @commands.command(hidden=True)
    async def addnegemoji(self, ctx, emoji):
        server = servers.get_server(ctx.guild.id)
        if not "negative_emojis" in server:
            server["negative_emojis"] = []
        server["negative_emojis"].append(emoji)
        ctx.channel.send(f"Added {emoji} to negative emojis")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def manage(self, ctx, *args, **kwargs):
        """Manage the bot. This command is hidden from the help command."""
        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--toggle-user-creation", action=toggle_autocreate_user)
        parser.add_argument("--toggle-server-creation", action=toggle_autocreate_server)
        parser.add_argument("--default-score", action=override__G("DEFAULT_SCORE", type=int), nargs=1)
        args = shlex.split(ctx.message.clean_content)
        if '--help' in args or '-h' in args:
            await ctx.channel.send(f"""
            Usage: !manage [--toggle-user-creation] [--toggle-server-creation] [--default-score]
            Sets global settings, current settings:
                User creation: {'on' if _G.AUTOCREATE_USER else 'off'}
                Server creation: {'on' if _G.AUTOCREATE_SERVER else 'off'}
                Default Score: {_G.DEFAULT_SCORE}

            Type !manage 'show-admin' to see a list of admin commands and what they do
            """)
        elif "show-admin" in args:
            await ctx.channel.send("""Displaying help...
__**Show Code**__
!show_settings
    Shows the current global object
!show_server
    Shows the current server object

__**Server Control**__
!manage [--toggle-user-creation] [--toggle-server-creation] [--default-score SCORE]
    Toggles autocreation and global variables
!sync
    Syncs current interaction app commands to global guild tree
!addblacklist <channelids...>
    Blacklist channels from the bot
!removeblacklist <channelids...>
    Remove blacklisted channels from the bot

__**Role Control**__
!add_admin_roles <role_ids...>
    Adds admin priveleges to role ids given
!remove_admin_roles <role_ids...>
    Removes admin priveleges to role ids given
!addrankrole <lower_point>, <greater_point> roleids...
    Adds a role to be given when a player hits between two point numbers
!removerankrole <lower_point>, <greater_point> roleids...
    Removes a role to be given when a player hits between two point numbers

__**Point Control**__
!reward <points> @users...
    Gives players points
!punish <points> @users
    Removes players points
!add_event "event", points
    Adds an event and the corresponding number of points,
    current valid events are:
        on_reaction_add_positive
        on_reaction_add_negative
        on_message
!change_event "event", points
    Overrides the points set for an event that will be gained/lost
        on_reaction_add_positive
        on_reaction_add_negative
        on_message
!addposemoji emoji
    Adds an emoji considered positive for points
!addnegemoji emoji
    Adds an emoji considered negative for points

__**Rank Control**__
!add @users
    Adds users to the rankings
!remove @users
    Removes users from the rankings

__**Code settings**__
!save
    Saves the current state of the bot
!unload <Cog> # TODO
    Unloads cog
!load <Cog> # TODO
    loads cog
!reload <Cog> # TODO
    reloads cog
!print ...
    Prints a message how the bot receives it
           """)
        else:
            parser.parse_known_args(args)

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def show_settings(self, ctx):
        await ctx.send(_G)

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def show_server(self, ctx):
        server = servers.get_server(ctx.guild.id)
        await ctx.send(server)

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def add_admin_roles(self, ctx):
        roles = get_role_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        current_admin_list = server.get("admin_ids", [])
        current_admin_list.extend(roles)
        server["admin_ids"] = current_admin_list
        await ctx.send(f"Added {', '.join([str(x) for x in roles])} to admin roles")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def remove_admin_roles(self, ctx):
        roles = get_role_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        current_admin_list = server.get("admin_ids", [])
        server["admin_ids"] = [role_id for role_id in current_admin_list if role_id not in roles]
        await ctx.send(f"Removed {', '.join([str(x) for x in roles])} from admin roles")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def add_points_to_role(self, ctx, role_id, lower_point, greater_point):
        if lower_point > greater_point:
            raise ValueError("lower_point must be less than greater_point")
        server = servers.get_server(ctx.guild.id)
        server["roles"][role_id] = (lower_point, greater_point)
        await ctx.send(f"Added points for role {role_id} from {lower_point} to {greater_point}")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def addrankrole(self, ctx, role,
          lower_point=commands.parameter(default=float("-inf"), converter=float),
          greater_point=commands.parameter(default=float("inf"), converter=float)
        ):
        if lower_point > greater_point:
            raise ValueError("lower_point must be less than greater_point, syntax is: !addrankrole <role> <lower_point> <greater_point>")
        role_id = get_role_ids(ctx.message.content)[0]
        server = servers.get_server(ctx.guild.id)
        if not "roles" in server:
            server["roles"] = {}
        server["roles"][role_id] = (lower_point, greater_point)
        await ctx.send(f"Added points threshold for role {role_id} from {lower_point} to {greater_point}")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def removerankrole(self, ctx):
        server = servers.get_server(ctx.guild.id)
        for _id in get_role_ids(ctx.message.content):
            if "roles" in server and _id in server["roles"]:
                server["roles"].pop(_id)
                await ctx.send(f"Removed role id {_id}")
            else:
                await ctx.send(f"Role id {_id} not found")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def save(self, ctx):
        history_data = servers.to_json()
        with history.open(mode="w") as f:
            json.dump(history_data, f, indent=4)
        await ctx.send("Saved")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def change_event(
        self,
        ctx,
        event,
        points=commands.parameter(converter=int),
    ):
        server = servers.get_server(ctx.guild.id)
        if event not in (events := server.get("events", {})):
            await ctx.channel.send("Invalid event, valid events are '{', '.join(events.keys())}")
        else:
            server["events"][event] = points

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def add_event(
        self,
        ctx,
        event,
        points=commands.parameter(converter=int),
    ):
        server = servers.get_server(ctx.guild.id)
        if not "events" in server:
            server["events"] = {}
        server["events"][event] = points

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def sync(self, ctx):
        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(content="Success!")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def addblacklist(
        self,
        ctx,
    ):
        channel_ids = get_channel_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        if "blacklisted_channels" not in server:
            server["blacklisted_channels"] = []
        server["blacklisted_channels"].extend(channel_ids)
        await ctx.send(f"Added {', '.join([str(x) for x in channel_ids])} to blacklisted channel_ids")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def removeblacklist(
        self,
        ctx,
    ):
        channel_ids = get_channel_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        if "blacklisted_channels" not in server:
            server["blacklisted_channels"] = []
        current_channel_list = server["blacklisted_channels"]
        server["blacklisted_channels"] = [x for x in current_channel_list if x not in channel_ids]
        await ctx.send(f"Removed {', '.join([str(x) for x in channel_ids])} to blacklisted channel_ids")

async def setup(bot):
    await bot.add_cog(Admin_Commands(bot))
