import os
from common.logger import loggerDEBUGdim

def main()
    loggerDEBUGdim("launching wifi-connect")
    response = os.system("sudo wifi-connect -s "+ co.SSID_WIFICONNECT)
    loggerDEBUGdim(f"wifi-connect with response: {response}")
    