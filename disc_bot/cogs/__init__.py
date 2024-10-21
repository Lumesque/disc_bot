from .AdminCog import Admin_Commands
from .BidCog import Bidding_Commands
from .BlankCog import BlankCog
from .CheckCog import Checks
from .EventCog import Events
from .RankCog import Rank_Commands
from .ScoreCog import Scores
from .TranslatorCog import Translation_Commands

cogs_list = [
    Translation_Commands,
    BlankCog,
    Rank_Commands,
    Bidding_Commands,
    Admin_Commands,
    Scores,
    Events,
    Checks,
]

extensions_list = [
    "disc_bot.cogs.BlankCog",
    "disc_bot.cogs.RankCog",
    "disc_bot.cogs.BidCog",
    "disc_bot.cogs.AdminCog",
    "disc_bot.cogs.ScoreCog",
    "disc_bot.cogs.EventCog",
    "disc_bot.cogs.CheckCog",
    "disc_bot.cogs.RouletteCog",
]
# Values that would send out messages prior to updating the system
delayed_extension_list = [
    "disc_bot.cogs.TranslatorCog",
    "disc_bot.cogs.ErrorCog",
]
