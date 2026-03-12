import sqlite3

class ChatMemory:

    def __init__(self):
        self.history = {}

    def save(self, user, message):
        if user not in self.history:
            self.history[user] = []

        self.history[user].append(message)

    def get_history(self, user, k=3):
        return self.history.get(user, [])[-k:]