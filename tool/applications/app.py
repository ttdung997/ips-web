import subprocess
import re
import json
import argparse
def getDpkgList():
    command = 'dpkg --list'
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, err = p.communicate()
    return output

def processOneLineData(line):
    # input = b' aircrack-ng            1:1.5.2-3          amd64        wireless WEP/WPA cracking utilities'
    # output = {"application_name": "aircrack-ng", "version" : "1:1.5.2-3", "architect":"amd64", "description": "wireless WEP/WPA cracking utilities"}
    line = line.strip().split()
    app = dict(
        application_name=line[0].decode("utf-8"),
        version=line[1].decode("utf-8"),
        architect=line[2].decode("utf-8"),
        description=(b" ".join(line[3:]).decode("utf-8"))
    )
    print(app)
# regex = "ii "
def getListApp():
    listapp = []
    dpkglist = getDpkgList().split(b"\nii")
    for line in dpkglist[1:]:
        try:
            app = processOneLineData(line)
            if type(app) == dict:
                listapp.append(app)
        except:
            continue
    return listapp

def getListAppJson():
    return json.dumps(getListApp(), indent=4)


def checkUpgradeable():
    command = 'apt list --upgradeable'
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, err = p.communicate()
    # print(output, err)
    # output = str(output)
    listpackage = output.split(b"\n")
    dictpackage = []
    for pack in listpackage[1:-1]:
        try:
            pack = str(pack)
            pack_info = pack.split()
            package = dict(
                package_name=(pack_info[0].split('/')[0]),
                current_version=pack_info[-1][:-1],
                newest_version=pack_info[1],
                architect=pack_info[2]
            )
            dictpackage.append(package)
        except Exception as e:
            print(e, listpackage.index(pack))
            continue

    return json.dumps(dictpackage, indent=4)

def main():
    parser = argparse.ArgumentParser(description="""Get linux information package\n
    Example: 
    - To get list pakage as json:  ./app 
    - To check list update package:      ./app --upgradeable

    Author: Nguyen Quoc Khanh
    Email:  nqkpro96@gmail.com
    Bach Khoa Cyber Security, Hanoi, 2020
    """)
    parser.add_argument('--upgradeable', action="store_true", help='check list update package:')
    args = parser.parse_args()
    if args.upgradeable:
        return print(checkUpgradeable())
    else:
        return getListAppJson()
if __name__ == "__main__":
    main()
