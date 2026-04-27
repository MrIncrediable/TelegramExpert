import random
import sqlite3


class Header:
    def __init__(self):
        self.one = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        self.two = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.tree = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        self.fore = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        self.five = 'Chrome/126.0 Safari/537.36'

    def user_agent(self):
        return f'{random.choice([self.one, self.two, self.tree])} {self.fore} {self.five}'

    def get(self):
        return {'User-Agent': self.user_agent()}

    def urlget(self):
        return [('User-Agent', self.user_agent())]

    def __del__(self):
        return None


class AccsRole:
    def __init__(self, path='settings/roles.db'):
        self.path = path

    def get(self, role=None):
        return role

    def getAll(self):
        return []


class AccountsRoles:
    def __init__(self, path='settings/roles.db'):
        self.path = path
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.path, timeout=5, check_same_thread=False)
        self.cursor = self.connection.cursor()
        return self.cursor

    def close(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()
        self.connection = None
        self.cursor = None

    def get(self, role=None):
        return [] if role is None else [role]
