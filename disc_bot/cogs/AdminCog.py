from discord.ext import commands
from ..config.globals import _G
from typing import Any
import argparse
import shlex

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
