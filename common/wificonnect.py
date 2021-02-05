import os
from common.logger import loggerDEBUG
from common import constants as co

def main():
    loggerDEBUG("launching wifi-connect")
    response = os.system("sudo wifi-connect -s "+ co.SSID_WIFICONNECT)
    loggerDEBUG(f"wifi-connect with response: {response}")
    