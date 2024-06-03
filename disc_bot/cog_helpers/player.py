from dataclasses import dataclass, InitVar
from typing import Optional
from ..config.globals import _G
import logging
logger = logging.getLogger('discord_player')

@dataclass
class DiscordPlayer:
    id: int
    server_id: int
    score: Optional[int] = None
    name: Optional[str] = None
    rank_role: Optional[str] = None

    def __post_init__(self):
        if self.score is None:
            # this must be done in post init since the definition of _G will be
            # defined on import for all instances of this class 
            self.score = _G.DEFAULT_SCORE
            
    @classmethod
    def from_context(cls, ctx):
        return cls(ctx.author.id, ctx.guild.id, name=ctx.author.display_name)

    def __hash__(self):
        return self.id
