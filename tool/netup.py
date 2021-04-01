import psutil

addr = psutil.net_if_addrs()
ifaceList  = addr.keys()
byte = psutil.net_io_counters(pernic=True)

index = 0
for iface in ifaceList:
    net = iface
    ip = addr[iface][0][1]
    try:
        ipchek = ip.split(".")[3]
        status = "<span style='color:#00d600'>Up</span>"
        print(iface+"||"+ip+"||"+status +"|||")
    except:
        ip = " "
        status = "<span style='color:red'>Down</span>"

