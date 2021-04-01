import os
import csv
import sys
import win32con
import winerror
import traceback
import win32evtlog
# import win32evtlogutil
from time import strftime

evt_types = {win32con.EVENTLOG_AUDIT_FAILURE: 'EVENTLOG_AUDIT_FAILURE',
             win32con.EVENTLOG_AUDIT_SUCCESS: 'EVENTLOG_AUDIT_SUCCESS',
             win32con.EVENTLOG_INFORMATION_TYPE: 'EVENTLOG_INFORMATION_TYPE',
             win32con.EVENTLOG_WARNING_TYPE: 'EVENTLOG_WARNING_TYPE',
             win32con.EVENTLOG_ERROR_TYPE: 'EVENTLOG_ERROR_TYPE'}

evt_obj_access = {12800: 'File System',
                  12801: 'Registry',
                  12802: 'Kernel Object',
                  12803: 'SAM',
                  12804: 'Other Object Access Events',
                  12805: 'Certification Services',
                  12806: 'Application Generated',
                  12807: 'Handle Manipulation',
                  12808: 'File Share',
                  12809: 'Filtering Platform Packet Drop',
                  12810: 'Filtering Platform Connection',
                  12811: 'Detailed File Share',
                  12812: 'Removable Storage',
                  12813: 'Central Policy Staging'}

# Define return error code
ERROR_PRIVILEGE = -3
ERROR_IO = -2
ERROR_CODE = -1
SUCCESS_CODE = 0
SKIP_CODE = 1

pathDirLogs = r"C:\Users\Cu Lee\Desktop\\"

# A list of file extensions to ignore
tmp_files = ['tmp', "rgt", "mta", "tlg", ".nd", ".ps", "log", "ldb", ":Zone.Identifier", "crdownload",
             ".DS_Store", ":AFP_AfpInfo", ":AFP_Resource"]
# A list of users to ignore
ignored_users = ["QBDataServiceUser25", "Example1"]
# Hashtable
pending_del = {}


def parse_event(evt_id, data):
    print(evt_id, data)


def get_events_log(name_server, log_type, path_log):
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    try:
        hand = win32evtlog.OpenEventLog(name_server, log_type)
        num_records = win32evtlog.GetNumberOfEventLogRecords(hand)
        print("There are %s = %d records." % (log_type, num_records))
    except (Exception, ValueError):
        return ERROR_PRIVILEGE

    path_csv = path_log + strftime('%y-%m-%d_%H.%M.%S') + ".csv"
    print(path_csv)
    try:
        with open(path_csv, mode='w') as f_csv:
            csv_writer = csv.writer(f_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Time', 'User', 'Action', 'Source', 'Destination', 'DebugNotes'])

            num = 0
            while 1:
                objects = win32evtlog.ReadEventLog(hand, flags, 0)
                if not objects:
                    print("xxx")
                    break

                for obj in objects:
                    evt_id = winerror.HRESULT_CODE(obj.EventID)
                    if not obj.StringInserts:
                        continue
                    user = obj.StringInserts[1]
                    try:
                        obj_name = obj.StringInserts[6]
                    except (Exception, ValueError):
                        continue
                    evt_time = obj.TimeGenerated.Format("%d/%m/%y %H:%M:%S")
                    print(user, obj_name, evt_time, 123)

                    if evt_id == 4656 and obj_name in pending_del:
                        print(1)
                        pending_del[obj_name]['Alive'] = True
                    elif evt_id == 4663 and obj.StringInserts[9] == "0x10000" and not ("recycle" in obj_name):
                        if obj_name in pending_del:
                            del pending_del[obj_name]
                        print(2)
                        pending_del[obj_name]['User'] = user
                        pending_del[obj_name]['HandleID'] = obj.StringInserts[7]
                        pending_del[obj_name]['TimeCreated'] = evt_time
                        pending_del[obj_name]['Alive'] = False
                        pending_del[obj_name]['Confirmed'] = False
                    elif evt_id == 4663 and obj.StringInserts[9] == "0x2" and not ("recycle" in obj_name):
                        csv_writer.writerow([evt_time, user, "created/modified", obj_name, "", "0x2 AccessMask"])
                        del pending_del[obj_name]
                    elif evt_id == 4663 and obj.StringInserts[9] == "0x80":
                        print(3)
                        for key in pending_del.keys():
                            dk = pending_del[key]["HandleID"] == obj.StringInserts[7] \
                                 and pending_del[key]["User"] == user and obj_name != key \
                                 and not pending_del[key]["Confirmed"]
                            if dk:
                                csv_writer.writerow([evt_time, user, "xxx", key, obj_name, ""])
                                del pending_del[obj_name]
                                break
                        if obj_name in pending_del:
                            pending_del[obj_name]["Alive"] = True
                    elif evt_id == 4659:
                        csv_writer.writerow([evt_time, user, "deleted", obj_name, "", "Event 4659"])
                    elif evt_id == 4660:
                        for key in pending_del.keys():
                            con = pending_del[key]["HandleID"] == obj.StringInserts[7] \
                                  and pending_del[key]['User'] == user
                            if con:
                                pending_del[key]["Confirmed"] = True
                num = num + len(objects)
            if num_records == num:
                print("Successfully read all %d records." % num_records)
            else:
                print("Couldn't get all records - reported %d, but found %d" % (num_records, num))
                print("(Note that some other app may have written records while we were running!)")
        return SUCCESS_CODE
    except(Exception, ValueError):
        print(traceback.print_exc(sys.exc_info()))
        print("xxxxxx")
        return ERROR_IO

    # path = r"C:\Event_Logs\Security.evtx"
    # try:
    #     hand = win32evtlog.OpenBackupEventLog(None, path)
    #     numRecords = win32evtlog.GetNumberOfEventLogRecords(hand)
    #     print(numRecords)
    # except (Exception, ValueError):
    #     return ERROR_CODE


def get_all_log_type(name_server, log_types):
    if not name_server:
        name_server = 'localhost'

    # Browse all log type
    for log_type in log_types:
        path_log = os.path.join(pathDirLogs, "%s\\" % name_server)
        if not os.path.isdir(path_log):
            os.mkdir(path_log)
        path_log += log_type + "\\"
        if not os.path.isdir(path_log):
            os.mkdir(path_log)
        res = get_events_log(name_server, log_type, path_log)
        if res == ERROR_PRIVILEGE:
            print("Bạn phải chạy với quyền Administrator")


if __name__ == '__main__':
    # None: local machine
    server = None
    # log_types_list = ['System', 'Application', 'Security']
    log_types_list = ['Security']
    get_all_log_type(server, log_types_list)
