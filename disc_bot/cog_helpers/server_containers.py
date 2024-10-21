import dataclasses as dc
import warnings
from collections import UserDict
from copy import deepcopy
from typing import Iterable

from ..config.globals import _G
from ..exceptions.ranks import PlayerNotFoundError
from .player import DiscordPlayer

IGNORED_KEYS = (
    "admin_ids",
    "roles",
    "events",
    "positive_emojis",
    "negative_emojis",
    "blacklisted_channels",
    "last_online",
    "last_save",
)


def int_all_in_dict(x: dict):
    """
    {
      '<server_id>': {
          'admin_ids': [<role_id>, <role_id>, ...],
          'roles': {
            '<role_id>': (<lower_point>, <greater_point>),
            ...
          },
          '<user_id>':
            {
              'score': <score>,
              'name': <name>
            }
        }
    }
    """
    converter = lambda x: int(x) if isinstance(x, str) and x.isdigit() else x  # noqa
    return {
        converter(k): int_all_in_dict(v)
        if isinstance(v, dict)
        else [converter(x) for x in v]
        if isinstance(v, (list, tuple))
        else v
        for k, v in x.items()
    }


class ServerContainer(UserDict):
    def get_player(self, server_id, user_id, name=None):
        player = self.get_server(server_id).get(user_id, None)
        if player is None:
            if _G.AUTOCREATE_USER:
                player = self.add_player(server_id, user_id, name=name)
                warnings.warn(
                    "Player does not exist, creating new player. If you would like to not see this message, please disable auto-creation, or add player and save",
                    stacklevel=2,
                )
            else:
                raise PlayerNotFoundError(f"Player {user_id} not found in server {server_id}")
        return player

    def get_player_from_context(self, ctx):
        return self.get_player(ctx.guild.id, ctx.author.id, name=ctx.author.display_name)

    def get_server(self, server_id):
        server = self.data.get(server_id, None)
        if server is None:
            if _G.AUTOCREATE_SERVER:
                server = self.add_server(server_id)
                warnings.warn(
                    "Server does not exist, creating new server. If you would like to not see this message, please disable auto-creation, or add server and save",
                    stacklevel=2,
                )
            else:
                raise KeyError(f"Server {server_id} does not exist")
        return server

    def add_server(self, server_id):
        if server_id not in self.data:
            self.data[server_id] = {}
        return self.data[server_id]

    def add_player(self, server_id, user_id, name=None):
        server = self.get_server(server_id)
        server[user_id] = (player := DiscordPlayer(user_id, server_id, name=name))
        return player

    def remove_server(self, server_id):
        self.data.pop(server_id, None)

    @classmethod
    def from_history(cls, json_data):
        """
        {
          '<server_id>':
            'admin_ids': [<role_id>, <role_id>, ...],
            'roles': {
              '<role_id>': (<lower_point>, <greater_point>),
              ...
            },
          '<user_id>':
            {
              'score': <score>,
              'name': <name>
            }
        """
        # Turn all numerics into numerical for searching
        json_data = int_all_in_dict(json_data)
        for server_id in json_data:
            temp = json_data[server_id]
            if (not isinstance(temp, Iterable)) or isinstance(temp, str):
                continue
            for user_id in temp:
                if not isinstance(temp[user_id], dict) or user_id in IGNORED_KEYS:
                    continue
                data = json_data[server_id][user_id]
                # If we get this far, this should be a user id, maybe add check?
                temp[user_id] = DiscordPlayer(**data)
        return cls(json_data)

    def to_json(self):
        """
        {
          '<server_id>': {
              'admin_ids': [<role_id>, <role_id>, ...],
              'roles': {
                '<role_id>': (<lower_point>, <greater_point>),
                ...
              },
              '<user_id>':
                {
                  'score': <score>,
                  'name': <name>
                }
            }
        """
        temp = deepcopy(self.data)
        for server_id in temp:
            current_server = temp[
                server_id
            ]  # {'admin_ids': [<role_id>, <role_id>, ...], 'roles': {...}, '<user_id>': {...}}
            # If we are not on a server object, just keep going
            if isinstance(current_server, Iterable) and not isinstance(current_server, str):
                for key in current_server:
                    current_user = current_server[key]
                    # Serialize
                    if not dc.is_dataclass(current_user):
                        continue
                    temp[server_id][key] = dc.asdict(current_user)
        return temp
