import datetime
import random
import sqlite3
import string
import eel
from program.static_classes import GetGender, Logs, logging
from telegram.links import tg_links

class db_base:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def import_list(self, users: list) -> str:
        try:
            if len(users) == 0:
                return False
            self.create()
            self.connect()
            count = 0
            for item in users:
                item = tg_links().standart(item)
                self.cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?)', (None, item, 'Ready'))
                count += 1
            self.close()
            Logs.PrintLog(message='Add to base', param=count)
            return self.path
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS BASE (ACCOUNT INTEGER, USERNAME TEXT, STATUS TEXT)')
            self.close()
            return self.path
        except BaseException as e:
            logging(e)

    def get(self, account=None) -> str:
        try:
            self.connect()
            self.cursor.execute('SELECT * FROM BASE WHERE USERNAME IS NOT NULL and STATUS = ? order by RANDOM() LIMIT 1 ', ('Ready',))
            row = self.cursor.fetchone()
            if row is None:
                return 'NO_GROUP'
            self.cursor.execute('UPDATE BASE SET ACCOUNT = ?, STATUS = ? WHERE USERNAME = ?', (account, 'Taken', row))
            self.close()
            return row
        except BaseException as e:
            logging(e)

    def get_all(self) -> str:
        try:
            self.connect()
            self.cursor.execute('SELECT * FROM BASE WHERE USERNAME IS NOT NULL order by RANDOM()')
            rows = self.cursor.fetchall()
            self.close()
            return rows
        except BaseException as e:
            logging(e)

    def update(self, account: str=None, link: str=None, status: str=None) -> bool:
        try:
            self.connect()
            self.cursor.execute('UPDATE BASE SET ACCOUNT = ?, STATUS = ? WHERE USERNAME = ?', (account, status, link))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_parsing:
    def __init__(self, path: str) -> None:
        try:
            self._path = path
            self._connect = sqlite3.connect(self._path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self._cursor = self._connect.cursor()
            self._attempt = 5
        except:
            pass

    def create(self, users_unic_usernames=False, users_unic_phone=False, groups_unic_usernames=False) -> str:
        try:
            if groups_unic_usernames:
                self._cursor.execute('CREATE TABLE IF NOT EXISTS GROUPS (ID INTEGER, USERNAME TEXT, TITLE TEXT, COUNT INTEGER, PHOTO INTEGER, INVITE INTEGER, SEND_MESSAGES INTEGER, SEND_MEDIA INTEGER, SEND_STICKERS INTEGER, SEND_POLLS INTEGER, SLOW_MODE INTEGER, SCAM INTEGER, TYPE TEXT, STATUS TEXT, UNIQUE(USERNAME))')
            else:
                self._cursor.execute('CREATE TABLE IF NOT EXISTS GROUPS (ID INTEGER, USERNAME TEXT, TITLE TEXT, COUNT INTEGER, PHOTO INTEGER, INVITE INTEGER, SEND_MESSAGES INTEGER, SEND_MEDIA INTEGER, SEND_STICKERS INTEGER, SEND_POLLS INTEGER, SLOW_MODE INTEGER, SCAM INTEGER, TYPE TEXT, STATUS TEXT, UNIQUE(ID))')
            
            if users_unic_usernames:
                self._cursor.execute('CREATE TABLE IF NOT EXISTS USERS (USER_ID INTEGER, GROUP_ID INTEGER, MESSAGE_ID INTEGER, COMMENT_ID INTEGER, PHONE TEXT, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, BIO TEXT, GENDER TEXT, PHOTO INTEGER, PREMIUM INTEGER, STATUS TEXT, TIME TEXT, INVITE_STATUS TEXT, SEND_STATUS TEXT, UNIQUE(USERNAME))')
            elif users_unic_phone:
                self._cursor.execute('CREATE TABLE IF NOT EXISTS USERS (USER_ID INTEGER, GROUP_ID INTEGER, MESSAGE_ID INTEGER, COMMENT_ID INTEGER, PHONE TEXT, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, BIO TEXT, GENDER TEXT, PHOTO INTEGER, PREMIUM INTEGER, STATUS TEXT, TIME TEXT, INVITE_STATUS TEXT, SEND_STATUS TEXT, UNIQUE(PHONE))')
            else:
                self._cursor.execute('CREATE TABLE IF NOT EXISTS USERS (USER_ID INTEGER, GROUP_ID INTEGER, MESSAGE_ID INTEGER, COMMENT_ID INTEGER, PHONE TEXT, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, BIO TEXT, GENDER TEXT, PHOTO INTEGER, PREMIUM INTEGER, STATUS TEXT, TIME TEXT, INVITE_STATUS TEXT, SEND_STATUS TEXT, UNIQUE(USER_ID))')
            self._connect.commit()
            return self._path
        except:
            pass

    def insert_group(self, group_id: int=0, username: str=None, title: str='', count: int=0, photo: int=0, invite: int=0, send_messages: int=0, send_media: int=0, send_stickers: int=0, send_pools: int=0, slow_mode: int=0, scam: int=0, types: str='', status: str='Ready') -> None:
        try:
            self._cursor.execute('INSERT OR IGNORE INTO GROUPS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (group_id, username, title, count, photo, invite, send_messages, send_media, send_stickers, send_pools, slow_mode, scam, types, status))
            self._connect.commit()
        except:
            pass

    def insert_user(self, user_id: int=None, group_id: int=None, mess_id: int=None, comm_id: int=None, phone: str=None, username: str=None, first_name: str=None, last_name: str=None, bio: str=None, gender: str=None, photo: str=None, premium: str=None, status: str=None, time: str=None, invite_status: str='Ready', send_status: str='Ready') -> None:
        try:
            self._cursor.execute('INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, group_id, mess_id, comm_id, phone, username, first_name, last_name, bio, gender, photo, premium, status, time, invite_status, send_status))
            self._connect.commit()
        except:
            pass

    def get_user_with_username(self, mode: str='invite') -> str:
        try:
            if mode == 'invite':
                self._cursor.execute("SELECT * FROM USERS WHERE USERNAME NOT NULL AND INVITE_STATUS = 'Ready' order by RANDOM() LIMIT 1")
            else:
                self._cursor.execute("SELECT * FROM USERS WHERE USERNAME NOT NULL AND SEND_STATUS = 'Ready' order by RANDOM() LIMIT 1")
            row = self._cursor.fetchone()
            if row is None:
                return False
            return row
        except:
            pass

    def get_users_with_phone(self, qty: int=1, mode: str='invite'):
        try:
            if mode == 'invite':
                self._cursor.execute("SELECT * FROM USERS WHERE PHONE NOT NULL AND INVITE_STATUS = 'Ready' order by RANDOM() LIMIT ?", (qty,))
            else:
                self._cursor.execute("SELECT * FROM USERS WHERE PHONE NOT NULL AND SEND_STATUS = 'Ready' order by RANDOM() LIMIT ?", (qty,))
            rows = self._cursor.fetchall()
            for row in rows:
                if mode == 'invite':
                    self._cursor.execute('UPDATE USERS SET INVITE_STATUS = ? WHERE PHONE = ?', ('Taken', row))
                else:
                    self._cursor.execute('UPDATE USERS SET SEND_STATUS = ? WHERE PHONE = ?', ('Taken', row))
                self._connect.commit()
            if rows is None:
                return None
            return rows
        except:
            pass

    def update_user_status(self, user_id=None, username=None, phone=None, mode='invite', status='Ready'):
        try:
            if user_id is not None:
                if mode == 'invite':
                    self._cursor.execute('UPDATE USERS SET INVITE_STATUS = ? WHERE USER_ID = ?', (status, user_id))
                else:
                    self._cursor.execute('UPDATE USERS SET SEND_STATUS = ? WHERE USER_ID = ?', (status, user_id))
            if username is not None:
                if mode == 'invite':
                    self._cursor.execute('UPDATE USERS SET INVITE_STATUS = ? WHERE USERNAME = ? OR USERNAME = ?', (status, f'https://t.me/{username}', username))
                else:
                    self._cursor.execute('UPDATE USERS SET SEND_STATUS = ? WHERE USERNAME = ? OR USERNAME = ?', (status, f'https://t.me/{username}', username))
            if phone is not None:
                if mode == 'invite':
                    self._cursor.execute('UPDATE USERS SET INVITE_STATUS = ? WHERE PHONE = ?', (status, phone))
                else:
                    self._cursor.execute('UPDATE USERS SET SEND_STATUS = ? WHERE PHONE = ?', (status, phone))
            self._connect.commit()
        except:
            pass

    def update_group(self, group_id: int=None, username: str=None, title: str=None, count: int=None, photo: int=None, invite: int=None, send_messages: int=None, send_media: int=None, send_stickers: int=None, send_pools: int=None, slow_mode: int=None, scam: int=None, types: str=None, status: str='Ready', mode: str='id') -> None:
        try:
            params = ()
            query = 'UPDATE GROUPS SET'
            if username is None:
                return None
            if group_id is not None:
                query += ' ID = ?,'
                params += (group_id,)
            if username is not None:
                query += ' USERNAME = ?,'
                params += (username,)
            if title is not None:
                query += ' TITLE = ?,'
                params += (title,)
            if count is not None:
                query += ' COUNT = ?,'
                params += (count,)
            if photo is not None:
                query += ' PHOTO = ?,'
                params += (photo,)
            if invite is not None:
                query += ' INVITE = ?,'
                params += (invite,)
            if send_messages is not None:
                query += ' SEND_MESSAGES = ?,'
                params += (send_messages,)
            if send_media is not None:
                query += ' SEND_MEDIA = ?,'
                params += (send_media,)
            if send_stickers is not None:
                query += ' SEND_STICKERS = ?,'
                params += (send_stickers,)
            if send_pools is not None:
                query += ' SEND_POLLS = ?,'
                params += (send_pools,)
            if slow_mode is not None:
                query += ' SLOW_MODE = ?,'
                params += (slow_mode,)
            if scam is not None:
                query += ' SCAM = ?,'
                params += (scam,)
            if types is not None:
                query += ' TYPE = ?,'
                params += (types,)
            if status is not None:
                query += ' STATUS = ?,'
                params += (status,)
            query = query
            if mode == 'id':
                if group_id is not None:
                    query += ' WHERE GROUP_ID = ?'
                    params += (group_id,)
                else:
                    query += ' WHERE USERNAME = ?'
                    params += (username,)
            elif mode == 'username':
                query += ' WHERE USERNAME = ?'
                params += (username,)
            self._cursor.execute(query, params)
            self._connect.commit()
        except:
            pass

    def update_user(self, user_id: int=None, group_id: int=None, mess_id: int=None, comm_id: int=None, phone: str=None, username: str=None, first_name: str=None, last_name: str=None, bio: str=None, gender: str=None, photo: str=None, premium: str=None, status: str=None, time: str=None, invite_status: str=None, send_status: str=None, mode: str='id') -> None:
        try:
            params = ()
            query = 'UPDATE USERS SET'
            if user_id is not None:
                query += ' USER_ID = ?,'
                params += (user_id,)
            if group_id is not None:
                query += ' GROUP_ID = ?,'
                params += (group_id,)
            if mess_id is not None:
                query += ' MESSAGE_ID = ?,'
                params += (mess_id,)
            if comm_id is not None:
                query += ' COMMENT_ID = ?,'
                params += (comm_id,)
            if phone is not None:
                query += ' PHONE = ?,'
                params += (phone,)
            if username is not None:
                query += ' USERNAME = ?,'
                params += (username,)
            if first_name is not None:
                query += ' FIRST_NAME = ?,'
                params += (first_name,)
            if last_name is not None:
                query += ' LAST_NAME = ?,'
                params += (last_name,)
            if bio is not None:
                query += ' BIO = ?,'
                params += (bio,)
            if gender is not None:
                query += ' GENDER = ?,'
                params += (gender,)
            if photo is not None:
                query += ' PHOTO = ?,'
                params += (photo,)
            if premium is not None:
                query += ' PREMIUM = ?,'
                params += (premium,)
            if status is not None:
                query += ' STATUS = ?,'
                params += (status,)
            if time is not None:
                query += ' TIME = ?,'
                params += (time,)
            if invite_status is not None:
                query += ' INVITE_STATUS = ?,'
                params += (invite_status,)
            if send_status is not None:
                query += ' SEND_STATUS = ?,'
                params += (send_status,)
            query = query
            if mode == 'id':
                if user_id is not None:
                    query += ' WHERE USER_ID = ?'
                    params += (user_id,)
                else:
                    query += ' WHERE USERNAME = ? OR USERNAME = ?'
                    params += (username, f'https://t.me/{username}')
            elif mode == 'username':
                query += ' WHERE USERNAME = ? OR USERNAME = ?'
                params += (username, f'https://t.me/{username}')
            elif mode == 'phone':
                query += ' WHERE PHONE = ?'
                params += (phone,)
            self._cursor.execute(query, params)
            self._connect.commit()
        except:
            pass

    def get_users_groups(self, qty: int, mode: str='invite', attempt: int=0):
        try:
            if attempt >= self._attempt:
                return False
            self._cursor.execute('SELECT * FROM GROUPS order by RANDOM() LIMIT 1')
            group = self._cursor.fetchone()
            if group is None or len(group) == 0:
                return False
            if mode == 'invite':
                self._cursor.execute('SELECT * FROM USERS WHERE GROUP_ID = ? and INVITE_STATUS = ? order by RANDOM() LIMIT ?', (group, 'Ready', qty))
            else:
                self._cursor.execute('SELECT * FROM USERS WHERE GROUP_ID = ? and SEND_STATUS = ? order by RANDOM() LIMIT ?', (group, 'Ready', qty))
            users = self._cursor.fetchall()
            if len(users) == 0:
                return self.get_users_groups(qty=qty, mode=mode, attempt=attempt + 1)
            for user in users:
                if mode == 'invite':
                    self._cursor.execute('UPDATE USERS SET INVITE_STATUS = ? WHERE USER_ID = ?', ('Taken', user))
                else:
                    self._cursor.execute('UPDATE USERS SET SEND_STATUS = ? WHERE USER_ID = ?', ('Taken', user))
            self._connect.commit()
            return
        except:
            pass

    def get_group(self, mode: str='id'):
        try:
            self._cursor.execute('SELECT * FROM GROUPS WHERE STATUS = ? order by RANDOM() LIMIT 1', ('Ready',))
            group = self._cursor.fetchone()
            if group is None or len(group) == 0:
                return False
            if mode == 'id':
                if group is not None:
                    self.update_group(username=group, status='Taken', mode='id')
                else:
                    self.update_group(username=group, status='Taken', mode='username')
            return group
        except:
            pass

    def import_groups(self, groups: list) -> str:
        try:
            if groups is None or len(groups) == 0:
                return False
            self.create(groups_unic_usernames=True)
            for group in groups:
                group = tg_links().standart(group)
                self._cursor.execute('INSERT OR IGNORE INTO GROUPS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (None, group, None, None, None, None, None, None, None, None, None, None, None, 'Ready'))
            self._connect.commit()
            return self._path
        except:
            pass

    def import_users(self, users: list) -> str:
        try:
            if users is None or len(users) == 0:
                return False
            self.create(users_unic_usernames=True)
            for user in users:
                user = tg_links().get_hash(user)
                self._cursor.execute('INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (None, None, None, None, None, user, None, None, None, None, None, None, None, None, 'Ready', 'Ready'))
            self._connect.commit()
            return self._path
        except:
            pass

    def import_phones(self, phones: list) -> str:
        try:
            if phones is None or len(phones) == 0:
                return False
            self.create(users_unic_phone=True)
            for phone in phones:
                phone = tg_links().phones(phone)
                self._cursor.execute('INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (None, None, None, None, phone, None, None, None, None, None, None, None, None, None, 'Ready', 'Ready'))
            self._connect.commit()
            return self._path
        except:
            pass

    def get_users(self):
        try:
            self._cursor.execute('SELECT * FROM USERS')
            users = self._cursor.fetchall()
            return users
        except:
            pass

    def get_users_count(self):
        try:
            self._cursor.execute('SELECT count(*) FROM USERS')
            count = self._cursor.fetchone()
            return count
        except:
            pass

    def union(self, file_name: str=None):
        try:
            Logs.PrintLog(message='Union database is started', param=file_name)
            conn = sqlite3.connect(file_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM GROUPS')
            groups = cursor.fetchall()
            cursor.execute('SELECT * FROM USERS')
            users = cursor.fetchall()
            conn.commit()
            conn.close()
            group_count = 0
            user_count = 0
            for group in groups:
                self.insert_group(group_id=group, username=group, title=group, count=group, photo=group, invite=group, send_messages=group, send_media=group, send_stickers=group, send_pools=group, slow_mode=group, scam=group, types=group, status=group)
                group_count += 1
            for user in users:
                self.insert_user(user_id=user, group_id=user, mess_id=user, comm_id=user, phone=user, username=user, first_name=user, last_name=user, bio=user, gender=user, photo=user, premium=user, status=user, time=user, invite_status=user, send_status=user)
                user_count += 1
            return {'groups': group_count, 'users': user_count}
        except:
            pass

    def create_txt(self, txt_path: str) -> str:
        try:
            Logs.PrintLog(message='Add data to *.txt file', param=txt_path)
            count = 0
            users = self.get_users()
            with open(txt_path, 'a') as f:
                for user in users:
                    if user != None and user != 'None':
                        f.write(f'{user}\n')
                        count += 1
            return count
        except:
            pass

    def check_gender(self):
        try:
            Logs.PrintLog(message='Check gender is started')
            male = 0
            female = 0
            un = 0
            count = 0
            users = self.get_users()
            for user in users:
                gender = GetGender(user)
                if gender == 'M':
                    male += 1
                elif gender == 'F':
                    female += 1
                else:
                    un += 1
                count += 1
                self._cursor.execute('UPDATE USERS SET GENDER = ? WHERE USER_ID = ?', (gender, user))
            self._connect.commit()
            return {'count': count, 'male': male, 'female': female, 'un': un}
        except:
            pass

class db_parsing_res:
    @staticmethod
    def connect(path: str) -> str:
        try:
            conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            return conn
        except:
            pass

    @staticmethod
    def create(_connect, unic_usernames=False) -> str:
        try:
            cursor = _connect.cursor()
            if unic_usernames:
                cursor.execute('CREATE TABLE IF NOT EXISTS GROUPS (ID INTEGER, USERNAME TEXT, TITLE TEXT, COUNT INTEGER, PHOTO INTEGER, INVITE INTEGER, SEND_MESSAGES INTEGER, SEND_MEDIA INTEGER, SEND_STICKERS INTEGER, SEND_POLLS INTEGER, SLOW_MODE INTEGER, SCAM INTEGER, TYPE TEXT, STATUS TEXT, UNIQUE(ID))')
                cursor.execute('CREATE TABLE IF NOT EXISTS USERS (USER_ID INTEGER, GROUP_ID INTEGER, MESSAGE_ID INTEGER, COMMENT_ID INTEGER, PHONE TEXT, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, BIO TEXT, GENDER TEXT, PHOTO INTEGER, PREMIUM INTEGER, STATUS TEXT, TIME TEXT, INVITE_STATUS TEXT, SEND_STATUS TEXT, UNIQUE(USERNAME))')
            else:
                cursor.execute('CREATE TABLE IF NOT EXISTS GROUPS (ID INTEGER, USERNAME TEXT, TITLE TEXT, COUNT INTEGER, PHOTO INTEGER, INVITE INTEGER, SEND_MESSAGES INTEGER, SEND_MEDIA INTEGER, SEND_STICKERS INTEGER, SEND_POLLS INTEGER, SLOW_MODE INTEGER, SCAM INTEGER, TYPE TEXT, STATUS TEXT, UNIQUE(ID))')
                cursor.execute('CREATE TABLE IF NOT EXISTS USERS (USER_ID INTEGER, GROUP_ID INTEGER, MESSAGE_ID INTEGER, COMMENT_ID INTEGER, PHONE TEXT, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, BIO TEXT, GENDER TEXT, PHOTO INTEGER, PREMIUM INTEGER, STATUS TEXT, TIME TEXT, INVITE_STATUS TEXT, SEND_STATUS TEXT, UNIQUE(USER_ID))')
            _connect.commit()
        except:
            pass

    @staticmethod
    def insert_group(_connect, group_id: int=0, username: str=None, title: str='', count: int=0, photo: int=0, invite: int=0, send_messages: int=0, send_media: int=0, send_stickers: int=0, send_pools: int=0, slow_mode: int=0, scam: int=0, types: str='', status: str='Ready') -> None:
        try:
            cursor = _connect.cursor()
            cursor.execute('INSERT OR IGNORE INTO GROUPS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (group_id, username, title, count, photo, invite, send_messages, send_media, send_stickers, send_pools, slow_mode, scam, types, status))
            _connect.commit()
        except:
            pass

    @staticmethod
    def insert_user(_connect, user_id: int=None, group_id: int=None, mess_id: int=None, comm_id: int=None, phone: str=None, username: str=None, first_name: str=None, last_name: str=None, bio: str=None, gender: str=None, photo: str=None, premium: str=None, status: str=None, time: str=None, invite_status: str='Ready', send_status: str='Ready') -> None:
        try:
            cursor = _connect.cursor()
            cursor.execute('INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, group_id, mess_id, comm_id, phone, username, first_name, last_name, bio, gender, photo, premium, status, time, invite_status, send_status))
            _connect.commit()
        except:
            pass

    @staticmethod
    def disconnect(_connect):
        try:
            _connect.commit()
            _connect.close()
        except:
            pass

class db_statistic:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (TIME TEXT, ACCOUNT INTEGER, GROUP_ID INTEGER, GROUP_LINK TEXT, USER_ID INTEGER, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, INVITE_STATUS TEXT, SEND_STATUS TEXT, MESSAGE TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, group_id: int=None, group_link: str=None, user_id: str=None, username: str=None, first_name: str=None, last_name: str=None, invite_status: str='Ready', send_status: str='Ready', message: str=None) -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                time_str = datetime.now().strftime('%y-%m-%d %H:%M:%S')
                cursor.execute('INSERT OR REPLACE INTO STATISTIC VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (time_str, account, group_id, group_link, user_id, username, first_name, last_name, invite_status, send_status, message))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_reg_statistic:
    def __init__(self, path: str=None) -> None:
        try:
            self.time = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            if path is not None:
                self.path = path
            else:
                self.path = f'additives/registrator/{self.time}_stat.db'
            self.filename = f'{self.time}_stat.db'
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, STATUS TEXT)')
                eel.WriteResult('Statistics', 'registrator', self.filename)
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: str, status: str) -> bool:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO STATISTIC VALUES (?, ?)', (account, status))
                conn.commit()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.time
            del self.path
            del self.filename
        except:
            pass

class db_param_accounts:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
            self.repeat = 5
        except:
            pass

    def select(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM REGISTRATOR order by RANDOM() LIMIT 1')
                row = cursor.fetchone()
                data = {}
                data = int(row)
                data = str(row)
                data = str(row)
                data = str(row)
                data = str(row)
                data = str(row)
                data = str(row)
                data = str(row)
                data = int(row)
                data = int(row)
                data = None
                data = None
                data = None
                data = None
                data = None
                data = None
                return data
        except BaseException as e:
            logging(e)
            self.repeat -= 1
            if self.repeat <= 0:
                raise ValueError('Check database')
            return self.select()

    def select_all(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM REGISTRATOR')
                rows = cursor.fetchall()
                if len(rows) < 1:
                    raise ValueError('Check Database')
        except BaseException as e:
            pass

    def __del__(self):
        try:
            del self.path
            del self.repeat
        except:
            pass

class db_create_channels:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS BASE (TIME TEXT, ACCOUNT INTEGER, ID INTEGER, NAME TEXT, LINK TEXT, MESSAGE TEXT, STATUS TEXT)')
            self.close()
            return self.path
        except BaseException as e:
            logging(e)

    def set_data(self, account: str=None, group_id: int=None, group_name: str=None, group_link: str=None, message: str=None, status: str='Done'):
        try:
            time_str = datetime.now().strftime('%y-%m-%d %H:%M:%S')
            self.connect()
            self.cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?, ?, ?)', (time_str, account, group_id, group_name, group_link, message, status))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_reactions:
    def __init__(self, path: str=None) -> None:
        try:
            self.time = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            if path is not None:
                self.path = path
            else:
                self.path = f'additives/reactions/{self.time}_result.db'
            self.filename = f'{self.time}_result.db'
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS BASE (TIME TEXT, ACCOUNT INTEGER, LINK TEXT, REACTION TEXT, STATUS TEXT)')
            self.close()
            eel.WriteResult('Result', 'reactions', self.filename)
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: str=None, link: str=None, reaction: str=None, status: str='Done'):
        try:
            time_str = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            self.connect()
            self.cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?)', (time_str, account, link, reaction, status))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_search_groups:
    def __init__(self, path: str=None) -> None:
        try:
            self.time = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            if path is not None:
                self.path = path
            else:
                self.path = f'additives/search_groups/{self.time}_result.db'
            self.filename = f'{self.time}_result.db'
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS BASE (ACCOUNT INTEGER, ID INTEGER, USERNAME TEXT, TITLE TEXT, COUNT INTEGER, NEW_OWNER TEXT, STATUS TEXT)')
            self.close()
            eel.WriteResult('Result', 'search_groups', self.filename)
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: str=None, uid: str=None, link: str=None, title: str=None, count: int=0, new_owner: str=None, status: str='Done'):
        try:
            self.connect()
            self.cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?, ?, ?)', (account, uid, link, title, count, new_owner, status))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_reporter:
    def __init__(self, path: str=None) -> None:
        try:
            self.time = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            if path is not None:
                self.path = path
            else:
                self.path = f'additives/reporter/{self.time}_result.db'
            self.filename = f'{self.time}_result.db'
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS BASE (ACCOUNT INTEGER, TARGET TEXT, REASON TEXT, MESSAGE TEXT, STATUS TEXT)')
            self.close()
            eel.WriteResult('Result', 'reporter', self.filename)
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: str=None, target: str=None, reason: str=None, message: str=None, status: str='Done'):
        try:
            self.connect()
            self.cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?)', (account, target, reason, message, status))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_proxy:
    def __init__(self, path: str='settings/proxy.db') -> None:
        try:
            self.path = path
        except:
            pass

    def create(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS PROXY (ID INTEGER, HOST TEXT, PORT TEXT, LOGIN TEXT, PASSWORD TEXT, TYPE TEXT, VERSION TEXT, RESPONSE TEXT, STATUS INTEGER)')
                conn.commit()
        except BaseException as e:
            logging(e)

    def recalculate(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM PROXY')
                proxies = cursor.fetchall()
                cursor.execute('DELETE FROM PROXY')
                count = 0
                for proxy in proxies:
                    count += 1
                    cursor.execute('INSERT OR REPLACE INTO PROXY VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (count, proxy, proxy, proxy, proxy, proxy, proxy, proxy, proxy))
                conn.commit()
        except BaseException as e:
            logging(e)

    def calculate(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM PROXY')
                proxies = cursor.fetchall()
                return len(proxies)
        except BaseException as e:
            logging(e)
            return 0

    def delete(self, proxy_id):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM PROXY WHERE ID = ?', (proxy_id,))
                conn.commit()
            self.recalculate()
        except BaseException as e:
            logging(e)

    def delete_all(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM PROXY')
                conn.commit()
        except BaseException as e:
            logging(e)

    def delete_bad(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM PROXY WHERE STATUS = ?', ('bad',))
                conn.commit()
            self.recalculate()
        except BaseException as e:
            logging(e)

    def add(self, data):
        try:
            self.create()
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                proxy_type = data
                proxy_ver = data
                proxy_add = data
                for proxy in proxy_add:
                    if proxy != '':
                        proxy_parts = proxy.replace(' ', '').split(':')
                        proxy_len = len(proxy_parts)
                        if proxy_len == 2:
                            proxy_parts.append(None)
                            proxy_parts.append(None)
                        cursor.execute('INSERT OR REPLACE INTO PROXY VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (None, proxy_parts, proxy_parts, proxy_parts, proxy_parts, proxy_type, proxy_ver, None, None))
                conn.commit()
            self.recalculate()
        except BaseException as e:
            logging(e)

    def get(self):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM PROXY')
                proxy = cursor.fetchall()
                if proxy !=[]:
                    return proxy
                return False
        except BaseException as e:
            logging(e)

    def get_id(self, proxy_id):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM PROXY WHERE ID = ?', (proxy_id,))
                proxy = cursor.fetchone()
                if len(proxy) > 0:
                    return proxy
                return False
        except BaseException as e:
            logging(e)

    def update(self, proxy_id, responce, status=None):
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE PROXY SET RESPONSE = ?, STATUS = ? WHERE ID LIKE ?', (responce, status, proxy_id))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_subscribe:
    def __init__(self, path: str=None) -> None:
        try:
            self.time = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            if path is not None:
                self.path = path
            else:
                self.path = f'additives/subscribe/{self.time}_stat.db'
            self.filename = f'{self.time}_stat.db'
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, LINK TEXT, STATUS TEXT)')
            self.close()
            eel.WriteResult('Statistic', 'subscribe', self.filename)
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: str=None, link: str=None, status: str='Done'):
        try:
            self.connect()
            self.cursor.execute('INSERT INTO STATISTIC VALUES (?, ?, ?)', (account, link, status))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_subscribe_bot:
    def __init__(self, path: str=None) -> None:
        try:
            self.time = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            if path is not None:
                self.path = path
            else:
                self.path = f'additives/subscribe_bot/{self.time}_stat.db'
            self.filename = f'{self.time}_stat.db'
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, LINK TEXT, STATUS TEXT)')
            self.close()
            eel.WriteResult('Statistic', 'subscribe_bot', self.filename)
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: str=None, link: str=None, status: str='Done'):
        try:
            self.connect()
            self.cursor.execute('INSERT INTO STATISTIC VALUES (?, ?, ?)', (account, link, status))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_coordinates:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
            self.connection = None
            self.cursor = None
        except:
            pass

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            logging(e)

    def import_list(self, coordinates: list) -> str:
        try:
            if len(coordinates) == 0:
                return False
            self.create()
            self.connect()
            count = 0
            for row in coordinates:
                row = row.replace('lat: ', '').strip()
                row = row.replace('lng: ', '').strip()
                row = row.replace('radius: ', '').strip()
                self.cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?)', (float(row), float(row), int(row), 'Ready'))
                count += 1
            self.close()
            Logs.PrintLog('Add to base', message=None, param=count)
            return self.path
        except BaseException as e:
            logging(e)

    def create(self) -> str:
        try:
            self.connect()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS BASE (LAT TEXT, LONG TEXT, RADIUS INTEGER, STATUS TEXT)')
            self.close()
            return self.path
        except BaseException as e:
            logging(e)

    def get(self) -> str:
        try:
            self.connect()
            self.cursor.execute('SELECT * FROM BASE WHERE STATUS = ? order by RANDOM() LIMIT 1 ', ('Ready',))
            row = self.cursor.fetchone()
            if row is None:
                return False
            self.cursor.execute('UPDATE BASE SET STATUS = ? WHERE LAT = ? AND LONG = ? AND RADIUS = ?', ('Taken', row, row, row))
            self.close()
            return row
        except BaseException as e:
            logging(e)

    def update(self, lat: str=None, long: str=None, radius: str=None, status: int=None) -> bool:
        try:
            self.connect()
            self.cursor.execute('UPDATE BASE SET STATUS = ? WHERE LAT = ? AND LONG = ? AND RADIUS = ?', (status, lat, long, radius))
            self.close()
        except BaseException as e:
            logging(e)

    def reset_status(self) -> bool:
        try:
            self.connect()
            self.cursor.execute('UPDATE BASE SET STATUS = ? WHERE STATUS != ?', ('Ready', 'Ready'))
            self.close()
        except BaseException as e:
            logging(e)

    def close(self):
        try:
            self.connection.commit()
            self.connection.close()
        except BaseException as e:
            logging(e)

    def __del__(self):
        try:
            del self.path
            del self.connection
            del self.cursor
        except:
            pass

class db_contacts:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (USER_ID INTEGER, NUMBER INTEGER, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def get(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM BASE WHERE STATUS = ? order by RANDOM() LIMIT 1', ('Ready',))
                row = cursor.fetchone()
                if row is None:
                    return False
                if row is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE USER_ID = ?', ('Taken', row))
                elif row is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE NUMBER = ?', ('Taken', row))
                elif row is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE USERNAME = ?', ('Taken', row))
                conn.commit()
                return {'id': row, 'number': row, 'username': row, 'first_name': row, 'last_name': row}
        except BaseException as e:
            logging(e)

    def get_all(self, limit: int=0) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM BASE LIMIT ?', (limit,))
                rows = cursor.fetchall()
                users =[]
                for row in rows:
                    users.append({'id': row, 'number': row, 'username': row, 'first_name': row, 'last_name': row})
                if len(users) == 0:
                    return None
                return users
        except BaseException as e:
            logging(e)

    def update(self, user_id: int=None, number: int=None, username: str=None, status: str='Done') -> bool:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                if user_id is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE USER_ID = ?', (status, user_id))
                    return True
                if number is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE NUMBER = ?', (status, number))
                    return True
                if username is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE USERNAME = ?', (status, username))
                    return True
                conn.commit()
        except BaseException as e:
            logging(e)

    def insert(self, user_id: int=None, number: int=None, username: str=None, first_name: str=None, last_name: str=None, status: str='Ready') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                if number is not None:
                    number = int(number)
                cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?, ?)', (user_id, number, username, first_name, last_name, status))
                conn.commit()
        except BaseException as e:
            logging(e)

    def import_list(self, users: list) -> None:
        try:
            if len(users) == 0:
                return False
            self.create()
            users = list(dict.fromkeys(users))
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                count = 0
                for item in users:
                    row = item.replace(' ', '').split('|')
                    if len(row) == 1:
                        first_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=random.randint(4, 24)))
                        last_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=random.randint(4, 24)))
                    elif len(row) == 2:
                        first_name = row
                        last_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=random.randint(4, 24)))
                    elif len(row) == 3:
                        first_name = row
                        last_name = row
                    contact = tg_links().contacts_phone_or_username(row)
                    cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?, ?)', (None, contact, contact, first_name, last_name, 'Ready'))
                    count += 1
                conn.commit()
            Logs.PrintLog('Add to base', message=None, param=count)
            return self.path
        except BaseException as e:
            logging(e)

class db_contacts_statistic:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, USER_ID INTEGER, NUMBER INTEGER, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, user_id: int=None, number: int=None, username: str=None, first_name: str=None, last_name: str=None, status: str='Ready') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO STATISTIC VALUES (?, ?, ?, ?, ?, ?, ?)', (account, user_id, number, username, first_name, last_name, status))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_contacts_export:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (USER_ID INTEGER, NUMBER INTEGER, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, STATUS TEXT, UNIQUE(USER_ID))')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, number: int=None, user_id: int=None, username: str=None, first_name: str=None, last_name: str=None, status: str='Ready') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                if number is not None:
                    number = int(number)
                cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?, ?)', (user_id, number, username, first_name, last_name, status))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_search_global:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (WORD TEXT, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def get(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM BASE WHERE STATUS = ? order by RANDOM() LIMIT 1', ('Ready',))
                row = cursor.fetchone()
                if row is None:
                    return None
                if row is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE WORD = ?', ('Taken', row))
                conn.commit()
                return row
        except BaseException as e:
            logging(e)

    def get_all(self, limit: int=0) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM BASE LIMIT ?', (limit,))
                rows = cursor.fetchall()
                results =[]
                for row in rows:
                    results.append(row)
                if len(results) == 0:
                    return None
                return results
        except BaseException as e:
            logging(e)

    def update(self, word: str=None, status: str='Done') -> bool:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                if word is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE WORD = ?', (status, word))
                    conn.commit()
                    return True
                return None
        except BaseException as e:
            logging(e)

    def import_list(self, words: list) -> None:
        try:
            if len(words) == 0:
                return False
            self.create()
            words = list(dict.fromkeys(words))
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                count = 0
                for word in words:
                    word = word.strip()
                    cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?)', (word, 'Ready'))
                    count += 1
                conn.commit()
            Logs.PrintLog('Add to base', message=None, param=count)
            return self.path
        except BaseException as e:
            logging(e)

class db_check_links_no_accounts:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (USERNAME TEXT, TITLE TEXT, COUNT TEXT, BIO TEXT, TYPE TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, username: str=None, title: str=None, count: str=None, bio: str=None, type: str=None) -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?)', (username, title, count, bio, type))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_export_offline:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (ACCOUNT INTEGER, ID INTEGER, PHONE INTEGER, USEERNAME TEXT, NAME TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

class db_create_bots:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (ACCOUNT INTEGER, TOKEN TEXT, USERNAME TEXT, NAME TEXT, BIO TEXT, PHOTO TEXT, DESCRIPTION TEXT, RESTRICT_GROUPS INTEGER, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, token: str=None, username: str=None, name: str=None, bio: str=None, photo: str=None, description: str=None, restrict_groups: int=None, status: str='Done') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (int(account), token, username, name, bio, photo, description, int(restrict_groups), status))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_edit_message:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, USER_ID INTEGER, TITLE TEXT, USERNAME TEXT, TYPE TEXT, MESSAGE TEXT, MESSAGE_EDIT TEXT, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, user_id: int=None, title: str=None, username: str=None, type: str=None, message: str=None, message_edit: str=None, status: str='Done') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO STATISTIC VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (account, user_id, title, username, type, message, message_edit, status))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_create_postbot:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (ACCOUNT INTEGER, POST TEXT, DESCRIPTION TEXT, FILE TEXT, BUTTONS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, post: str=None, description: str=None, file: str=None, buttons: str=None) -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?, ?, ?, ?)', (int(account), post, description, file, buttons))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_stories_public:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def get(self, unic: str=True) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                if unic:
                    cursor.execute('SELECT * FROM BASE WHERE STATUS = ? order by RANDOM() LIMIT 1', ('Ready',))
                else:
                    cursor.execute('SELECT * FROM BASE order by RANDOM() LIMIT 1')
                row = cursor.fetchone()
                if row is None:
                    return None
                if unic:
                    if row is not None:
                        cursor.execute('UPDATE BASE SET STATUS = ? WHERE FILE = ?', ('Taken', row))
                        conn.commit()
                return row
        except BaseException as e:
            logging(e)

    def put(self, files: list) -> str:
        try:
            if len(files) == 0:
                return False
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (FILE TEXT, STATUS TEXT)')
                for file in files:
                    file = file.replace(' ', '')
                    cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?)', (file, 'Ready'))
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

class db_stories_public_statistic:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, LINK TEXT, FILE TEXT, DESCRIPTION TEXT, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, link: str=None, file: str=None, description: str=None, status: str='Done') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO STATISTIC VALUES (?, ?, ?, ?, ?)', (account, link, file, description, status))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_stories_public_users:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def get(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM USERS WHERE STATUS = ? order by RANDOM() LIMIT 1', ('Ready',))
                row = cursor.fetchone()
                if row is None:
                    return None
                cursor.execute('UPDATE USERS SET STATUS = ? WHERE USERNAME = ?', ('Taken', row))
                conn.commit()
                return row
        except BaseException as e:
            logging(e)

    def put(self, users: list) -> str:
        try:
            if len(users) == 0:
                return False
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS USERS (USERNAME TEXT, STATUS TEXT)')
                for user in users:
                    user = tg_links().clear_username(user)
                    cursor.execute('INSERT OR REPLACE INTO USERS VALUES (?, ?)', (user, 'Ready'))
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def update(self, username: str=None, status: str='Done') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE USERS SET STATUS = ? WHERE USERNAME = ?', (status, username))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_stories_del_statistic:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def create(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STATISTIC (ACCOUNT INTEGER, STORIES_ID INTEGER, STATUS TEXT)')
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def insert(self, account: int=None, stories_id: int=None, status: str='Done') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR REPLACE INTO STATISTIC VALUES (?, ?, ?)', (account, stories_id, status))
                conn.commit()
        except BaseException as e:
            logging(e)

class db_stories_send:
    def __init__(self, path: str) -> None:
        try:
            self.path = path
        except:
            pass

    def put(self, links: list) -> str:
        try:
            if len(links) == 0:
                return False
            links = list(dict.fromkeys(links))
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS BASE (LINK TEXT, STATUS TEXT)')
                for link in links:
                    link = link.replace(' ', '')
                    cursor.execute('INSERT OR REPLACE INTO BASE VALUES (?, ?)', (link, 'Ready'))
                conn.commit()
            return self.path
        except BaseException as e:
            logging(e)

    def get(self) -> str:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM BASE WHERE STATUS = ? order by RANDOM() LIMIT 1', ('Ready',))
                row = cursor.fetchone()
                if row is None:
                    return None
                if row is not None:
                    cursor.execute('UPDATE BASE SET STATUS = ? WHERE LINK = ?', ('Taken', row))
                conn.commit()
                return row
        except BaseException as e:
            logging(e)

    def update(self, link: str=None, status: str='Done') -> None:
        try:
            with sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES, timeout=5, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE BASE SET STATUS = ? WHERE LINK = ?', (status, link))
                conn.commit()
        except BaseException as e:
            logging(e)