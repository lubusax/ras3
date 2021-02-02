import os
from common.logger import loggerDEBUGdim
from common import constants as co

def main():
    loggerDEBUGdim("launching wifi-connect")
    response = os.system("wifi-connect -s "+ co.SSID_WIFICONNECT)
    loggerDEBUGdim(f"wifi-connect with response: {response}")
    