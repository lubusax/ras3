import subprocess
import os


def setEthernetEnvVariable():
  pass

def setConnectedEnvVariable():
    result = subprocess.check_output(
        "nmcli general | grep 'connected' &> /dev/null",
        shell=True).decode("utf-8")
    if result:
        print("connected to internet: using nmcli general")
        os.environ["C_CONNECTED"] = "True"
    else:
        print("not connected to internet: using nmcli general")
        os.environ["C_CONNECTED"] = "False"
