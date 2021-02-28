import socket

from common.common import prettyPrint as pp

def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

print(hostname_resolves("ras3-template"))