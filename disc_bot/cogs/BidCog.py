from ..cog_helpers.state_machine import StateMachine
from discord.ext import commands
from collections import namedtuple
import asyncio
import random

PlayerBid = namedtuple("PlayerBid", ["bid", "guess"])

class Bidding_Commands(commands.Cog):
    bidders = {} 
    def __init__(self, bot):
        self.bot = bot
        self.state = StateMachine()

    @commands.command()
    async def start_bid(self, ctx):
        if self.state.dead:
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

    @commands.command()
    async def end_bid(self, ctx):
        if self.state.running:
            next(self.state)
            await ctx.channel.send("Bidding has ended, please wait for final results.")
            rolled = random.randint(1, 11)
            winners, losers = "", ""
            for player, player_bid in self.bidders.items():
                if player_bid.guess == rolled:
                    player.score = player.score + \
                        player_bid.bid * (
                            1.2 + (
                                len(self.bidders) / 10
                                if len(self.bidders) < 4
                                else .4
                                )
                            )
                    winners += f"{player.name} "
                else:
                    player.score -= player_bid.bid
                    losers += f"{player.name} "
            next(self.state)
            self.bidders = {}
            await ctx.channel.send(f"""
                                   The winning number is: **
                                   ##{rolled}
                                   __Winners__:
                                       {winners}
                                   __Losers__: 
                                       {losers}
                                    Use the !start_bid command to start a new bid!
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
