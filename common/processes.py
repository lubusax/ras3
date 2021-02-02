import psutil

from common.common import prettyPrint as pp
from common.logger import loggerDEBUGdim

def isProcessRunning(processSearchString):
    '''
    Return True
    if there is any running process
    that contains the input value.
    '''
    for proc in psutil.process_iter():
        try:
            if processSearchString.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            #TODO log ERROR
            return False
    return False

def getProcessObject(processSearchString):
    '''
    Return "psutil process Object"
    if there is any running process
    that contains the input value.
    '''
    for proc in psutil.process_iter():
        #pp(proc)
        try:
            if processSearchString.lower() in proc.name().lower():
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            #TODO logError
            return None
    return None

def tests(processSearchString="chrome"):

    def test1(processSearchString):
        if isProcessRunning(processSearchString):
            loggerDEBUGdim(f'A process with name {processSearchString} was running')
        else:
            loggerDEBUGdim(f'No process with name {processSearchString} was running')

    def test2(processSearchString):
        processObject = getProcessObject(processSearchString)
        if processObject:
            loggerDEBUGdim(f'A process with name {processSearchString} was running')
            pp(processObject)
        else:
            loggerDEBUGdim(f'No process with name {processSearchString} was found')

    test1(processSearchString)
    test2(processSearchString)