import subprocess
import os
import time
import signal


from common import files as fl
from common import constants as co
from common import processes as pr
from common.logger import loggerDEBUGdim
from common.common import isPingable
from multiprocessing import Process, Manager


from common.launcher import launcher

def is_eth0_up():
    with open(co.ETH0_OPERSTATE_FILE, "r") as f:
        result = f.read()
    if "up" in result:
        loggerDEBUGdim(f"eth0 is up")
        return True
    else:
        loggerDEBUGdim(f"eth0 is NOT up")
        return False    

def is_wlan0_up():
    with open(co.WLAN0_OPERSTATE_FILE, "r") as f:
        result = f.read()
    if "up" in result:
        loggerDEBUGdim(f"wlan0 is up")
        return True
    else:
        loggerDEBUGdim(f"wlan0 is NOT up")
        return False   

# def isDeviceConnected():
#     result = subprocess.check_output(
#         "nmcli dev status | grep 'connected' ",
#         shell=True).decode("utf-8")
#     if result:
#         loggerDEBUGdim("connected to internet (nmcli dev status)")
#         return True
#     else:
#         loggerDEBUGdim("not connected to internet (nmcli dev status)")
#         return False

# def isWiFiDefined():
#     return not fl.isDirectoryEmpty(co.DIR_WIFI_CONNECTIONS)

    
# def ensureConnectivity():
#     if isDeviceConnected():
#         loggerDEBUGdim(f"RAS is connected")
#         if wificonnectProcess and wificonnectProcess.is_alive():
#             loggerDEBUGdim(f"terminating wifi-connect {wificonnectProcess}")
#             wificonnectProcess.terminate()        
#         #setFlagToEthernetOrWiFi() # if Ethernet and WiFi are both available, Flag is Ethernet
#     else:
#         loggerDEBUGdim(f"RAS is NOT connected")
#         loggerDEBUGdim(f"starting wifi-connect {wificonnectProcess}")
#         if not wificonnectProcess:
#             wificonnectProcess = Process(name="wifi-connect", target=launcher, args=("common.wificonnect",))            
#         if not wificonnectProcess.is_alive():
#             wificonnectProcess.start()

#     time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)

def main():
    wificonnectProcess = None
    while True:
        if not isPingable("1.1.1.1"):
            if not is_eth0_up():
                if not is_wlan0_up():
                    loggerDEBUGdim(f"eth0 and wlan0 are both down - RAS is NOT connected")
                    if not wificonnectProcess:
                        wificonnectProcess = Process(   name="wifi-connect",           \
                                                        target=launcher,               \
                                                        args=("common.wificonnect",)  )
                    loggerDEBUGdim(f"starting wifi-connect {wificonnectProcess}")
                    if not wificonnectProcess.is_alive():
                        wificonnectProcess.start()
            else:
                loggerDEBUGdim(f"eth0 is up but internet (1.1.1.1) can not be reached- Check the Ethernet Internet Provider. RAS is NOT connected")
        elif wificonnectProcess:
            if wificonnectProcess.exitcode is None:
                loggerDEBUGdim(f"Internet (1.1.1.1) can be reached and wifi-connect is still running. Terminating wifi-connect {wificonnectProcess}")
                loggerDEBUGdim(f"wifi-connect Process PID is {wificonnectProcess.pid}")
                os.kill(wificonnectProcess.pid, signal.SIGTERM)
                wificonnectProcess = None      

        # TODO setFlagToEthernetOrWiFi() # if Ethernet and WiFi are both available, Flag is Ethernet

        time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)


if __name__ == "__main__":
    main()
