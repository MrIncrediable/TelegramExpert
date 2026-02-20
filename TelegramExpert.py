import os
import sys
from program.updater import Updater

def run_exe():
    try:
        program = 'unis.exe'
        os.system(program + ' -checked')
    except:
        print(' - Error, I can not run the file, check the operating system settings')
        _exit()

def _exit():
    input(' - To end the program, press [ENTER]')
    sys.exit()

if __name__ == '__main__':
    print(' ----------------------------------------------------------------------------- ')
    print(' --                                                                           -- ')
    print(' --                          TELEGRAM EXPERT RELEASE                        -- ')
    print(' --                                                                           -- ')
    print(' ----------------------------------------------------------------------------- ')
    print(' --  www.TelegramExpert.pro  --                     --  developed by STRIX  -- ')
    print(' ----------------------------------------------------------------------------- ')
    print('')
    
    if not Updater():
        sys.exit()
        
    run_exe()
    _exit()
    