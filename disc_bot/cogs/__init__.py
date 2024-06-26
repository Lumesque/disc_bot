import os
from pathlib import Path
from .TranslatorCog import Translation_Commands
from .BlankCog import BlankCog
from .RankCog import Rank_Commands
from .BidCog import Bidding_Commands
from .AdminCog import Admin_Commands
from .ScoreCog import Scores

cogs_list = [
    Translation_Commands,
    BlankCog,
    Rank_Commands, 
    Bidding_Commands,
    Admin_Commands,
    Scores,
]
