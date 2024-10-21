import asyncio
import json
import logging
import random
from enum import Enum, auto, unique
from typing import Callable, ClassVar, NamedTuple, Optional, Union

import discord
from discord.ext import commands

from ..cog_helpers.server_containers import int_all_in_dict
from ..server_data import RESOURCE_PATH, servers
from ..utils import is_admin

FORMAT_HELP = """Single: **{}**, special (3 in a row): **{}**\n"""


@unique
class UniqueActions(Enum):
    RETURN = (auto(),)
    BANK = (auto(),)  # noqa PIE796
    LEAVE = (auto(),)  # noqa PIE796
    FREEGAME = (auto(),)  # noqa PIE796


@unique
class Stage(Enum):
    END = (auto(),)
    BEGIN = (auto(),) # noqa PIE796


class RouletteEntry(NamedTuple):
    disc_emote: str
    action: Callable
    special: Callable
    help: str
    requirement: Optional[Callable] = None
    stage: Optional[Stage] = None

    def build_help(self):
        return f"{self.disc_emote} {self.help}"


zero = RouletteEntry(
    disc_emote=":white_square_button:",
    action=lambda x: x,
    special=lambda x: x,
    help=FORMAT_HELP.format("Nothing", "Nothing"),
)
one = RouletteEntry(
    disc_emote=":skull_crossbones:",
    action=lambda x: x - 10,
    special=lambda x: x - 50,
    help=FORMAT_HELP.format("-10 points", "-50 points"),
)
two = RouletteEntry(
    disc_emote=":gem:",
    action=lambda x: x + 100,
    special=lambda x: x + 500,
    help=FORMAT_HELP.format("+100 points", "+500 points"),
)
three = RouletteEntry(
    disc_emote=":firecracker:",
    action=UniqueActions.LEAVE,
    special=lambda x: x - 100,
    stage=Stage.BEGIN,
    help=FORMAT_HELP.format("No points gained or lost", "-100 points"),
)
four = RouletteEntry(
    disc_emote=":seven:",
    action=lambda x: x,
    special=UniqueActions.BANK,
    help=FORMAT_HELP.format("Nothing", "All points in the bank"),
)
five = RouletteEntry(
    disc_emote=":cherries:",
    action=lambda x: x + 30,
    special=lambda x: x + 120,
    help=FORMAT_HELP.format("+30 points", "+120 points"),
)
six = RouletteEntry(
    disc_emote=":tangerine:",
    action=lambda x: x + 10,
    special=lambda x: x + 40,
    help=FORMAT_HELP.format("+10 points", "+40 points"),
)
seven = RouletteEntry(
    disc_emote=":pear:",
    action=lambda x: x + 5,
    special=lambda x: x + 20,
    help=FORMAT_HELP.format("+5 points", "+20 points"),
)
eight = RouletteEntry(
    disc_emote=":watermelon:",
    action=lambda x: x * 1.5,
    special=UniqueActions.RETURN,
    stage=Stage.END,
    help=FORMAT_HELP.format("1.5x multiplier", "Nothing"),
)
nine = RouletteEntry(
    disc_emote=":grapes:",
    action=lambda x: x * 2,
    special=lambda x: UniqueActions.FREEGAME, # noqa ARG005
    help=FORMAT_HELP.format("2x multiplier", "Free game"),
)

entries = {"0": zero, "1": one, "2": two, "3": three, "4": four, "5": five, "6": six, "7": seven, "8": eight, "9": nine}


def build_help() -> str:
    string = ""
    for roulette in entries.values():
        string += roulette.build_help()
    return string


HELP_STR = build_help()


class Roulette(commands.Cog):
    "Roulette Cog, use !gamble to gamble or !gamblehelp to learn more!"

    player_bank: ClassVar = 0
    free_games: ClassVar[dict] = {}

    def __init__(self, bot):
        self.bot = bot
        self.servers = servers
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_setup(self, path):
        if (p := (path / "bank.json")).exists():
            with p.open(mode="r") as f:
                self.free_games = int_all_in_dict(json.load(f))
            self.player_bank = self.free_games.get("bank", 0)

    @commands.Cog.listener()
    async def on_save(self, path):
        self.logger.info(f"Saving to {path}/bank.json")
        with (path / "bank.json").open(mode="w") as f:
            self.free_games["bank"] = self.player_bank
            json.dump(self.free_games, f, indent=4)

    @commands.Cog.listener()
    async def on_close(self, path):
        await self.on_save(path)

    @commands.command()
    async def bank(self, ctx):
        "See how many points are currently in the bank"
        await ctx.channel.send(f"Current points in the bank: {self.player_bank}")

    def add_player_freegame(self, guild_id, player_id):
        if guild_id not in self.free_games:
            self.free_games[guild_id] = {}
        if player_id not in self.free_games[guild_id]:
            self.free_games[guild_id][player_id] = 0
        self.free_games[guild_id][player_id] += 1

    def has_freegame(self, guild_id, player_id) -> bool:
        return player_id in self.free_games.get(guild_id, {}) and self.free_games[guild_id][player_id] > 0

    def use_freegame(self, guild_id, player_id) -> None:
        self.free_games[guild_id][player_id] -= 1

    @commands.command()
    async def slot(self, ctx: commands.Context) -> None:
        "Gamble the days away!"
        # Original points to be tallied or removed
        points = 0
        out = str(random.randint(100, 999))
        template = f"""Gambling...
        __**Starting Roulette for {ctx.author.display_name}**__

        {{}} {{}} {{}}
        """
        finished_template = f"""Gambled...
        __**Finished Roulette for {ctx.author.display_name}**__

        {{}} {{}} {{}}
        Point change: {{}}
        """
        msg, out = await self.countdown_timer(ctx, template)
        if out[0] == out[1] == out[2]:
            action = entries[out[0]].special
            tmp = self._process_action(action, points)
            if tmp == UniqueActions.LEAVE:
                pass
            elif tmp == UniqueActions.FREEGAME:
                self.add_player_freegame(ctx.guild.id, ctx.author.id)
            else:
                points = tmp
        # Not a special case, process each
        else:
            # Process twice, one for order
            order = []
            end = []
            for n in out:
                x = entries[n]
                match x.stage:
                    case Stage.END:
                        end.append(x)
                    case Stage.BEGIN:
                        order.insert(0, x)
                    case _:
                        order.append(x)
            order.extend(end)

            for act in order:
                tmp = self._process_action(act.action, points)
                if tmp == UniqueActions.LEAVE:
                    break
                points = tmp
        if points < 0:
            self.player_bank += abs(points)
            if self.has_freegame(ctx.guild.id, ctx.author.id):
                points = f"0, you had a free game! Would have lost {abs(points)}"
                await msg.edit(content=self.fstr(out[0], out[1], out[2], finished_template, points))
                self.use_freegame(ctx.guild.id, ctx.author.id)
                return
        await msg.edit(content=self.fstr(out[0], out[1], out[2], finished_template, points))
        scores = self.bot.get_cog("Scores")
        scores.update_score(ctx, ctx.guild.id, ctx.author.id, name=ctx.author.display_name, change=points)

    @commands.command()
    @commands.check(is_admin)
    async def give_free_game(self, ctx):
        members = ctx.message.mentions
        for member in members:
            self.add_player_freegame(ctx.guild.id, member.id)

    @commands.command()
    async def freegames(self, ctx):
        "See who has free games"
        _str = "__Those with free games:__\n"
        for gamers in self.free_games.get(ctx.guild.id, {}):
            if self.free_games[ctx.guild.id][gamers] > 0:
                user = discord.utils.get(ctx.guild.members, id=gamers)
                _str += f"**{user.display_name}**\n"

        await ctx.channel.send(_str)

    def fstr(self, x, y, z, template, *args):
        return template.format(entries[x].disc_emote, entries[y].disc_emote, entries[z].disc_emote, *args)

    async def countdown_timer(self, ctx, str_template):
        fstr = lambda x, y, z: self.fstr(x, y, z, str_template) # noqa E731
        msg = await ctx.send(fstr(*"000"))
        total_seconds = 2
        while total_seconds > 0:
            current_time = 1 / random.randint(1, 2)
            asyncio.sleep(current_time)
            out = str(random.randint(100, 999))
            await msg.edit(content=fstr(*out))
            total_seconds -= current_time
        return msg, out

    def _process_action(self, action: Union[Callable, UniqueActions], points: int) -> Union[int, UniqueActions]:
        match action:
            case UniqueActions.RETURN:
                return points
            case UniqueActions.BANK:
                points += self.player_bank
                self.player_bank = 0
                return points
            case UniqueActions.LEAVE:
                return UniqueActions.LEAVE
            case UniqueActions.FREEGAME:
                return UniqueActions.FREEGAME
            case _:
                if callable(action):
                    return action(points)
                else:
                    raise ValueError(f"Unexplained action {action}")

    @commands.command()
    async def slothelp(self, ctx):
        "Display what each icon does"
        string = ""
        for roulette in entries.values():
            string += roulette.build_help()
        await ctx.channel.send(f"Help for roulette wheel, the following symbols mean the following things: \n{string}")

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def checkbank(self, ctx):
        await ctx.channel.send(self.free_games)


async def setup(bot):
    cog = Roulette(bot)
    await cog.on_setup(RESOURCE_PATH)
    await bot.add_cog(cog)


async def teardown(bot):
    cog = bot.get_cog("Roulette")
    await cog.on_close(RESOURCE_PATH)
