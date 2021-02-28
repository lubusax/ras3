import os, sys, time 
import importlib
from typing import Dict, List

import flask

import zmq

from multiprocessing import Process, Manager

from colorama import Fore as cf
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

from common import constants as co
from common.launcher import launcher
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG
from messaging.messaging import SubscriberMultipart as Subscriber

loggerINFO(f'running on python version: {sys.version}')

managed_essential_processes = { # key(=process name) : (pythonmodule where the process is defined (= process name))
    "internet_connectivity_d": "connectivity.manager",
    "thermal_d": "thermal.manager"   
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
    #running_list = ["%s%s\u001b[0m" % ("\u001b[32m" if running[p].is_alive() else "\u001b[31m", p) for p in running]
    running_alive = [p for p in running if running[p].is_alive()]
    running_dead = [p for p in running if p not in running_alive]
    loggerDEBUG("alive: " + cf.GREEN + ' ; '.join(running_alive) + cf.RESET)    
    loggerDEBUG("dead: " + cf.RED + ' ; '.join(running_dead) + cf.RESET) 

def manager_thread():
    ras_subscriber = Subscriber("5556")
    ras_subscriber.subscribe("thermal")
    log_begin_manager_thread()
    start_all_daemon_processes()
    start_all_managed_processes()
    #thermal = ThermalStatus() # instance of class ThermalStatus
    while 1:
        # get thermal status
        topic, message = ras_subscriber.receive() # BLOCKING
        #loggerDEBUG(f"received {topic} {message}")
        if topic == "thermal":
            counter, temperature, load_5min, memUsed = \
                message.split()     
            loggerDEBUG(f"thermal update nr.{counter}: T {temperature}°C," + \
                f" CPU load 5 min avg {load_5min}%, mem used {memUsed}%")

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