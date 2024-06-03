from discord.ext import commands
from ..config.globals import _G
from ..server_data import servers, history
from typing import Any
import argparse
import shlex
import re
import json

def get_role_ids(_msg):
    print(_msg)
    return [int(x) for x in re.findall("\d{19}", _msg)]

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
        await ctx.send(f"Added {', '.join([str(x) for x in roles])} to admin roles")

    @commands.command(hidden=True)
    async def remove_admin_roles(self, ctx):
        roles = get_role_ids(ctx.message.content)
        server = servers.get_server(ctx.guild.id)
        current_admin_list = server.get("admin_ids", [])
        server["admin_ids"] = [role_id for role_id in current_admin_list if role_id not in roles]
        await ctx.send(f"Removed {', '.join([str(x) for x in roles])} from admin roles")

    @commands.command(hidden=True)
    async def add_points_to_role(self, ctx, role_id, lower_point, greater_point):
        if lower_point > greater_point:
            raise ValueError("lower_point must be less than greater_point")
        server = servers.get_server(ctx.guild.id)
        server["roles"][role_id] = (lower_point, greater_point)
        await ctx.send(f"Added points for role {role_id} from {lower_point} to {greater_point}")

    @commands.command(hidden=True)
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
    async def removerankrole(self, ctx):
        server = servers.get_server(ctx.guild.id)
        for _id in get_role_ids(ctx.message.content):
            if "roles" in server and _id in server["roles"]:
                server["roles"].pop(_id)
                await ctx.send(f"Removed role id {_id}")
            else:
                await ctx.send(f"Role id {_id} not found")


    @commands.command(hidden=True)
    async def save(self, ctx):
        history_data = servers.to_json()
        with history.open(mode="w") as f:
            json.dump(history_data, f, indent=4)
        await ctx.send("Saved")
