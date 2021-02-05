import time
import psutil

from common import constants as co
# from connectivity import helpers as ch   # connectivity helpers
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG

def main():

    cpu_count = psutil.cpu_count()

    while True:
        # msg.thermal.freeSpace = get_available_percent(default=100.0) / 100.0
        # msg.thermal.memUsedPercent = int(round(psutil.virtual_memory().percent))
        # msg.thermal.cpuPerc = int(round(psutil.cpu_percent()))

        #msg.thermal.freeSpace = get_available_percent(default=100.0) / 100.0
        memUsedPercent = int(round(psutil.virtual_memory().percent))
        cpuPerc = int(round(psutil.cpu_percent()))
        loadAvg = psutil.getloadavg()
        temperatures = psutil.sensors_temperatures()

        loadAvgPerc = [ int(round(l*100/cpu_count)) for l in loadAvg]
        loggerDEBUG(f"memUsedPercent {memUsedPercent}%")    
        loggerDEBUG(f"cpuPerc {cpuPerc}%") 
        loggerDEBUG(f"loadAvgPerc 1min:{loadAvgPerc[0]}% - 5min:{loadAvgPerc[1]}% - 15min:{loadAvgPerc[2]}%" ) 
        loggerDEBUG(f"temperatures {temperatures}")

        time.sleep(co.PERIOD_THERMAL_MANAGER)


if __name__ == "__main__":
    main()
