import time

from common import constants as co
from connectivity import helpers as ch   # connectivity helpers

def main():

    server = serverAccesPoint = ch.wificonnectProcess() # server to define a new SSID WiFi 

    while True:

        if not ch.internetReachable():

            server.handleInternetNotReachable()

        elif server.isRunning():            # internet is working,

            server.terminate()                   # wifi connect should be terminated

        time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)

        # TODO setFlagToEthernetOrWiFi() # if Ethernet and WiFi are both available, Flag is Ethernet


if __name__ == "__main__":
    main()
