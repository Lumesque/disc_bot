import pytest
from disc_bot.config.globals import _G
from disc_bot.cog_helpers.player import DiscordPlayer

@pytest.mark.trylast
def test_global_change():
    assert _G.DEFAULT_SCORE == 1000
    _G.DEFAULT_SCORE = 2000
    assert _G.DEFAULT_SCORE == 2000
    player = DiscordPlayer(0, 0)
    assert player.score == 2000
    _G.DEFAULT_SCORE = 1000
