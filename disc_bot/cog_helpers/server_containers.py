from typing import ClassVar
from collections import UserDict
from .player import DiscordPlayer
from ..config.globals import _G
from dataclasses import dataclass as dc
import warnings

class ServerContainer(UserDict):

    def get_player(self, server_id, user_id):
        return self.get_server(server_id).get(user_id, None)

    def get_server(self, server_id):
        server = self.data.get(server_id, None)
        if server is None:
            if _G.AUTOCREATE:
                server = self.add_server(server_id)
                warnings.warn(
                        "Server does not exist, creating new server. If you would like to not see this message, please disable auto-creation, or add server and save"
                        )
            else:
                raise KeyError(f"Server {server_id} does not exist")
        return server

    def add_server(self, server_id):
        self.data[server_id] = {}
        return self.data[server_id]

    def add_player(self, server_id, user_id):
        server = self.get_server(server_id)
        server[user_id] = (player := DiscordPlayer(user_id, server_id))
        return player

    def remove_server(self, server_id):
        self.data.pop(server_id, None)

    @classmethod
    def from_history(cls, json_data):
        for server_id in json_data:
            for user_id in json_data[server_id]:
                data = json_data[server_id][user_id]
                json_data[server_id][user_id] = DiscordPlayer(**data)
        return cls(json_data)

    def to_json(self):
        temp = self.data.copy()
        for server_id in temp:
            for user_id in temp[server_id]:
                data = temp[server_id][user_id]
                temp[server_id][user_id] = dc.as_dict(data)
        return temp

