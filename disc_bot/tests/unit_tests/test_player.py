import pytest

from disc_bot.cog_helpers.player import DiscordPlayer
from disc_bot.cog_helpers.server_containers import ServerContainer
from disc_bot.config.globals import _G


@pytest.fixture
def server():
    container = ServerContainer()
    container.add_server(0)
    return container


@pytest.fixture
def player():
    return DiscordPlayer(0, 0)


def test_add_user(server):
    server.add_player(0, 0)
    assert len(server.get_server(0)) == 1


def test_player(player):
    assert player.score == 1000


def test_addition(player):
    player.score += 1
    assert player.score == 1001
    assert _G.DEFAULT_SCORE == 1000
