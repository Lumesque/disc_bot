import os
from ...cli.run_bot import get_process
from ...exceptions.handling import print_traceback
from dotenv import load_dotenv
import discord
from contextlib import suppress
from discord.ext import commands
import re

if not load_dotenv():
    raise FileNotFoundError("No .env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
DISC_CHANNEL = int(os.getenv("CHANNEL_ID"))
ADMIN_ROLE = int(os.getenv("ADMIN_ROLE"))

def get_channel(bot_obj):
    return bot_obj.get_channel(DISC_CHANNEL)

process = get_process(BOT_TOKEN, discord.Intents.all())
process.start()
bot = commands.Bot(
        command_prefix = '!',
        guild_subscriptions = True,
        intents = discord.Intents.all()
        )

@bot.event
async def on_ready():
    channel = get_channel(bot)
    with print_traceback("Bot did not translate"):
        assert await assert_no_response(bot, channel, command="!ping"), "Bot failed to fail admin check"
        assert await assert_adding_role(bot, channel, ADMIN_ROLE), "Bot failed to add admin role"
        assert await assert_response(bot, channel, command="!ping"), "Bot failed to pass admin check"
        print("Bot passed admin check!")
    # fuck dat shit up
    process.kill()
    await bot.close()

def msg_contains(_id):
    def check(m):
        return re.find(_id, m.content) is None
    return check

async def assert_adding_role(bot, channel, role_id):
    _msg = await channel.send(f"!add_admin_roles {role_id}")
    with suppress(TimeoutError):
        # This should fail so check doesn't matter
        #_ = await bot.wait_for('message', check=check, timeout=3)
        _ = await bot.wait_for('message', check = msg_contains(role_id), timeout=3)
        return True
    return False

async def assert_no_response(bot, channel, command="!ping"):
    _msg = await channel.send(command)
    with suppress(TimeoutError):
        # This should fail so check doesn't matter
        #_ = await bot.wait_for('message', check=check, timeout=3)
        _ = await bot.wait_for('message', timeout=3)
        return False
    return True

async def assert_response(bot, channel, command="!ping"):
    _msg = await channel.send(command)
    with suppress(TimeoutError):
        # This should fail so check doesn't matter
        #_ = await bot.wait_for('message', check=check, timeout=3)
        _ = await bot.wait_for('message', timeout=3)
        return True
    return False

bot.run(TEST_TOKEN)
