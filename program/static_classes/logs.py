import datetime
import logging as _logging
import os
import sys
import traceback
from collections import deque
from threading import Lock

LOG_SHOW = False
LOG_FILE = True
_log_lock = Lock()
_log_buffer = deque(maxlen=1000)
_error_buffer = deque(maxlen=1000)

_logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=_logging.INFO,
)


def _ensure_log_dir() -> None:
    os.makedirs('logs', exist_ok=True)


class logging:
    def __init__(self, exception=None):
        self._exception = exception
        self._log = str(exception) if exception is not None else ''
        self._print = LOG_SHOW
        self._file = LOG_FILE
        self._write()

    def _write(self):
        if self._exception is None:
            return None
        add_to_errors(self._exception)
        if self._print:
            print(self._log)
        if self._file:
            _ensure_log_dir()
            with _log_lock, open('logs/errors.log', 'a', encoding='utf-8') as file:
                file.write(f'{datetime.datetime.now().isoformat()} {self._log}\n')
                if isinstance(self._exception, BaseException):
                    file.write(''.join(traceback.format_exception(self._exception)))
        return None

    def __call__(self):
        return self


class Logs:
    @staticmethod
    def PrintLog(message='', param=None):
        text = message if param is None else f'{message}: {param}'
        add_to_log(text)
        if LOG_SHOW:
            print(text)
        return text

    @staticmethod
    def PrintLogDone(message='', param=None):
        text = message if param is None else f'{message}: {param}'
        add_to_log(text)
        if LOG_SHOW:
            print(text)
        return text

    @staticmethod
    def LangCheck(lang, key, default=''):
        if isinstance(lang, dict):
            return lang.get(key, default)
        return default

    @staticmethod
    def UpdateLogInWindow(*args, **kwargs):
        return None

    @staticmethod
    def WaitStopAnsfer(*args, **kwargs):
        return None


class SensitiveData:
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return proxy_hide(self.value)

    def __repr__(self):
        return str(self)


def add_to_log(message):
    _log_buffer.append(str(message))
    return True


def add_to_errors(error):
    _error_buffer.append(str(error))
    return True


def proxy_hide(value):
    if value is None:
        return None
    text = str(value)
    if len(text) <= 8:
        return '*' * len(text)
    return f'{text[:4]}***{text[-4:]}'


def get_logger(name=__name__):
    return _logging.getLogger(name)
