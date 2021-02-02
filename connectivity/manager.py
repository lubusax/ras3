import subprocess
import os
import time


from common import files as fl
from common import constants as co
from common import processes as pr


def setEthernetEnvVariable():
  pass

def isDeviceConnected():
    result = subprocess.check_output(
        "nmcli general | grep 'connected' &> /dev/null",
        shell=True).decode("utf-8")
    if result:
        print("connected to internet: using nmcli general")
        return True
    else:
        print("not connected to internet: using nmcli general")
        return False

def isWiFiDefined():
    return not fl.isDirectoryEmpty(co.DIR_WIFI_CONNECTIONS)

def launchWiFiConnect():
    print(time.strftime("%a, %d %b %Y %H:%M:%S"), "before wifi connect")
    response = os.system("sudo wifi-connect -s "+ co.SSID_WIFICONNECT)
    print(time.strftime("%a, %d %b %Y %H:%M:%S"), "after wifi connect with response: ", response)

def killWifiConnect():
    if pr.isProcessRunning("wifi-connect"):
        #kill it
        pass


def ensureConnectivity():
    if isDeviceConnected():
        killWifiConnect()
        setFlagToEthernetOrWiFi() # if Ethernet and WiFi are both available, Flag is Ethernet
    else:
        launchWifiConnect()

    time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)

def main():
    ensureConnectivity()

if __name__ == "__main__":
    main()
