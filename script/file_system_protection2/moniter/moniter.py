import sys
import json
from win32.database import *
from win32.functions import *

def ussage():
    print("")
    print("Argument not found.")
    return 1

def main():
    argv = sys.argv
    if len(argv) != 4:
        if len(argv) == 2:
            if(argv[1] == '-l'):
                print(json.dumps({'moniter_list':get_list_moniter_object()}))
                return 0
            elif argv[1]  == '-a':
                print(json.dumps({'alert_list':get_list_alert()}))
                return 0
            elif argv[1] == '-e':
                print(json.dumps({'last_alert_id':getLastAlertId()}))
                return 0
            elif argv[1]  == '-f':
                print(json.dumps({'file_list':get_list_moniter_file()}))
                return 0

        if len(argv) == 3:
            if(argv[1] == '-a'):
                print(json.dumps({'alert_list':getAlertListFromId(argv[2])}))
                return 0
                
        return ussage()
    if argv[1] == '-i':
        res = insert_moniter_obj(argv[2], argv[3])
        
        checkList = get_list_moniter_object()
        if res == 0:
            print(json.dumps({'result': res == 0, 'moniter_list': checkList}))
        else:
            print(json.dumps({'result': False, 'error_msg': res, 'moniter_list': checkList}))

        return 0
    elif argv[1] == '-r':
        res = remove_moniter_obj(argv[2], argv[3])
        checkList = get_list_moniter_object()
        if res == 0:
            print(json.dumps({'result': res == 0, 'moniter_list': checkList}))
        else:
            print(json.dumps({'result': False, 'error_msg': res, 'moniter_list': checkList}))

    elif argv[1] == '-s':
        res, msg = scan(argv[2], argv[3])
        # alertList = get_alert_list()
        succ = res == 0
        if res != 0:
            print(json.dumps({'result': succ, 'error_msg': msg}))
        else:
            print(json.dumps({'result': succ, 'message': msg}))
        return 0
   
if __name__ == '__main__':
    # removeDb()
    # print(get_list_sys_check())
    main()
    # resetDb()
    # checkList = get_check_list()
    # print({'result': res == 0, 'check_list': checkList})

