import pytest
from disc_bot.cog_helpers.server_containers import ServerContainer

@pytest.fixture
def empty_container():
    return ServerContainer()

@pytest.fixture
def nonempty_container():
    container = ServerContainer()
    container.add_server(0)
    return container

def test_server_container(empty_container):
    assert empty_container == {}

def test_add_server(empty_container):
    empty_container.add_server(0)
    assert len(empty_container) == 1

def test_remove_server(empty_container):
    empty_container.add_server(0)
    empty_container.remove_server(0)
    assert len(empty_container) == 0

def test_get_server(nonempty_container):
    assert nonempty_container.get_server(0) == {}





