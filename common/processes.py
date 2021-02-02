import psutil

from common.common import prettyPrint as pp
from common.logger import loggerDEBUGdim

def isProcessRunning(processName):
    '''
    Return True
    if there is any running process
    that contains the input value.
    '''
    if processName:
        for proc in psutil.process_iter():
            try:
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                #TODO log ERROR
                return False
    return False

def getProcessObject(processName):
    '''
    Return "psutil process Object"
    if there is any running process
    that contains the input value.
    '''
    if processName:
        for proc in psutil.process_iter():
            pp(proc)
            try:
                if processName.lower() in proc.name().lower():
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                #TODO logError
                return None
    return None

def killProcess(processName):
    if processName:
        processtoKill= getProcessObject(processName)
        if processtoKill:
            processtoKill.kill()
            return True
    return False

def tests(processName):

    def test1(processName): # isProcessRunning
        if isProcessRunning(processName):
            loggerDEBUGdim(f'A process with name {processName} was running')
        else:
            loggerDEBUGdim(f'No process with name {processName} was running')

    def test2(processName): # getProcessObject
        processObject = getProcessObject(processName)
        if processObject:
            loggerDEBUGdim(f'A process with name {processName} was running')
            pp(processObject)
        else:
            loggerDEBUGdim(f'No process with name {processName} was found')

    def test3(processName): # killProcess
        # TODO
        pass


    test1(processName)
    test2(processName)
    test3(processName)