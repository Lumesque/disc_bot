# -*- coding: utf-8 -*-
"""

Keeps record of history and emojis with the add message
-> adds message to history, and add_user_react
-> add reaction to message from user

"""

from collections import defaultdict


class MessageHistory:
    def __init__(self, message_cap=20, **kwargs):
        self._messages = defaultdict(dict)
        self._reaction_from_users = defaultdict(dict)
        self._message_cap = message_cap

    def add(self, message):
        self._messages[message] = {}
        if len(self._messages) > self._message_cap:
            (k := next(iter(self._messages)), self._messages.pop(k))

    def is_message_stored(self, message) -> bool:
        if any(x for x in self._messages.keys() if x == message):
            return True
        return False

    def add_user_message(self, message, user, emoji):
        if not self._messages[message].get(emoji, None):
            self._messages[message][emoji] = []
        self._messages[message][emoji].append(user)

    def has_user_reacted(self, message, user, emoji) -> bool:
        if not self._messages[message].get(emoji, None):
            return False
        elif any(x for x in self._messages[message][emoji] if x == user):
            return True
        return False

    def has_message_expired(self, message) -> bool:
        if any(x for x in self._messages.keys() if x == message):
            return False
        return True

    def user_reactions(self, user, reaction):
        self._reaction_from_users[user] = reaction

    def list_message_senders(self):
        users = []
        for message in self._messages.keys():
            user = message.author.name
            if user not in users:
                users.append(user)
        return users

    def cleanup(self):
        self._messages = {}
        self._reaction_from_users = {}
