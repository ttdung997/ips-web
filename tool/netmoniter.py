import psutil
import time

addr = psutil.net_if_addrs()
ifaceList  = addr.keys()

index = 0
cardList = []
for iface in ifaceList:
    net = iface
    ip = addr[iface][0][1]
    try:
        ipcheck = ip.split(".")[3]
        status = "<span style='color:#00d600'>Up</span>"
        cardList.append(iface)
    except:
        status = "<span style='color:red'>Down</span>"

    # print(iface)
byte = psutil.net_io_counters(pernic=True)
# print(byte)
i = 0
for card in cardList:
    print(str(i)+"||"+card + "||"+str((byte[card][0]/8/1024-int(byte[card][0]/8/1024)))+"||"+str((byte[card][1]/8/1024/1000))+"|||")   
    i = i+1


