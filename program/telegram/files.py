import json
import os


class json_file:
    @staticmethod
    def read(path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def write(path, data):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True


class txt_file:
    @staticmethod
    def read(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            return [line.strip() for line in file if line.strip()]

    @staticmethod
    def write(path, data):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as file:
            if isinstance(data, (list, tuple, set)):
                file.write('\n'.join(map(str, data)))
            else:
                file.write(str(data))
        return True


def if_file_exist(path):
    return os.path.exists(path)


def get_account_json(path):
    return json_file.read(path)


def set_account_json(path, data):
    return json_file.write(path, data)


def get_session(path):
    base, _ = os.path.splitext(path)
    return base + '.session'


def rewrite_proxy_and_status(path, proxy=None, status=None):
    data = json_file.read(path) if os.path.exists(path) else {}
    if proxy is not None:
        data['proxy'] = proxy
    if status is not None:
        data['status'] = status
    return json_file.write(path, data)
