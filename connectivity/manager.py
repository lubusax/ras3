import subprocess
import os
import time


from common import files as fl
from common import constants as co
from common import processes as pr
from common.logger import loggerDEBUGdim
from multiprocessing import Process, Manager

from common.launcher import launcher

def isDeviceConnected():
    return subprocess.check_output(
        "nmcli general | grep 'connected' &> /dev/null",
        shell=True).decode("utf-8")

def isWiFiDefined():
    return not fl.isDirectoryEmpty(co.DIR_WIFI_CONNECTIONS)

    
def ensureConnectivity():
    wificonnectProcess = Process(name="wifi-connect", target=launcher, args=("common.wificonnect",))
    if isDeviceConnected():
        loggerDEBUGdim(f"RAS is connected")
        if wificonnectProcess.is_alive():
            loggerDEBUGdim(f"terminating wifi-connect {wificonnectProcess}")
            wificonnectProcess.terminate()        
        #setFlagToEthernetOrWiFi() # if Ethernet and WiFi are both available, Flag is Ethernet
    else:
        loggerDEBUGdim(f"RAS is NOT connected")
        loggerDEBUGdim(f"starting wifi-connect {wificonnectProcess}")
        if not wificonnectProcess.is_alive():
            wificonnectProcess.start()

    time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)

def main():
    while True:
        ensureConnectivity()

if __name__ == "__main__":
    main()
