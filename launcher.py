import time
import os

from common import files
from common import constants as c

# DIR_WIFI_CONNECTIONS = "/etc/NetworkManager/system-connections"
# SSID_WIFICONNECT = "__ras__"

if files.isDirectoryEmpty(c.DIR_WIFI_CONNECTIONS):
  print(time.strftime("%a, %d %b %Y %H:%M:%S +0000"), " no wifi connections found")
  response = os.system("sudo wifi-connect -s "+ c.SSID_WIFICONNECT)
  print(time.strftime("%a, %d %b %Y %H:%M:%S +0000"), " after wifi connect with response: ", response)
else:
  print(time.strftime("%a, %d %b %Y %H:%M:%S +0000"), " at least one wifi connection found")