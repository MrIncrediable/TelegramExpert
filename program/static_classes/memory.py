import base64
import datetime
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

from .fingerprint import get_fingerprint, get_lic_key

_DATA_DIR = 'temp'
_MODULE_FILE = os.path.join(_DATA_DIR, '001.dat')
_LANG_FILE = os.path.join(_DATA_DIR, '002.dat')
_SWITCHER_FILE = os.path.join(_DATA_DIR, '003.dat')
_PID_FILE = os.path.join(_DATA_DIR, 'pid.dat')
_SSL_FILE = os.path.join(_DATA_DIR, '004.dat')

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
        self.key = self._key()

    def _key(self):
        license_key = get_lic_key()
        fingerprint = get_fingerprint()
        date = datetime.datetime.now().strftime('%Y-%m-%U')
        if not license_key:
            raise ValueError('key error')
        if not fingerprint:
            raise ValueError('finger error')
        key = SHA256.new()
        key.update(f'{date}_{license_key}_{fingerprint}'.encode('utf-8'))
        return key.digest()

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
    try:
        _ensure_temp()
        payload = ''.join(_MODULES[item] for item in data if item in _MODULES)
        with open(_MODULE_FILE, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(FileProtector().encrypt(payload))
        return True
    except Exception:
        return False


def check_module(module):
    try:
        with open(_MODULE_FILE, 'r', encoding='utf-8', errors='ignore') as file:
            data = FileProtector().decrypt(file.read())
        return f'mod:{module}|' in data
    except Exception:
        return False


def memory_set_lang(key):
    try:
        _ensure_temp()
        value = str(key)
        if value in ('ru', 'en', 'cn') or value.startswith('EXPERT-EN'):
            lang = 'lang:en'
        elif value.startswith('EXPERT-CN'):
            lang = 'lang:cn'
        else:
            lang = 'lang:ru'
        with open(_LANG_FILE, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(FileProtector().encrypt(lang))
        return True
    except Exception:
        return False


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
        return 'en'
    except Exception:
        return 'en'


def memory_set_switcher():
    try:
        _ensure_temp()
        license_key = get_lic_key()
        date = datetime.datetime.now().strftime('%Y-%m-%U')
        key = SHA256.new()
        key.update(f'{date}_{license_key}'.encode('utf-8'))
        with open(_SWITCHER_FILE, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(FileProtector().encrypt(key.hexdigest()))
        return True
    except Exception:
        return False


def memory_check_switcher(ids=0):
    try:
        license_key = get_lic_key()
        date = datetime.datetime.now().strftime('%Y-%m-%U')
        key = SHA256.new()
        key.update(f'{date}_{license_key}'.encode('utf-8'))
        with open(_SWITCHER_FILE, 'r', encoding='utf-8', errors='ignore') as file:
            data = FileProtector().decrypt(file.read())
        return key.hexdigest() in data
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
    try:
        _ensure_temp()
        payload = ''.join(f'{item}|' for item in value)
        with open(_SSL_FILE, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(FileProtector().encrypt(payload))
        return True
    except Exception:
        return False


def memory_get_ssl():
    try:
        with open(_SSL_FILE, 'r', encoding='utf-8', errors='ignore') as file:
            data = FileProtector().decrypt(file.read())
        return [item.strip() for item in data.split('|') if item.strip()]
    except Exception:
        return False
