import os, sys, time 
#import importlib

from multiprocessing import Process, Manager

from common.launcher import launcher
from common.logger import loggerINFO, loggerCRITICAL


loggerINFO(f'running on python version: {sys.version}')

managed_essential_processes = {
    "connectivityManager": "connectivity.manager"    
}

managed_NON_essential_processes = {}

managed_processes = {
    **managed_essential_processes,
    **managed_NON_essential_processes
    }

daemon_processes = {}

running = {}

def start_managed_process(name):

    if name not in running and name in managed_processes:

        process = managed_processes[name]

        loggerINFO(f"starting python process {process}")

        running[name] = Process(name=name, target=launcher, args=(process,))

        running[name].start()

def terminate_managed_process(name):
  loggerINFO(f"killing python process {process}")

def start_all_managed_processes():
    for p in managed_processes:
        start_managed_process(p)

def start_all_daemon_processes():
    for p in daemon_processes:
        start_daemon_process(p)

def terminate_non_essential_managed_processes():
    for p in managed_NON_essential_processes:
        terminate_managed_process(p)

def managerThread():

    loggeINFO(f"starting manager thread") 

    start_all_daemon_processes()
    start_all_managed_processes()

    thermal = ThermalStatus() # instance of class ThermalStatus

    while 1:

        if thermal.isCritical():
            terminate_non_essential_managed_processes()
        else:
            start_all_managed_processes()

        thermal.update()

def main():

  try:
    managerThread()
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