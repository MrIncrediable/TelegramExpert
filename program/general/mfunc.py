#decoded by lolz.live/mrpenny / t.me/zeus_jackpot
import os
import sys
import eel
import json
import time
import psutil
import ctypes
import locale
import random
import string
import urllib
import base64
import hashlib
import sqlite3
import zipfile
import datetime
import requests
import concurrent.futures as concurrent
from tkinter import Tk
from tqdm import tqdm
from pathlib import Path
from threading import Lock, Thread
from mimesis import Person
from mimesis.enums import Gender
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests.adapters import HTTPAdapter, Retry
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
from program.database import db_proxy
from multithon.errors import StopProgram
from program.telegram import json_file, set_account_json
from program.static_classes import (
    AccsRole, GeneratorName, Header, Logs, VersionControl, 
    get_fingerprint, get_lic_key, logging, memory_get_lang, 
    memory_get_ssl, memory_remove_pid, memory_set_lang, 
    memory_set_module, memory_set_ssl, memory_set_switcher, set_lic_key
)

PROGRAM_VERSION = 'prod'

def GetConfig():
    CreateConfig()
    try:
        config = json_file.read('settings/config.json')
        if config.get('gpt', None) is None or config.get('control_offical', None) is None or config.get('control_unoffical', None) is None or config.get('control_name', None) is None or config.get('control_tweb', None) is None or config.get('tweb_proxy', None) is None:
            os.remove('settings/config.json')
            CreateConfig()
            config = json_file.read('settings/config.json')
        config['lang'] = memory_get_lang()
        config['ssl'] = memory_get_ssl()
        config['license'] = get_lic_key()
        return config
    except:
        return False

def CreateConfig():
    try:
        if not os.path.exists('settings/config.json'):
            config = {}
            config['timeout'] = 15
            config['settings'] = {}
            config['proxy'] = 'settings'
            config['proxy_change'] = True
            config['proxy_change_count'] = 3
            config['browser'] = False
            config['log'] = 'w'
            config['thread_count'] = 100
            config['thread_wait_from'] = 0
            config['thread_wait_to'] = 0
            config['antibot'] = True
            config['antibot_wait'] = 5
            config['flood_wait'] = 80
            config['peer_flood'] = 1
            config['entry_wait'] = 300
            config['theme'] = 'dark'
            config['color'] = '#00ffd0'
            config['port'] = 777
            config['control_offical'] = True
            config['control_unoffical'] = True
            config['control_name'] = True
            config['control_tweb'] = True
            config['tweb_proxy'] = True
            config['gpt'] = False
            
            with open('settings/config.json', 'w') as f:
                json.dump(config, f, indent=2)
            return True
        return True
    except:
        return None

def config_set(option, value, path='settings/config.json'):
    try:
        if not os.path.exists(path):
            CreateConfig()
        config = json_file.read(path)
        config[option] = value
        json_file.write(path, config)
        return True
    except Exception as e:
        logging(e)
        return False

def GetProxy():
    try:
        return None
    except:
        pass

def StopDetect(stop_thread=None):
    try:
        Logs.PrintLogDone(message='Work is done')
        eel.HideStopButton()
        stop_thread.set()
        return None
    except:
        pass

def check_get_settings(settings):
    try:
        for key in settings:
            if settings[key] == '' and key != 'file_db':
                eel.sendErrorBox('Check settings')
                StopProgram()
        return None
    except:
        pass

def random_account_param(rows):
    try:
        row = random.choice(rows)
        param = {}
        param['app_id'] = int(row[0])
        param['app_hash'] = str(row[1])
        param['sdk'] = str(row[2])
        param['device'] = str(row[3])
        param['app_version'] = str(row[4])
        param['lang_code'] = str(row[5])
        param['system_lang_code'] = str(row[6])
        param['lang_pack'] = str(row[7])
        param['tz_offset'] = int(row[8])
        param['perf_cat'] = int(row[9])
        param['device_token'] = None
        param['device_token_secret'] = None
        param['device_secret'] = None
        param['signature'] = None
        param['certificate'] = None
        param['safetynet'] = None
        return param
    except:
        pass

def GetUserNames(data):
    try:
        def get_string(filename):
            try:
                if filename is None or filename == '':
                    return ''
                with open(filename, 'r', errors='ignore', encoding='utf-8') as f:
                    content = random.choice(f.read().strip().split('\n'))
                return content
            except:
                pass
                
        reg_set_names = data['Settings'].get('reg_set_names', False)
        if reg_set_names:
            reg_path_first = data['Settings'].get('reg_path_first', False)
            reg_path_last = data['Settings'].get('reg_path_last', False)
            reg_sex = data['Settings'].get('reg_sex', 'rand')
            if reg_sex == 'rand':
                reg_sex = random.choice([1, 2])
            elif reg_sex == 'm':
                reg_sex = 1
            else:
                reg_sex = 2
            first_name = get_string(reg_path_first)
            last_name = get_string(reg_path_last)
            return first_name, last_name, reg_sex
        else:
            names = GeneratorName()
            first_name, last_name, reg_sex = names.get()
            return first_name, last_name, reg_sex
    except:
        pass

def GetUserNamesManual(country='en', sex='random', file_firstname='', file_lastname=''):
    try:
        def get_string(filename):
            try:
                if filename is None or filename == '':
                    return ''
                with open(filename, 'r', errors='ignore', encoding='utf-8') as f:
                    content = random.choice(f.read().strip().split('\n'))
                return content
            except:
                pass

        if country == None or country == 'none':
            country = 'en'
        if sex == None or sex == 'none':
            sex = 'random'
            
        if country == 'own':
            first_name = get_string(file_firstname)
            last_name = get_string(file_lastname)
            if sex == 'random' or sex == 'rand':
                sex = random.choice([0, 1])
        else:
            person = Person(country, Newdatafolder=os.getcwd() + '\\additives\\data\\identity')
            if sex == 'random' or sex == 'rand':
                sex = random.choice(['male', 'female'])
            if sex == 'female' or sex == 'f':
                gender = Gender.FEMALE
            else:
                gender = Gender.MALE
            first_name = person.name(gender=gender)
            last_name = person.last_name(gender=gender)
            if gender == Gender.MALE:
                sex = 1
            else:
                sex = 2
                
        return first_name, last_name, sex
    except:
        pass

def reg_get_2fa(data=None):
    try:
        reg_set_2fa_mode = data['Settings'].get('reg_set_2fa_mode', 'random')
        if reg_set_2fa_mode == 'manual':
            reg_set_2fa_pass = data['Settings'].get('reg_set_2fa_pass', '').strip()
            if reg_set_2fa_pass == '':
                reg_set_2fa_mode = 'random'
        if reg_set_2fa_mode == 'random':
            reg_set_2fa_pass = ''.join((random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(random.randint(6, 14))))
        return reg_set_2fa_pass
    except:
        pass

def get_account_time(timespan: int = None):
    try:
        def table_translate_type(current, val):
            try:
                type_map = {
                    'days': ['день', 'дня', 'дней'],
                    'weeks': ['недели', 'недель'],
                    'months': ['месяца', 'месяцев', 'месяц'],
                    'hours': ['часа', 'час', 'часов'],
                    'minutes': ['минута', 'минут', 'минуты'],
                    'seconds': ['секунда', 'секунды', 'секунд'],
                    'years': ['год', 'года', 'лет']
                }
                
                if current == 'день':
                    if 2 <= val < 5:
                        current = 'дня'
                    elif val >= 5:
                        current = 'дней'
                elif current == 'недель':
                    if 2 <= val < 5:
                        current = 'недели'
                    elif val >= 5:
                        current = 'недель'
                elif current == 'месяц':
                    if 2 <= val < 5:
                        current = 'месяца'
                    elif val >= 5:
                        current = 'месяцев'
                elif current == 'год':
                    if 2 <= val < 5:
                        current = 'года'
                    elif val >= 5:
                        current = 'лет'
                elif current == 'час':
                    if 2 <= val < 5:
                        current = 'часа'
                    elif val >= 5:
                        current = 'часов'
                elif current == 'минута':
                    if 2 <= val < 5:
                        current = 'минуты'
                    elif val >= 5:
                        current = 'минут'
                elif current == 'секунда':
                    if 2 <= val < 5:
                        current = 'секунды'
                    elif val >= 5:
                        current = 'секунд'
                        
                for k, v_list in type_map.items():
                    if current in v_list:
                        current = k
                return current
            except:
                pass

        if timespan is None:
            timespan = time.time()
        timespan = int(timespan)
        dt = datetime.datetime.fromtimestamp(timespan)
        diff = datetime.datetime.now() - dt
        
        res = {'value': 0, 'type': '0', 'AccVal': 'N'}
        if diff.days == 0:
            if diff.seconds < 60:
                val = round(diff.seconds)
                res = {'value': val, 'type': table_translate_type('секунда', val), 'AccVal': 'N'}
            elif 60 <= diff.seconds < 3600:
                val = round(diff.seconds / 60)
                res = {'value': val, 'type': table_translate_type('минута', val), 'AccVal': 'N'}
            elif 3600 <= diff.seconds < 86400:
                val = round(diff.seconds / 3600)
                res = {'value': val, 'type': table_translate_type('час', val), 'AccVal': 'N'}
        else:
            if 1 <= diff.days < 7:
                val = round(diff.days)
                res = {'value': val, 'type': table_translate_type('день', val), 'AccVal': 'D'}
            elif 7 <= diff.days <= 31:
                val = round(diff.days / 7)
                res = {'value': val, 'type': table_translate_type('недель', val), 'AccVal': 'W'}
            elif 31 < diff.days <= 365:
                val = round(diff.days / 31)
                res = {'value': val, 'type': table_translate_type('месяц', val), 'AccVal': 'W'}
            elif diff.days > 365:
                val = round(diff.days / 365)
                res = {'value': val, 'type': table_translate_type('год', val), 'AccVal': 'W'}
        return res
    except:
        pass

def get_panel_accounts(accounts, path='sessions/active', config=None):
    try:
        def get_accounts_table(account):
            try:
                avatar = ''
                is_avatar = 0
                avatar_path = str(account.get('avatar')).replace('./static/', '')
                phone = str(account.get('phone'))
                app_version = str(account.get('app_version'))
                
                if int(account.get('app_id')) == 2040 and config['control_tweb'] == False:
                    avatar += f'<i class="bi bi-laptop" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="Go to WEB version" onclick="openAccount(\'{phone}\')" style="z-index:1000"></i></a>'
                else:
                    avatar += '<i class="bi bi-laptop-x" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="The account does not work on Telegram Desktop settings. Logging in to the web version is not available."></i>'
                
                is_avatar += 1
                
                if not VersionControl(config=config, log=False).check(app_id=account['app_id'], version=account['app_version']):
                    avatar += '<i class="bi bi-version-warning" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="Warning! Check app_version in json! Version control is ON"></i>'
                    is_avatar += 1
                    
                sex = account.get('sex')
                is_avatar += 1
                
                if sex == 'male' or sex == 'm' or sex == '1' or sex == 1:
                    avatar += '<i class="bi bi-gender-male" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="male"></i>'
                elif sex == 'female' or sex == 'f' or sex == '2' or sex == 2:
                    avatar += '<i class="bi bi-gender-female" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="female"></i>'
                else:
                    avatar += '<i class="bi bi-gender-trans" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="transgender, or gender not set in json =) "></i>'
                
                if avatar_path != 'null' and avatar_path != 'img/default.png':
                    avatar += '<i class="bi bi-camera" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="photo is set"></i>'
                    is_avatar += 1
                    
                if avatar_path == 'null' or avatar_path == 'none':
                    avatar_path = 'img/default.png'
                    
                if os.path.exists(f'additives/web/{avatar_path}'):
                    avatar_path = 'img/default.png'
                    
                if account.get('twoFA', '') != '':
                    avatar += '<i class="bi bi-key" style="padding-left:10px;" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="' + str(account.get('twoFA')) + '"></i>'
                    is_avatar += 1
                    
                proxy = account.get('proxy', [])
                if proxy != None and len(proxy) > 2:
                    proxy = f"{proxy[1]}:{proxy[2]}"
                else:
                    proxy = '0.0.0.0:0'
                    
                reg_time = get_account_time(account.get('register_time'))
                reg_time = f"{reg_time['value']} {reg_time['type']}"
                
                username = account.get('username', '')
                if username != None and username.strip() == '':
                    username = ''
                if username == None or username.strip() == 'null':
                    username = ''
                    
                status = account.get('status', '-')
                if status is None:
                    status = '<span class="panel_free">-</span>'
                elif 'free' in status.lower():
                    status = '<span class="panel_free">' + status + '</span>'
                elif 'ban' in status.lower():
                    status = '<span class="panel_ban">' + status + '</span>'
                elif 'spamblock' in status.lower():
                    status = '<span class="panel_spamblock">' + status + '</span>'
                elif 'tempspamblock' in status.lower():
                    status = '<span class="panel_tempspamblock">' + status + '</span>'
                    
                work = account.get('work', 0)
                if work is None:
                    work = 0
                if work == 1:
                    progress = "<div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated' role='progressbar' aria-valuenow='50' aria-valuemin='0' aria-valuemax='100' style='width: 100%'>working...</div></div><div class='text-status-progress'>one account = one task!</div>"
                else:
                    progress = "<div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated bg-success' role='progressbar' aria-valuenow='0' aria-valuemin='0' aria-valuemax='100' style='width: 0%'>0%</div></div><div class='text-status-progress'></div>"
                    
                res = {
                    'lastproxy': proxy,
                    'twofa': account.get('twoFA'),
                    'add': avatar,
                    'img': avatar_path,
                    'username': username,
                    'name': '{} {}'.format(str(account.get('first_name')), str(account.get('last_name'))).replace('None', ''),
                    'phone': phone,
                    'alive': reg_time,
                    'version': app_version,
                    'progress': progress,
                    'module': account.get('module'),
                    'time': account.get('time'),
                    'status': status
                }
                
                if username == '':
                    res['usernameVal'] = '0'
                else:
                    res['usernameVal'] = '1'
                    
                res['addOpt'] = is_avatar
                return res
            except:
                reg_time = '-'
                return None

        def get_account(account, path, roles):
            try:
                path = Path(path)
                is_avatar = 0
                avatar = ''
                is_roles = 0
                acc_data = json_file.read('{}\\{}\\{}'.format(os.getcwd(), path, account))
                if acc_data == False:
                    return None
                
                table_data = get_accounts_table(acc_data)
                
                for role in roles:
                    if role[0] == table_data['phone']:
                        avatar += '<span class="badge badge-pill badge-light roles">' + f"{role[1]}" + '</span>'
                        is_roles += 1
                        
                if 'default' in table_data['img']:
                    is_img = 0
                else:
                    is_img = 1
                is_avatar += 1
                
                res = {
                    '#': {'val': is_avatar, 'img': '<img data-order="' + str(is_img) + '" src=' + table_data['img'] + ' alt="" height="30px" width="30px" style="border-radius: 100%;">'},
                    'username': {'val': table_data['username'], 'sort': table_data['usernameVal']},
                    'name': {'val': table_data['name'], 'sort': table_data['name']},
                    'phone': {'val': table_data['phone'], 'sort': table_data['phone']},
                    'alive': {'val': table_data['alive'], 'sort': str(acc_data.get('register_time'))},
                    'version': {'val': table_data['version'], 'sort': table_data['version']},
                    'roles': {'val': avatar, 'sort': is_roles},
                    'addopt': {'val': table_data['add'], 'sort': table_data['addOpt']},
                    'module': {'val': table_data['module'], 'sort': table_data['module']},
                    'time': {'val': table_data['time'], 'sort': table_data['time']},
                    'lastproxy': {'val': table_data['lastproxy'], 'sort': table_data['lastproxy']},
                    'status': {'val': table_data['status'], 'sort': table_data['status']},
                    'progress': {'val': table_data['progress'], 'sort': table_data['progress']}
                }
                return res
            except:
                return None

        roles = AccsRole().getAll()
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = []
            res_list = []
            count = 0
            for acc in accounts:
                futures.append(executor.submit(get_account, acc, path, roles))
                
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res is not None:
                    count += 1
                    res['#']['val'] = count
                    res_list.append(res)
                    if len(res_list) >= 500:
                        eel.UploadFullAccountByOne(res_list)
                        res_list = []
                        
        if len(res_list) != 0:
            eel.UploadFullAccountByOne(res_list)
            
        return None
    except:
        pass

def getFile(data):
    try:
        file = GetFileDB()
        if file is None:
            file = ''
        else:
            file = file[0]
        eel.LoadFilePathes(data['filename'], file)
        return None
    except:
        pass

def getPath(data):
    try:
        path = GetFolderPath()
        if path is None:
            path = ''
        eel.LoadFilePathes(data['filename'], path)
        return None
    except:
        pass

def GetFileDB():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file = askopenfilenames(parent=root, initialdir='/', title='Chose DB File', multiple=False, filetypes=(('DB File', '*.db'), ('All Files', '*.*')))
        root.update()
        if file == '':
            return None
        return list(file)
    except:
        pass

def GetFileTXT():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file = askopenfilenames(parent=root, initialdir='/', title='Chose TXT File', multiple=False, filetypes=(('TXT File', '*.txt'), ('All Files', '*.*')))
        root.update()
        if file == '':
            return None
        return list(file)
    except:
        pass

def GetFolderPath():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        folder = askdirectory(title='Chose folder path')
        root.update()
        if folder == '':
            return None
        return list(folder)
    except:
        pass

def getFileAdd():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file = askopenfilenames(parent=root, initialdir='/', title='Select file', multiple=False, filetypes=(('image files', '*.png *.jpg'), ('video files', '*.mp4'), ('sound files', '.ogg *.mp3'), ('All files', '*.*')))
        root.update()
        if file == []:
            return None
        return file
    except:
        pass

def getListsUsers(par='txt'):
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file = askopenfilename(initialdir='/', title='Select file', multiple=True, filetypes=(('image files', '*.png *.jpg'), ('video files', '*.mp4'), ('sound files', '.ogg *.mp3'), ('All files', '*.*')))
        if file == '':
            return None
        return '\n'.join(file)
    except:
        pass

def task_manager(data):
    try:
        if data['action'] == 'get_task_manager':
            res = get_task_manager()
            return res
        return False
    except:
        pass

def SendStop(pid):
    try:
        pid = str(pid)
        with Lock():
            try:
                memory_remove_pid(pid)
            except BaseException as e:
                logging(e)
            try:
                del_task_manager(pid)
            except BaseException as e:
                logging(e)
            try:
                eel.HideStopButton()
            except BaseException:
                pass
        return True
    except:
        pass

def set_task_manager(pid, accounts, name, status):
    try:
        if type(accounts) != list:
            accounts = [accounts]
        pid = int(pid)
        conn = sqlite3.connect('temp/task_manager.db', detect_types=sqlite3.PARSE_DECLTYPES | 5, timeout=5, check_same_thread=False)
        cur = conn.cursor()
        dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        cur.execute('CREATE TABLE IF NOT EXISTS TASKS (PID INTEGER, START TEXT, MODULE TEXT, ACCOUNTS INTEGER, STATUS TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS ACCOUNTS (PID INTEGER, NUMBER TEXT, STATUS TEXT)')
        cur.execute('INSERT OR REPLACE INTO TASKS VALUES (?, ?, ?, ?, ?)', (int(pid), dt, name, len(accounts), status))
        for acc in accounts:
            cur.execute('INSERT OR REPLACE INTO ACCOUNTS VALUES (?, ?, ?)', (int(pid), acc, 0))
            set_account_json('sessions/active/' + f'{acc}' + '.json', work=1)
        conn.commit()
        conn.close()
        eel.task_manager_update_ui()
        return True
    except Exception as e:
        print('set_task_manager:' + str(e))
        return False

def get_task_manager(pid=0):
    try:
        pid = int(pid)
        conn = sqlite3.connect('temp/task_manager.db', detect_types=sqlite3.PARSE_DECLTYPES | 5, timeout=5, check_same_thread=False)
        cur = conn.cursor()
        if pid == 0:
            cur.execute('SELECT * FROM TASKS')
        else:
            cur.execute('SELECT * FROM TASKS WHERE PID = ?', (pid,))
        res = cur.fetchall()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print('get_task_manager:' + str(e))
        return False

def del_task_manager(pid=0):
    try:
        conn = sqlite3.connect('temp/task_manager.db', detect_types=sqlite3.PARSE_DECLTYPES | 5, timeout=5, check_same_thread=False)
        cur = conn.cursor()
        if pid == 0:
            cur.execute('SELECT * FROM TASKS')
            tasks = cur.fetchall()
            for task in tasks:
                cur.execute('SELECT FROM ACCOUNTS WHERE PID = ?', (task[0],))
                accs = cur.fetchall()
                for acc in accs:
                    set_account_json('sessions/active/' + f'{acc[1]}' + '.json', work=0)
            cur.execute('DELETE FROM TASKS')
            cur.execute('DELETE FROM ACCOUNTS')
        else:
            cur.execute('SELECT * FROM ACCOUNTS WHERE PID = ?', (pid,))
            accs = cur.fetchall()
            for acc in accs:
                set_account_json('sessions/active/' + f'{acc[1]}' + '.json', work=0)
            cur.execute('DELETE FROM TASKS WHERE PID = ?', (int(pid),))
            cur.execute('DELETE FROM ACCOUNTS WHERE PID = ?', (int(pid),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('del_task_manager:' + str(e))
        return False

def clear_task_manager():
    try:
        conn = sqlite3.connect('temp/task_manager.db', detect_types=sqlite3.PARSE_DECLTYPES | 5, timeout=5, check_same_thread=False)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS TASKS (PID INTEGER, START TEXT, MODULE TEXT, ACCOUNTS INTEGER, STATUS TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS ACCOUNTS (PID INTEGER, NUMBER TEXT, STATUS TEXT)')
        cur.execute('DELETE FROM TASKS')
        cur.execute('DELETE FROM ACCOUNTS')
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('clear_task_manager:' + str(e))
        return False

class ProxyChecker:
    def __init__(self, timeout=None):
        try:
            self.timeout = timeout
            self.sites_ip = [
                'https://api64.ipify.org',
                'https://v4v6.ipv6-test.com/api/myip.php',
                'https://api.aruljohn.com/ip'
            ]
            self.headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a1) Gecko/20060814 Firefox/51.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43'
                ])
            }
            return None
        except:
            pass

    def get_ip(self, proxy):
        try:
            start_time = time.time()
            url = random.choice(self.sites_ip)
            resp = requests.get(url, proxies=proxy, headers=self.headers, timeout=self.timeout, verify=False)
            diff = time.time() - start_time
            content = resp.content
            if resp.status_code == 200:
                res = '%.3f' % diff
                return [res, 'ok']
            return False
        except:
            return False

    def check(self, proxy):
        try:
            host = proxy[0]
            port = proxy[1]
            user = proxy[2]
            pwd = proxy[3]
            protocol = proxy[4]
            status = proxy[5]
            proxy_type = proxy[6]
            
            if proxy_type == '' or proxy_type is None:
                return False
                
            proxy_type = proxy_type.lower()
            if proxy_type == 'http':
                if user is None:
                    proxy_url = f'http://{host}:{port}'
                else:
                    proxy_url = f'http://{user}:{pwd}@{host}:{port}'
            elif proxy_type == 'socks4':
                if user is None:
                    proxy_url = f'socks4h://{host}:{port}'
                else:
                    proxy_url = f'socks4h://{user}:{pwd}@{host}:{port}'
            elif proxy_type == 'socks5':
                if user is None:
                    proxy_url = f'socks5h://{host}:{port}'
                else:
                    proxy_url = f'socks5h://{user}:{pwd}@{host}:{port}'
            else:
                return False
                
            proxies = {'http': proxy_url, 'https': proxy_url}
            res = self.get_ip(proxy=proxies)
            if res == False:
                return False
            return res
        except:
            return False

def proxy_controller(data):
    try:
        db = db_proxy()
        if data['action'] == 'proxy_get_all':
            return db.get()
            
        if data['action'] == 'proxy_add':
            db.add(data['data'])
            return None
            
        if data['action'] == 'proxy_delete_one':
            db.delete(data['id'])
            return None
            
        if data['action'] == 'proxy_delete_bad':
            db.delete_bad()
            return None
            
        if data['action'] == 'proxy_delete_all':
            db.delete_all()
            return None
            
        config = GetConfig()
        if data['action'] == 'proxy_check_one':
            proxy = db.get_id(data['id'])
            if proxy != False:
                Thread(target=check_proxy_one, args=(proxy, config['timeout'])).start()
                
        if data['action'] == 'proxy_check_all':
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                futures = []
                proxies = db.get()
                if proxies:
                    db = db_proxy()
                    count = len(proxies)
                    streams = 1000
                    wait = count
                    done = 0
                    eel.StreamStat(json.dumps({'st_task': count, 'st_stream': streams, 'st_wait': wait, 'st_done': done}))
                    for proxy in proxies:
                        futures.append(executor.submit(check_proxy, proxy, config['timeout']))
                    for future in concurrent.futures.as_completed(futures):
                        done += 1
                        wait -= 1
                        eel.StreamStat(json.dumps({'st_task': count, 'st_stream': streams, 'st_wait': wait, 'st_done': done}))
                        res = future.result()
                        status = res.get('status')
                        if status:
                            db.update(res['id'], res['time'], res['text'])
                            eel.proxy_set_status(res['id'], res['time'], res['text'])
                        else:
                            db.update(res['id'])
                            eel.proxy_set_status(res['id'])
            return None
        return None
    except BaseException as e:
        logging(e)

def check_proxy(proxy, timeout):
    try:
        checker = ProxyChecker(timeout)
        res = checker.check(proxy)
        if res:
            return {'status': True, 'id': proxy[0], 'time': res[0], 'text': res[1]}
        return {'status': False, 'id': proxy[0]}
    except BaseException as e:
        logging(e)

def check_proxy_one(proxy, timeout):
    try:
        db = db_proxy()
        proxy_id = proxy[0]
        checker = ProxyChecker(timeout=timeout)
        res = checker.check(proxy=proxy)
        if res == False:
            db.update(proxy_id=proxy_id)
            eel.proxy_set_status(proxy_id)
            return False
        db.update(proxy_id, res[0], res[1])
        eel.proxy_set_status(proxy_id, res[0], res[1])
        return True
    except BaseException as e:
        logging(e)
        return False

def get_user_lang():
    try:
        windll = ctypes.windll.kernel32
        lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        lang = lang.lower()
        if 'ru' in lang:
            return 'ru'
        elif 'en' in lang:
            return 'en'
        elif 'zh' in lang:
            return 'cn'
        return 'en'
    except BaseException:
        return 'en'

def get_key_lang():
    try:
        key = get_lic_key()
        if key != False:
            if 'EXPERT-RU-' in key:
                return 'ru'
            elif 'EXPERT-EN-' in key:
                return 'en'
            elif 'EXPERT-CN-' in key:
                return 'cn'
        return 'en'
    except BaseException:
        return 'en'

def get_server_lic_url():
    try:
        lang = get_key_lang()
        if 'ru' in lang:
            return 'https://ru.telegramexpert.su/'
        elif 'en' in lang:
            return 'https://en.telegramexpert.su/'
        elif 'cn' in lang:
            return 'https://cn.telegramexpert.su/'
        return None
    except:
        pass

def get_server_file_url():
    try:
        if PROGRAM_VERSION == 'prod':
            lang = get_user_lang()
            if 'ru' in lang:
                return 'https://files-ru.telegramexpert.su/'
            elif 'en' in lang:
                return 'https://files-en.telegramexpert.su/'
            elif 'cn' in lang:
                return 'https://files-cn.telegramexpert.su/'
        elif PROGRAM_VERSION == 'demo':
            return 'https://files-demo.telegramexpert.su/'
        elif PROGRAM_VERSION == 'admin':
            return 'https://files-admin.telegramexpert.su/'
        return None
    except:
        pass

def requests_reconnect(link):
    try:
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.3, allowed_methods=False, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        try:
            with session.get(f'{link}', headers=Header().get(), timeout=(30, 60), verify=True) as resp:
                content = resp.content
                return content
        except:
            raise ConnectionError('404')
    except BaseException as e:
        logging(e)
        raise ConnectionError('404')

class Crypto:
    def __init__(self):
        try:
            self.iv = base64.b64decode('u1c0cnTGVCSG9evTP1DIjg==')
            self.key = base64.b64decode('nAAF43H4rKw898yiZF7qvYgouSccGAWxC66oxjPkssE=')
        except:
            pass

    def encrypt(self, data):
        try:
            data = data.encode('utf-8')
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            encrypted = cipher.encrypt(pad(data, AES.block_size))
            return base64.b64encode(encrypted).decode('utf-8')
        except BaseException as e:
            logging(e)
            return False

    def decrypt(self, data):
        try:
            data = base64.b64decode(data)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted = unpad(cipher.decrypt(data), AES.block_size)
            return decrypted.decode('utf-8')
        except BaseException as e:
            logging(e)
            return False

    def __del__(self):
        try:
            del self.iv
            del self.key
        except:
            pass

def upgs_nonce():
    try:
        crypto = Crypto()
        fingerprint = get_fingerprint()
        key = get_lic_key()
        if fingerprint and key:
            data = json.dumps({'action': 'check', 'key': key, 'token': fingerprint['token'], 'secret': fingerprint['hdd_serial']})
            encrypted_data = crypto.encrypt(data=data)
            resp = requests_reconnect(f"{get_server_lic_url()}lic.php?data={encrypted_data}")
            decrypted_resp = json.loads(crypto.decrypt(data=resp.text))
            
            status = decrypted_resp.get('status')
            data_resp = decrypted_resp.get('data')
            resp_key = decrypted_resp.get('key')
            ssl_val = decrypted_resp.get('ssl')
            
            if status == 'ok' and key == resp_key and data_resp != 'bad' and ssl_val:
                if type(data_resp) is list and type(ssl_val) is list:
                    if memory_set_module(data_resp):
                        raise ValueError('Error')
                    if memory_set_lang(key):
                        raise ValueError('Error')
                    if memory_set_switcher():
                        raise ValueError('Error')
                    if memory_set_ssl(ssl_val):
                        raise ValueError('Error')
                    return True
        return False
    except BaseException as e:
        logging(e)
        return False

def OnStart():
    try:
        def GetKey():
            try:
                crypto = Crypto()
                fingerprint = get_fingerprint()
                if fingerprint != False:
                    data = json.dumps({'action': 'key', 'token': fingerprint['token'], 'secret': fingerprint['hdd_serial']})
                    encrypted_data = crypto.encrypt(data=data)
                    resp = requests_reconnect(f"{get_server_lic_url()}lic.php?data={encrypted_data}")
                    decrypted_resp = json.loads(crypto.decrypt(data=resp.text))
                    
                    status = decrypted_resp.get('status')
                    if status == 'ok':
                        if decrypted_resp.get('data') == 'good':
                            return decrypted_resp.get('key')
                return False
            except BaseException as e:
                logging(e)
                return False

        def EnterKey():
            try:
                key = input(' - Please enter license key: ')
                if key == 'getkey':
                    key = GetKey()
                if key:
                    set_lic_key(key)
                else:
                    print(' - Key incorrect, please try again')
                    EnterKey()
            except:
                pass

        if not upgs_nonce():
            EnterKey()
            OnStart()
        return True
    except:
        pass

def Updater():
    try:
        def close_all_neccessary_process(processname):
            try:
                def close_one_file_process(pid):
                    try:
                        for p in psutil.process_iter(['pid', 'name', 'exe'], attrs=['attrs']):
                            exe = p.info['exe']
                            if exe is not None:
                                if f'onefile_{pid}_' in exe:
                                    p.kill()
                    except:
                        pass
                        
                cwd = os.getcwd().replace('/', '\\').replace('\\\\', '\\')
                for p in psutil.process_iter(attrs=['pid', 'name', 'exe']):
                    pid = p.info['pid']
                    name = p.info['name']
                    exe = p.info['exe']
                    if pid is not None and name is not None and exe is not None:
                        if cwd in exe and processname == name:
                            close_one_file_process(pid)
                            p.kill()
            except:
                pass

        def data_from_server(server_url):
            try:
                resp = requests_reconnect(f"{server_url}update.php?data=get_files")
                if resp.status_code != 200:
                    raise ConnectionError('404')
                return json.loads(resp.text)
            except:
                print(' - Error! Check internet connection')
                sys.exit(0)

        def get_file_hash(filename):
            try:
                if not os.path.exists(filename):
                    return 0
                with open(filename, 'rb') as f:
                    file_hash = hashlib.sha1(f.read()).hexdigest()
                return file_hash
            except:
                return None

        def delete_file(path):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass

        def unzip(file, output):
            try:
                with zipfile.ZipFile(file) as zf:
                    zf.extractall(path=output)
                return True
            except:
                raise ValueError('Error unzip file')

        def download_file(server_url, file, indicator):
            try:
                class DownloadProgressBar(tqdm):
                    def update_to(self, b=1, bsize=1, tsize=None):
                        try:
                            if tsize is not None:
                                self.total = tsize
                            self.update(b * bsize - self.n)
                        except:
                            pass

                crypto = Crypto()
                enc_name = crypto.encrypt(file['server_name'])
                delete_file(file['path'])
                url = f"{server_url}update.php?data=get_file&file={enc_name}"
                
                opener = urllib.request.build_opener()
                opener.addheaders = Header().urlget()
                urllib.request.install_opener(opener)
                
                if indicator:
                    with DownloadProgressBar(unit='B', ncols=78, unit_scale=True, miniters=1, desc=' - Download') as t:
                        urllib.request.urlretrieve(url, filename=file['path'], reporthook=t.update_to)
                else:
                    urllib.request.urlretrieve(url, filename=file['path'])
            except:
                pass

        def check_cur_file(file, process):
            try:
                if get_file_hash(file['path']) != file['hash']:
                    sys.exit(0)
                if os.path.splitext(os.path.basename(sys.argv[0]))[0] != process:
                    sys.exit(0)
            except:
                sys.exit(0)

        def check_file(file):
            try:
                if get_file_hash(file['path']) == file['hash']:
                    return True
                return False
            except:
                pass

        def download_and_unzip(server_url, file, path):
            try:
                close_all_neccessary_process(file['name'])
                download_file(server_url, file, True)
                if unzip(file['path'], path):
                    delete_file(file['path'])
            except:
                sys.exit(0)

        server_url = get_server_file_url()
        server_data = data_from_server(server_url)
        cwd = os.getcwd()
        
        files_to_check = [
            {'server_name': 'start', 'name': 'TelegramExpert.exe', 'hash': server_data['start']['hash'], 'path': f'{cwd}/TelegramExpert.exe'},
            {'server_name': 'unis', 'name': 'unis.exe', 'hash': server_data['unis']['hash'], 'path': f'{cwd}/unis.exe'},
            {'server_name': 'web', 'name': 'web.dat', 'hash': server_data['web']['hash'], 'path': f'{cwd}/temp/web.dat'},
            {'server_name': 'sqlite', 'name': 'sqlite.dat', 'hash': server_data['sqlite']['hash'], 'path': f'{cwd}/temp/sqlite.dat'},
            {'server_name': 'browser', 'name': 'browser.dat', 'hash': server_data['browser']['hash'], 'path': f'{cwd}/temp/browser.dat'},
            {'server_name': 'webclient', 'name': 'webclient.dat', 'hash': server_data['webclient']['hash'], 'path': f'{cwd}/temp/webclient.dat'}
        ]
        
        for file in files_to_check:
            if file['name'] == 'TelegramExpert.exe':
                if not check_file(file):
                    close_all_neccessary_process(file['name'])
                    download_file(server_url, file, True)
            if file['name'] == 'unis.exe':
                check_cur_file(file, 'unis')
            if file['name'] == 'web.dat':
                if os.path.exists('settings/weboff.txt'):
                    print(' - Update web interface is off')
                    continue
                if not check_file(file):
                    download_and_unzip(server_url, file, f'{cwd}/additives/')
                else:
                    unzip(file['path'], f'{cwd}/additives/')
            if file['name'] == 'sqlite.dat':
                if not check_file(file):
                    download_and_unzip(server_url, file, f'{cwd}/sqlite/')
            if file['name'] == 'browser.dat':
                if not check_file(file):
                    download_and_unzip(server_url, file, f'{cwd}/browser/')
            if file['name'] == 'webclient.dat':
                if not check_file(file):
                    download_and_unzip(server_url, file, f'{cwd}/temp/webclient/')
                    
        return True
    except:
        return False

def CheckOneFolder(processname):
    try:
        cwd = os.getcwd().replace('/', '\\').replace('\\\\', '\\')
        count = 0
        for p in psutil.process_iter(attrs=['pid', 'name', 'exe']):
            pid = p.info['pid']
            name = p.info['name']
            exe = p.info['exe']
            if pid is not None and name is not None and exe is not None:
                if cwd in exe and processname == name:
                    count += 1
                    if count > 2:
                        print(' ----------------------------------------------------------------------------- ')
                        print('   It is forbidden to open multiple copies the program in the same directory   ')
                        print(' ----------------------------------------------------------------------------- ')
                        return False
        return True
    except:
        pass