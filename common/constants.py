from decouple import config

WORKING_DIR = config("WORKING_DIR")
DIR_WIFI_CONNECTIONS = config("DIR_WIFI_CONNECTIONS")
SSID_WIFICONNECT = config("SSID_WIFICONNECT")
PERIOD_CONNECTIVITY_MANAGER = 10 # in seconds
ETH0_OPERSTATE_FILE = config("ETH0_OPERSTATE_FILE")
WLAN0_OPERSTATE_FILE = config("WLAN0_OPERSTATE_FILE")
WAIT_PERIOD_FOR_PROCESS_GRACEFUL_TERMINATION = 10 # in seconds

INTERFACES = {
    "eth0"  : [ETH0_OPERSTATE_FILE,],
    "wlan0" : [WLAN0_OPERSTATE_FILE,]
    }