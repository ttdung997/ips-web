import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import json
import psutil


AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}


def main():
    templ = "%-5s %-30s %-30s %-13s %-6s %s"

    # print(templ % (
    #     "Proto", "Local address", "Remote address", "Status", "PID",
    #     "Program name"))
    # proc_names = {}
    netstat = []
    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']
    for c in psutil.net_connections(kind='inet'):
        netstat.append({
        "Proto": proto_map[(c.family, c.type)],
        "Local address" : c.laddr, 
        "Remote address" : c.raddr or AD, 
        "Status" : c.status,
        "PID" : c.pid or AD,
        "Program name" : proc_names.get(c.pid, '?')[:15]
        })
        # laddr = "%s:%s" % (c.laddr)
        # raddr = ""
        # if c.raddr:
        #     raddr = "%s:::%s" % (c.raddr)
        # print(templ % (
        #     proto_map[(c.family, c.type)],
        #     laddr,
        #     raddr or AD,
        #     c.status,
        #     c.pid or AD,
        #     proc_names.get(c.pid, '?')[:15],
        # ))
        # print(c.laddr['ip'])
        # break 
    print(netstat)
def getInfo():
    proc_names = {}
    netstat = []
    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']
    for c in psutil.net_connections(kind='inet'):
        netstat.append({
        "Proto": proto_map[(c.family, c.type)],
        "Local address" : c.laddr, 
        "Remote address" : c.raddr or AD, 
        "Status" : c.status,
        "PID" : c.pid or AD,
        "Program name" : proc_names.get(c.pid, '?')[:15]
        })
    return json.dumps(netstat, indent=4)

if __name__ == '__main__':
    print(getInfo())