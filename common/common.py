from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

#import time
import subprocess
import os

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

def prettyPrint(message):
    pPrint(message)

def isPingable(address):
  response = os.system("ping -c 1 " + address)
  if response == 0:
      pingstatus = True
  else:
      pingstatus = False # ping returned an error
  return pingstatus

def runShellCommand(command):
    try:
        completed = subprocess.run(command.split())
        loggerDEBUG(f'command {command} - returncode: {completed.returncode}')
    except:
        loggerERROR(f"error on method run shell command: {command}")