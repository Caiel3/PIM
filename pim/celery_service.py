'''Usage : python celery_service.py install (start / stop / remove)
Run celery as a Windows service
'''
from logging import exception
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import subprocess
import sys
import os
from pathlib import Path
import shlex
import logging
import time

# The directory for celery.log and celery_service.log
# Default: the directory of this script
INSTDIR = Path(__file__).parent
# The path of python Scripts
# Usually it is in path_to/venv/Scripts.
# If it is already in system PATH, then it can be set as ''
PYTHONSCRIPTPATH = INSTDIR / 'D:/Users/Administrador/AppData/Local/Programs/Python/Python38/Scripts'
=======
PYTHONSCRIPTPATH = INSTDIR / 'D:/Users/Administrador/AppData/Local/Programs/Python/Python38-32/Scripts'
>>>>>>> 3cba3160d8a459b29f0a369ebdb7fdf52a395380
# The directory name of django project
# Note: it is the directory at the same level of manage.py
# not the parent directory
PROJECTDIR = 'pim'

logging.basicConfig(
    filename = INSTDIR / 'celery_service.log',
    level = logging.DEBUG, 
    format = '[%(asctime)-15s: %(levelname)-7.7s] %(message)s'
)

class CeleryService(win32serviceutil.ServiceFramework):

    _svc_name_ = "Celery_pim"
    _svc_display_name_ = "Pim celery service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

    def SvcStop(self):
        logging.info('Stopping {name} service ...'.format(name=self._svc_name_))        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        sys.exit()           

    def SvcDoRun(self):
        try:
            logging.info('Starting dmartine {name} service ...'.format(name=self._svc_name_))
            os.chdir(INSTDIR) # so that proj worker can be found
            logging.info('cwd: ' + os.getcwd())
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            command = '"{celery_path}" -A {proj_dir} worker -f "{log_path}" -l info '.format(
=======
            command = '"{celery_path}" -A {proj_dir} worker -f "{log_path}" -l info -P eventlet'.format(
>>>>>>> 3cba3160d8a459b29f0a369ebdb7fdf52a395380
                celery_path=PYTHONSCRIPTPATH / 'celery.exe',
                proj_dir=PROJECTDIR,
                log_path=INSTDIR / 'celery.log')
            logging.info('command: ' + command)
            args = shlex.split(command)
            proc = subprocess.Popen(args)
            logging.info('pid: {pid}'.format(pid=proc.pid))
            self.timeout = 3000
            while True:
                rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                if rc == win32event.WAIT_OBJECT_0:
                    # stop signal encountered
                    # terminate process 'proc'
                    PROCESS_TERMINATE = 1
                    handle = win32api.OpenProcess(PROCESS_TERMINATE, False, proc.pid)
                    win32api.TerminateProcess(handle, -1)
                    win32api.CloseHandle(handle)                
                    break

            pass
        except exception as e:
            logging.info(f'Ocurrio un error {e}')
            pass
        
if __name__ == '__main__':
    try:
        l= win32serviceutil.HandleCommandLine(CeleryService)
        logging.info(f'user {PYTHONSCRIPTPATH}' )
        pass
    except exception as e:
       
        logging.info(f'Un error {e}')
        pass
   