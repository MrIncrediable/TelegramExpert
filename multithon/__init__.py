try:
    from .client.telegramclient import TelegramClient
except Exception:
    TelegramClient = None

try:
    from .tl.custom import Button
except Exception:
    Button = None

try:
    from . import events, utils, errors, types, functions, custom
except Exception:
    events = utils = errors = types = functions = custom = None

__version__ = '1.40.0'
__all__ = ['TelegramClient', 'Button', 'types', 'functions', 'custom', 'errors', 'events', 'utils']
