from dataclasses import dataclass, InitVar
from typing import Optional
from ..config.globals import _G

@dataclass
class DiscordPlayer:
    id: int
    server_id: int
    score: Optional[int] = None

    def __post_init__(self):
        if self.score is None:
            # this must be done in post init since the definition of _G will be
            # defined on import for all instances of this class 
            self.score = _G.DEFAULT_SCORE