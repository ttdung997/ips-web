import sys, os
import threading
from time import sleep
import subprocess
import time
import json
import requests
from json.decoder import JSONDecoder


class ThreadscanIntegrity (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while(True):
            # Tim id bao cao moi nhat
            cmdGetId = 'python3 script/file_system_protection/integrity_check_linux.py -e'
            pID = subprocess.Popen(cmdGetId, stdout=subprocess.PIPE, shell=True)
            (outputId, err) = pID.communicate()
            pID_status = pID.wait()
            ID = json.loads(outputId.decode('ASCII'))['last_alert_id']

            # lay danh sach tep tin/thu muc kiem tra tinh toan ven
            cmd = 'python3 script/file_system_protection/integrity_check_linux.py -l'
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()

            # Vong lap quet tung tep tin/ thu muc
            if(p_status == 0):
                data = json.loads(output.decode('ASCII'))['check_list']
                count = len(data)
                succ = 0
                error = 0
                i = 0
                for d in data:
                    cmd = 'python3 script/file_system_protection/integrity_check_linux.py -s ' + '"'+d[2]+'"'+" "+str(d[1])
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p_status = p.wait()

            # lay danh sach bao cao phat hien thay doi vua quet
            cmd = 'python3 script/file_system_protection/integrity_check_linux.py -a '+str(ID)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            alert = json.loads(output.decode('ASCII'))['alert_list']
            if(len(alert)>0):
                alertSend = json.loads(output.decode('ASCII'))
                print("integrity_check_linux")
                print(alertSend)
                ThreadsendReportIntegrityToServer = sendReportIntegrityToServer(alertSend)
                ThreadsendReportIntegrityToServer.start()

            time.sleep(3600)


class sendReportIntegrityToServer (threading.Thread):
    def __init__(self, alert):
        threading.Thread.__init__(self)
        self.alert=alert
    def run(self):
        try:
            # print(self.alert)
            # defining the api-endpoint  
            f = open("config.txt", "r")
            data = f.read().split(" |||")
            name = data[0].split(":: ")[1]
            url = data[1].split(":: ")[1]
            key = data[2].split(":: ")[1]
            API_ENDPOINT = url + "/integrity-update"
            # data to be sent to api 
            data = self.alert
              
            # sending post request and saving response as response object 
            r = requests.post(url = API_ENDPOINT, json = data) 
              
            # extracting response text  
            pastebin_url = r.text 
            print("The pastebin URL is:%s"%pastebin_url) 
        except Exception as e:
            print(e)


class ThreadscanMonitor (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while(True):
            # Tim id bao cao moi nhat
            cmdGetId = 'python3 script/file_system_protection/moniter/moniter_linux.py -e'
            pID = subprocess.Popen(cmdGetId, stdout=subprocess.PIPE, shell=True)
            (outputId, err) = pID.communicate()
            pID_status = pID.wait()
            ID = json.loads(outputId.decode('ASCII'))['last_alert_id']

            # lay danh sach tep tin/thu muc theo doi
            cmd = 'python3 script/file_system_protection/moniter/moniter_linux.py -l'
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()

            # Vong lap quet tung tep tin/ thu muc
            if(p_status == 0):
                data = json.loads(output.decode('ASCII'))['moniter_list']
                for d in data:
                    cmd = 'python3 script/file_system_protection/moniter/moniter_linux.py -s ' + '"'+d[2]+'"'+" "+str(d[1])
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p_status = p.wait()

            # lay danh sach bao cao phat hien thay doi vua quet
            cmd = 'python3 script/file_system_protection/moniter/moniter_linux.py -a '+str(ID)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            alert = json.loads(output.decode('ASCII'))['alert_list']
            print("moniter")
            print(alert)
            if(len(alert)>0):
                alertSend = json.loads(output.decode('ASCII'))
                ThreadsendReportMonitorToServer = sendReportMonitorToServer(alertSend)
                ThreadsendReportMonitorToServer.start()

            time.sleep(3600)


class sendReportMonitorToServer (threading.Thread):
    def __init__(self, alert):
        threading.Thread.__init__(self)
        self.alert=alert
    def run(self):
        try:
            # print(self.alert)
            # defining the api-endpoint  
            f = open("config.txt", "r")
            data = f.read().split(" |||")
            name = data[0].split(":: ")[1]
            url = data[1].split(":: ")[1]
            key = data[2].split(":: ")[1]

            API_ENDPOINT = url + "/moniter-update"
            # data to be sent to api 
            data = self.alert
              
            # sending post request and saving response as response object 
            r = requests.post(url = API_ENDPOINT, json = data) 
              
            # extracting response text  
            pastebin_url = r.text 
            print("The pastebin URL is:%s"%pastebin_url)
        except Exception as e:
            print(e)



if __name__ == "__main__":
    scanIntegrity = ThreadscanIntegrity()
    scanIntegrity.start()
    scanMonitor = ThreadscanMonitor()
    scanMonitor.start()

    

