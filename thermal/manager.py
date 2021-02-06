import time
import psutil
import zmq

from common import constants as co
# from connectivity import helpers as ch   # connectivity helpers
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG
from messaging.messaging import PublisherMultipart as Publisher

def main():

    pub_thermal = Publisher("5556")

    cpu_count = psutil.cpu_count()

    counter = 0

    while True:
        # msg.thermal.freeSpace = get_available_percent(default=100.0) / 100.0
        # msg.thermal.memUsedPercent = int(round(psutil.virtual_memory().percent))
        # msg.thermal.cpuPerc = int(round(psutil.cpu_percent()))

        #msg.thermal.freeSpace = get_available_percent(default=100.0) / 100.0
        memUsedPercent = int(round(psutil.virtual_memory().percent))
        cpuPerc = int(round(psutil.cpu_percent()))
        loadAvg = psutil.getloadavg()
        temperatures = psutil.sensors_temperatures()
        temperatureCurrent = int(psutil.sensors_temperatures()['cpu_thermal'][0].current)

        loadAvgPerc = [ int(round(l*100/cpu_count)) for l in loadAvg]
        loggerDEBUG(f"memUsedPercent {memUsedPercent}%")    
        loggerDEBUG(f"cpuPerc {cpuPerc}%") 
        loggerDEBUG(f"loadAvgPerc 1min:{loadAvgPerc[0]}% - 5min:{loadAvgPerc[1]}% - 15min:{loadAvgPerc[2]}%" ) 
        loggerDEBUG(f"current temperature {temperatureCurrent}°C")

        message = f"{counter} {temperatureCurrent} {loadAvgPerc[1]} {memUsedPercent}"

        pub_thermal.publish("thermal", message)
        # temperature max CPU RPi 85°C - Yellow > 80°C - Red > 84°C (self defined limits)
        counter += 1

        time.sleep(co.PERIOD_THERMAL_MANAGER)


if __name__ == "__main__":
    main()
