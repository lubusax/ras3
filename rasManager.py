import os, sys, time 
import importlib
from typing import Dict, List

from multiprocessing import Process, Manager

from common import constants as co
from common.launcher import launcher
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG


loggerINFO(f'running on python version: {sys.version}')

managed_essential_processes = { # key(=process name) : (pythonmodule where the process is defined (= process name))
    "internet_connectivity_d": "connectivity.manager"    
}

managed_NON_essential_processes = {}

managed_processes = {
    **managed_essential_processes,
    **managed_NON_essential_processes
    }

daemon_processes = {}

running: Dict[str, Process] = {}

def start_managed_process(name):
    if name not in running and name in managed_processes:
        preimport_managed_process(name)
        process = managed_processes[name]
        loggerINFO(f"starting python process {process}")
        running[name] = Process(name=name, target=launcher, args=(process,))
        running[name].start()

def start_daemon_process(name):
    pass

def start_all_daemon_processes():
    pass

def terminate_managed_process(name):
    loggerINFO(f"terminating python process {process}")
    pass

def preimport_managed_process(name):
    module = managed_processes[name]
    loggerINFO(f"preimporting {module}")
    importlib.import_module(module)

def start_all_managed_processes():
    for name in managed_processes:
        start_managed_process(name)

def start_all_daemon_processes():
    for name in daemon_processes:
        start_daemon_process(name)

def terminate_non_essential_managed_processes():
    for p in managed_NON_essential_processes:
        terminate_managed_process(p)

def log_begin_manager_thread():
    loggerINFO(f"starting manager thread") 
    loggerINFO({"environ": os.environ})

def log_running_processes_list():
    running_list = ["%s%s\u001b[0m" % ("\u001b[32m" if running[p].is_alive() else "\u001b[31m", p) for p in running]
    loggerDEBUG(' '.join(running_list))    

def manager_thread():
    log_begin_manager_thread()
    start_all_daemon_processes()
    start_all_managed_processes()
    #thermal = ThermalStatus() # instance of class ThermalStatus
    while 1:
        # get thermal status
        if False: #thermal.isCritical()
            terminate_non_essential_managed_processes()
        else:
            start_all_managed_processes()
        log_running_processes_list()
        time.sleep(co.PERIOD_MAIN_THREAD)


def main():

  try:
    manager_thread()
  except Exception as e:
    loggerCRITICAL(f'managerThread() failed to start with exception {e}')
  finally:
    # TODO cleanupAllProcesses()
    pass


if __name__ == "__main__":

  try:
    main()
  except Exception as e:
    loggerCRITICAL(f'main() failed to start with exception {e}')