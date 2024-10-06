from ..cog_helpers.state_machine import StateMachine
import discord
from discord import app_commands
from discord.ext import commands
from collections import namedtuple
from ..server_data import servers
import asyncio
import random
import logging

PlayerBid = namedtuple("PlayerBid", ["bid", "guess"])

class Bidding_Commands(commands.Cog):
    bidders = {}
    def __init__(self, bot):
        self.bot = bot
        self.state = StateMachine()
        self.servers = servers
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.command()
    async def start_bid(self, ctx):
        if self.state.dead:
            self.logger.info("Starting bid...")
            next(self.state)
            asyncio.create_task(self.timer(ctx))
            await ctx.channel.send("""
            Bidding has started and is open for 60 seconds. To join, please use the /join command followed by a number of points you're willing to offer.
            Potentially earn 120-160% of your original bid! Number increases based on the amount of players that join.
            """)
        else:
            await ctx.channel.send("Bidding has already started.")

    @commands.command()
    async def join(self, ctx, bid, guess):
        if self.state.running:
            cog = self.bot.get_cog('Rank_Commands')
            player = cog.servers.get_player_from_context(ctx)
            bid, guess = float(bid), int(guess)
            if bid > player.score:
                await ctx.channel.send("You don't have that many points!")
            else:
                self.bidders[player] = PlayerBid(bid, guess)
        else:
            await ctx.channel.send("Bidding has not yet started.")

    @discord.app_commands.command()
    async def join(self, interaction, bid: app_commands.Range[float, .1], guess: app_commands.Range[int, 1, 10]):
        if not self.state.running:
            await interaction.response.send_message("No bid is currently going on")
        else:
            author = interaction.user
            player = self.servers.get_player(interaction.guild.id, interaction.user.id, interaction.user.name)
            if bid > player.score:
                await interaction.response.send_message(f"You're capped at {player.score:.2f}, you're bidding too much")
            else:
                self.bidders[player] = PlayerBid(bid, guess)
                await interaction.response.send_message(f"{author} has bet {bid:.2f} with a guess of {guess}!")

    @commands.command()
    async def end_bid(self, ctx):
        if self.state.running:
            next(self.state)
            await ctx.channel.send("Bidding has ended, please wait for final results.")
            rolled = random.randint(1, 11)
            self.logger.debug(f"Number rolled: {rolled}")
            winners, losers = "", ""
            scores = self.bot.get_cog('Scores')
            for player, player_bid in self.bidders.items():
                if player_bid.guess == rolled:
                    change = player.score + \
                        player_bid.bid * (
                            1.2 + (
                                len(self.bidders) / 10
                                if len(self.bidders) < 4
                                else .4
                                )
                            )
                    scores.update_score(ctx, ctx.guild.id, player.id, name=player.name, change=change)
                    winners += f"{player.name} "
                else:
                    scores.update_score(ctx,ctx.guild.id, player.id, name=player.name, change=-player_bid.bid)
                    losers += f"{player.name} "
            next(self.state)
            self.bidders = {}
            await ctx.channel.send(f"""
               The winning number is: **
               ## {rolled}
               __Winners__:
                   {winners}
               __Losers__:
                   {losers}
                `Use the !start_bid command to start a new bid!`
            """)
        else:
            await ctx.channel.send("Bidding has not yet started.")

    async def timer(self, ctx):
        timer = 60
        msg = await ctx.send("Time left: " + str(timer))
        while timer > 0:
            await asyncio.sleep(1)
            timer -= 1
            if self.state.dead: break
            await msg.edit(content="Time left: " + str(timer))
        if self.state.running:
            self.end_bid

async def setup(bot):
    await bot.add_cog(Bidding_Commands(bot))
