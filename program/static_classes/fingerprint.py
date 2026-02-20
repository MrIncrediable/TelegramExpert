import os
import subprocess
import uuid
import hashlib
import platform

def get_fingerprint():
    def wmic_check():
        try:
            cmd = ['wmic', 'csproduct', 'get', 'uuid', '/VALUE']
            subprocess.check_output(cmd, shell=True, text=True)
            return True
        except Exception as e:
            print(f'wmic_check {e}')
            return False

    def wmic_query(query, replace):
        try:
            output = subprocess.check_output(query, shell=True, text=True)[1:]
            clean_output = output.replace(replace, '').replace('=', '').replace('.', '').replace(' ', '').replace('\r', '').replace('\n', '').strip()
            if len(clean_output) > 5:
                return clean_output
            return False
        except Exception as e:
            print(f'wmic_query {e}')
            return False

    def shell_query(query, replace):
        try:
            output = subprocess.check_output(query, shell=True, text=True)
            clean_output = output.replace(replace, '').replace('=', '').replace('.', '').replace(' ', '').replace('\r', '').replace('\n', '').strip()
            if len(clean_output) > 5:
                return clean_output
            return False
        except Exception as e:
            print(f'shell_query {e}')
            return False

    if wmic_check():
        hwid_info = {}
        hwid_info['uid'] = wmic_query(['wmic', 'csproduct', 'get', 'uuid', '/VALUE'], 'uuid')
        hwid_info['cpu_id'] = wmic_query(['wmic', 'CPU', 'get', 'ProcessorId', '/VALUE'], 'ProcessorId')
        hwid_info['cpu_name'] = wmic_query(['wmic', 'CPU', 'get', 'caption', '/VALUE'], 'caption')
        hwid_info['hdd_serial'] = wmic_query(['wmic', 'DISKDRIVE', 'where', "MediaType='Fixed hard disk media'", 'get', 'SerialNumber', '/VALUE'], 'SerialNumber')
        hwid_info['hdd_model'] = wmic_query(['wmic', 'DISKDRIVE', 'where', "MediaType='Fixed hard disk media'", 'get', 'Model', '/VALUE'], 'Model')
        
        if hwid_info['hdd_model'] == False or hwid_info['hdd_model'] == '':
            hwid_info['hdd_model'] = hwid_info['uid']
            
        if hwid_info['hdd_serial'] == False or hwid_info['hdd_serial'] == '':
            hwid_info['hdd_serial'] = hwid_info['uid']
        else:
            hwid_info['hdd_serial'] = hwid_info['hdd_serial'][:40]
            
        hwid_string = f"{hwid_info['uid']}{hwid_info['cpu_id']}{hwid_info['cpu_name']}{hwid_info['hdd_serial']}{hwid_info['hdd_model']}"
        hwid_info['token'] = str(hashlib.md5(hwid_string.encode()).hexdigest()).upper()[:32]
        return hwid_info['token']
    else:
        hwid_info = {}
        hwid_info['hdd_serial'] = shell_query('powershell -Command "Get-PhysicalDisk | Select-Object -ExpandProperty SerialNumber"', 'SerialNumber')
        
        if hwid_info['hdd_serial'] != False:
            sys_info = platform.uname()
            hwid_info['uid'] = str(uuid.UUID(int=uuid.getnode()))
            hwid_info['cpu_name'] = sys_info.processor
            hwid_info['system'] = sys_info.system
            hwid_info['version'] = sys_info.version
            hwid_info['machine'] = sys_info.machine
            
            hwid_info['hdd_serial'] = hwid_info['hdd_serial'][:40]
            hwid_string = f"{hwid_info['uid']}{hwid_info['cpu_name']}{hwid_info['system']}{hwid_info['version']}{hwid_info['machine']}{hwid_info['hdd_serial']}"
            hwid_info['token'] = str(hashlib.md5(hwid_string.encode()).hexdigest()).upper()[:32]
            return hwid_info['token']
        return False

def get_lic_key():
    try:
        if os.path.exists('settings/license.txt'):
            with open('settings/license.txt', 'r') as f:
                return str(f.read(42))
        return False
    except:
        return False

def set_lic_key(info) -> bool:
    try:
        with open('settings/license.txt', 'w') as f:
            f.write(info)
        return True
    except:
        return False