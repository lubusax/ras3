import time
import os

from common import files as fl
from common import constants as co

from processes import internet_connectivity as ic

ic.setConnectedEnvVariable()

if fl.isDirectoryEmpty(co.DIR_WIFI_CONNECTIONS):
  print(time.strftime("%a, %d %b %Y %H:%M:%S +0000"), " no wifi connections found")
  response = os.system("sudo wifi-connect -s "+ co.SSID_WIFICONNECT)
  print(time.strftime("%a, %d %b %Y %H:%M:%S +0000"), " after wifi connect with response: ", response)
else:
  print(time.strftime("%a, %d %b %Y %H:%M:%S +0000"), " at least one wifi connection found")