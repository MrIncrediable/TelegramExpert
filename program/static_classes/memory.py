import base64
import datetime
import os
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

from .fingerprint import get_fingerprint, get_lic_key

_DATA_DIR = 'temp'
_MODULE_FILE = os.path.join(_DATA_DIR, '001.dat')
_LANG_FILE = os.path.join(_DATA_DIR, '002.dat')
_SWITCHER_FILE = os.path.join(_DATA_DIR, 'switcher.dat')
_PID_FILE = os.path.join(_DATA_DIR, 'pid.dat')
_SSL_FILE = os.path.join(_DATA_DIR, 'ssl.dat')

_MODULES = {
    1: 'mod:registrator|',
    2: 'mod:duplicator|',
    3: 'mod:inviteadmin|',
    4: 'mod:interceptor|',
    5: 'mod:reporter|',
    6: 'mod:chatcloner|',
    7: 'mod:channelcloner|',
    8: 'mod:forwarder|',
    9: 'mod:booster|',
    10: 'mod:converter|',
    11: 'mod:gpt|',
    12: 'mod:privatereg|',
}


def _ensure_temp() -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)


class FileProtector:
    def __init__(self):
        self.iv = base64.b64decode('u1c0cnTGVCSG9evTP1DIjg==')
        fp = get_fingerprint() or 'telegram-expert'
        license_key = get_lic_key() or ''
        self.key = SHA256.new(f'{fp}{license_key}'.encode('utf-8')).digest()

    def _key(self):
        return self.key

    def encrypt(self, data):
        raw = str(data).encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(pad(raw, AES.block_size))).decode('ascii')

    def decrypt(self, data):
        if data in (None, ''):
            return ''
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(base64.b64decode(data)), AES.block_size).decode('utf-8')

    def __del__(self):
        self.key = b''


def memory_set_module(data):
    _ensure_temp()
    payload = ''.join(_MODULES[item] for item in data if item in _MODULES)
    with open(_MODULE_FILE, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(FileProtector().encrypt(payload))
    return None


def check_module(module):
    try:
        with open(_MODULE_FILE, 'r', encoding='utf-8', errors='ignore') as file:
            data = FileProtector().decrypt(file.read())
        return f'mod:{module}|' in data
    except Exception:
        return False


def memory_set_lang(key):
    _ensure_temp()
    value = str(key)
    if value in ('ru', 'en', 'cn'):
        lang = f'lang:{value}'
    elif value.startswith('EXPERT-EN'):
        lang = 'lang:en'
    elif value.startswith('EXPERT-CN'):
        lang = 'lang:cn'
    else:
        lang = 'lang:ru'
    with open(_LANG_FILE, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(FileProtector().encrypt(lang))
    return None


def memory_get_lang():
    try:
        with open(_LANG_FILE, 'r', encoding='utf-8', errors='ignore') as file:
            lang = FileProtector().decrypt(file.read())
        if 'lang:ru' in lang:
            return 'ru'
        if 'lang:en' in lang:
            return 'en'
        if 'lang:cn' in lang:
            return 'cn'
        return False
    except Exception:
        return False


def memory_set_switcher():
    _ensure_temp()
    with open(_SWITCHER_FILE, 'w', encoding='utf-8') as file:
        file.write(str(time.time()))
    return None


def memory_check_switcher(timeout=0):
    try:
        with open(_SWITCHER_FILE, 'r', encoding='utf-8') as file:
            value = float(file.read().strip())
        return timeout <= 0 or time.time() - value <= timeout
    except Exception:
        return False


def memory_set_pid(pid=None):
    _ensure_temp()
    pid = os.getpid() if pid is None else pid
    with open(_PID_FILE, 'a', encoding='utf-8') as file:
        file.write(f'{int(pid)}\n')
    return True


def memory_check_pid(pid):
    try:
        with open(_PID_FILE, 'r', encoding='utf-8') as file:
            return str(pid) in {line.strip() for line in file if line.strip()}
    except Exception:
        return False


def memory_remove_pid(pid):
    try:
        with open(_PID_FILE, 'r', encoding='utf-8') as file:
            rows = [line.strip() for line in file if line.strip() and line.strip() != str(pid)]
        _ensure_temp()
        with open(_PID_FILE, 'w', encoding='utf-8') as file:
            file.write('\n'.join(rows))
            if rows:
                file.write('\n')
        return True
    except Exception:
        return False


def memory_set_ssl(value):
    _ensure_temp()
    with open(_SSL_FILE, 'w', encoding='utf-8') as file:
        file.write('1' if value else '0')
    return None


def memory_get_ssl():
    try:
        with open(_SSL_FILE, 'r', encoding='utf-8') as file:
            return file.read().strip() == '1'
    except Exception:
        return False
