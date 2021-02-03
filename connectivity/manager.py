import subprocess
import os
import time
import signal
import psutil


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

def on_terminate(proc):
    loggerDEBUGdim( \
        f"process {proc} terminated with exit code {proc.returncode}")

def main():

    wificonnectProcess = None

    def startWifiConnect():

        loggerDEBUGdim(f"eth0 and wlan0 are both down" + \ 
                        "- RAS is NOT connected")

        if not wificonnectProcess:
            wificonnectProcess = Process(   name="wifi-connect",           \
                                            target=launcher,               \
                                            args=("common.wificonnect",)  )

        loggerDEBUGdim(f"starting wifi-connect {wificonnectProcess}")

        if not wificonnectProcess.is_alive():
            wificonnectProcess.start()
    
    def terminateWifiConnect():
        if wificonnectProcess.exitcode is None:
            loggerDEBUGdim(f"Internet (1.1.1.1) can be reached and wifi-connect is still running. Terminating wifi-connect {wificonnectProcess}")
            loggerDEBUGdim(f"wifi-connect Process PID is {wificonnectProcess.pid}")
            proc0 = psutil.Process(pid=wificonnectProcess.pid)
            procs = proc0.children(recursive=True)
            procs.insert(0, proc0)
            for p in procs:
                loggerDEBUGdim(f"terminating PID {p.pid}")
                p.terminate()
            gone, alive = psutil.wait_procs(procs, timeout=10, callback=on_terminate)
            for p in alive:
                loggerDEBUGdim(f"killing PID {p.pid}")
                p.kill()
            wificonnectProcess = None

    def messageEth0NotWorking():
        loggerDEBUGdim( \
            f"eth0 is up but internet (1.1.1.1) can not be reached-"+ \ 
             " Check the Ethernet Internet Provider. RAS is NOT connected")

    def handleInternetNotReachable():
        if not is_eth0_up():
            if not is_wlan0_up():  # wlan0 is up 1)in mode AP (when wifi connect started) 
                startWifiConnect() # OR 2)when connected to a SSID
        else:
            messageEth0NotWorking()

    while True:

        if not isPingable("1.1.1.1"):
            handleInternetNotReachable()
        elif wificonnectProcess:            # internet is working,
            terminateWifiConnect()          # wifi connect should be terminated

        time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)
        # TODO setFlagToEthernetOrWiFi() # if Ethernet and WiFi are both available, Flag is Ethernet


if __name__ == "__main__":
    main()
