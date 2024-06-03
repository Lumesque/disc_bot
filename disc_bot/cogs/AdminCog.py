from discord.ext import commands
from ..config.globals import _G
from ..server_data import servers
from typing import Any
import argparse
import shlex
import re

def get_role_ids(_msg):
    return re.findall("\d{19}", _msg)

class toggle_autocreate(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs=0,**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        _G.AUTOCREATE = not _G.AUTOCREATE

def override__G(attr, type = str):
    class Action(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(_G, attr, type(*values))
    return Action



class Admin_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def manage(self, ctx, *args, **kwargs):
        """Manage the bot. This command is hidden from the help command."""
        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--toggle-creation", action=toggle_autocreate)
        parser.add_argument("--default-score", action=override__G("DEFAULT_SCORE", type=int), nargs=1)
        args = shlex.split(ctx.message.clean_content)
        parser.parse_known_args(args)
        await ctx.channel.send(", ".join(args))


    @commands.command(hidden=True)
    async def show_settings(self, ctx):
        await ctx.send(_G)

    @commands.command(hidden=True)
    async def show_server(self, ctx):
        server = servers.get_server(ctx.guild.id)
        await ctx.send(server)

    @commands.command(hidden=True)
    async def add_admin_roles(self, ctx):
        roles = get_role_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        current_admin_list = server.get("admin_ids", [])
        current_admin_list.extend(roles)
        server["admin_ids"] = current_admin_list
        await ctx.send(f"Added {', '.join(roles)} to admin roles")

    @commands.command(hidden=True)
    async def remove_admin_roles(self, ctx):
        roles = get_role_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        current_admin_list = server.get("admin_ids", [])
        server["admin_ids"] = [role_id for role_id in current_admin_list if role_id not in roles]
        await ctx.send(f"Removed {', '.join(roles)} from admin roles")
