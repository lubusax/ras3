from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

#import time
import subprocess

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

def prettyPrint(message):
    pPrint(message)


def runShellCommand(command):
    try:
        completed = subprocess.run(command.split())
        loggerDEBUG(f'command {command} - returncode: {completed.returncode}')
    except:
        loggerERROR(f"error on method run shell command: {command}")